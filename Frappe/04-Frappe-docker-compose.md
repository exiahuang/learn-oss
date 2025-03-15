# Frappe docker

https://github.com/frappe/frappe_docker/blob/main/pwd.yml

```yml
version: "3"

services:
  backend:
    image: frappe/erpnext:v15.54.3
    networks:
      - frappe_network
    deploy:
      restart_policy:
        condition: on-failure
    volumes:
      - sites:/home/frappe/frappe-bench/sites
      - logs:/home/frappe/frappe-bench/logs
    environment:
      DB_HOST: db
      DB_PORT: "3306"
      MYSQL_ROOT_PASSWORD: admin
      MARIADB_ROOT_PASSWORD: admin

  configurator:
    image: frappe/erpnext:v15.54.3
    networks:
      - frappe_network
    deploy:
      restart_policy:
        condition: none
    entrypoint:
      - bash
      - -c
    command:
      - >
        ls -1 apps > sites/apps.txt;
        bench set-config -g db_host $$DB_HOST;
        bench set-config -gp db_port $$DB_PORT;
        bench set-config -g redis_cache "redis://$$REDIS_CACHE";
        bench set-config -g redis_queue "redis://$$REDIS_QUEUE";
        bench set-config -g redis_socketio "redis://$$REDIS_QUEUE";
        bench set-config -gp socketio_port $$SOCKETIO_PORT;
    environment:
      DB_HOST: db
      DB_PORT: "3306"
      REDIS_CACHE: redis-cache:6379
      REDIS_QUEUE: redis-queue:6379
      SOCKETIO_PORT: "9000"
    volumes:
      - sites:/home/frappe/frappe-bench/sites
      - logs:/home/frappe/frappe-bench/logs

  create-site:
    image: frappe/erpnext:v15.54.3
    networks:
      - frappe_network
    deploy:
      restart_policy:
        condition: none
    volumes:
      - sites:/home/frappe/frappe-bench/sites
      - logs:/home/frappe/frappe-bench/logs
    entrypoint:
      - bash
      - -c
    command:
      - >
        wait-for-it -t 120 db:3306;
        wait-for-it -t 120 redis-cache:6379;
        wait-for-it -t 120 redis-queue:6379;
        export start=`date +%s`;
        until [[ -n `grep -hs ^ sites/common_site_config.json | jq -r ".db_host // empty"` ]] && \
          [[ -n `grep -hs ^ sites/common_site_config.json | jq -r ".redis_cache // empty"` ]] && \
          [[ -n `grep -hs ^ sites/common_site_config.json | jq -r ".redis_queue // empty"` ]];
        do
          echo "Waiting for sites/common_site_config.json to be created";
          sleep 5;
          if (( `date +%s`-start > 120 )); then
            echo "could not find sites/common_site_config.json with required keys";
            exit 1
          fi
        done;
        echo "sites/common_site_config.json found";
        bench new-site --mariadb-user-host-login-scope='%' --admin-password=admin --db-root-username=root --db-root-password=admin --install-app erpnext --set-default frontend;

  db:
    image: mariadb:10.6
    networks:
      - frappe_network
    healthcheck:
      test: mysqladmin ping -h localhost --password=admin
      interval: 1s
      retries: 20
    deploy:
      restart_policy:
        condition: on-failure
    command:
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
      - --skip-character-set-client-handshake
      - --skip-innodb-read-only-compressed # Temporary fix for MariaDB 10.6
    environment:
      MYSQL_ROOT_PASSWORD: admin
      MARIADB_ROOT_PASSWORD: admin
    volumes:
      - db-data:/var/lib/mysql

  frontend:
    image: frappe/erpnext:v15.54.3
    networks:
      - frappe_network
    depends_on:
      - websocket
    deploy:
      restart_policy:
        condition: on-failure
    command:
      - nginx-entrypoint.sh
    environment:
      BACKEND: backend:8000
      FRAPPE_SITE_NAME_HEADER: frontend
      SOCKETIO: websocket:9000
      UPSTREAM_REAL_IP_ADDRESS: 127.0.0.1
      UPSTREAM_REAL_IP_HEADER: X-Forwarded-For
      UPSTREAM_REAL_IP_RECURSIVE: "off"
      PROXY_READ_TIMEOUT: 120
      CLIENT_MAX_BODY_SIZE: 50m
    volumes:
      - sites:/home/frappe/frappe-bench/sites
      - logs:/home/frappe/frappe-bench/logs
    ports:
      - "18888:8080"

  queue-long:
    image: frappe/erpnext:v15.54.3
    networks:
      - frappe_network
    deploy:
      restart_policy:
        condition: on-failure
    command:
      - bench
      - worker
      - --queue
      - long,default,short
    volumes:
      - sites:/home/frappe/frappe-bench/sites
      - logs:/home/frappe/frappe-bench/logs

  queue-short:
    image: frappe/erpnext:v15.54.3
    networks:
      - frappe_network
    deploy:
      restart_policy:
        condition: on-failure
    command:
      - bench
      - worker
      - --queue
      - short,default
    volumes:
      - sites:/home/frappe/frappe-bench/sites
      - logs:/home/frappe/frappe-bench/logs

  redis-queue:
    image: redis:6.2-alpine
    networks:
      - frappe_network
    deploy:
      restart_policy:
        condition: on-failure
    volumes:
      - redis-queue-data:/data

  redis-cache:
    image: redis:6.2-alpine
    networks:
      - frappe_network
    deploy:
      restart_policy:
        condition: on-failure

  scheduler:
    image: frappe/erpnext:v15.54.3
    networks:
      - frappe_network
    deploy:
      restart_policy:
        condition: on-failure
    command:
      - bench
      - schedule
    volumes:
      - sites:/home/frappe/frappe-bench/sites
      - logs:/home/frappe/frappe-bench/logs

  websocket:
    image: frappe/erpnext:v15.54.3
    networks:
      - frappe_network
    deploy:
      restart_policy:
        condition: on-failure
    command:
      - node
      - /home/frappe/frappe-bench/apps/frappe/socketio.js
    volumes:
      - sites:/home/frappe/frappe-bench/sites
      - logs:/home/frappe/frappe-bench/logs

volumes:
  db-data:
  redis-queue-data:
  sites:
  logs:

networks:
  frappe_network:
    driver: bridge

```

# Frappe-ps

```sh
docker ps | grep frappe
frappe/erpnext:v15.54.3    "nginx-entrypoint.sh"    0.0.0.0:18888->8080/tcp, :::18888->8080/tcp  frappe_docker-frontend-1
frappe/erpnext:v15.54.3    "/home/frappe/frappe…"                                                frappe_docker-backend-1
frappe/erpnext:v15.54.3    "node /home/frappe/f…"                                                frappe_docker-websocket-1
frappe/erpnext:v15.54.3    "bench worker --queu…"                                                frappe_docker-queue-long-1
frappe/erpnext:v15.54.3    "bench schedule"                                                      frappe_docker-scheduler-1
frappe/erpnext:v15.54.3    "bench worker --queu…"                                                frappe_docker-queue-short-1
mariadb:10.6               "docker-entrypoint.s…"   3306/tcp                                     frappe_docker-db-1
redis:6.2-alpine           "docker-entrypoint.s…"   6379/tcp                                     frappe_docker-redis-cache-1
redis:6.2-alpine           "docker-entrypoint.s…"   6379/tcp                                     frappe_docker-redis-queue-1
```

docker exec -it frappe_docker-backend-1 bash

frappe_docker-backend-1
~/frappe-bench/apps/frappe/frappe



# config



```
~/frappe-bench$ ls apps/
erpnext  frappe

~/frappe-bench$ cat sites/apps.json
{
    "frappe": {
        "resolution": {
            "commit_hash": null,
            "branch": null
        },
        "required": [],
        "idx": 1,
        "version": "15.57.2"
    },
    "erpnext": {
        "is_repo": true,
        "resolution": {
            "commit_hash": "47429095a2bc48dc66e5fe091f804ca0dd78010c",
            "branch": "v15.54.3"
        },
        "required": [],
        "idx": 2,
        "version": "15.54.3"
    }
}

~/frappe-bench$ cat sites/apps.txt
erpnext
frappe

~/frappe-bench$ cat sites/common_site_config.json
{
 "db_host": "db",
 "db_port": 3306,
 "default_site": "frontend",
 "redis_cache": "redis://redis-cache:6379",
 "redis_queue": "redis://redis-queue:6379",
 "redis_socketio": "redis://redis-queue:6379",
 "socketio_port": 9000
}

```


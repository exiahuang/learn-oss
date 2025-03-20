# install

[frappe/frappe_docker: Docker images for production and development setups of the Frappe framework and ERPNext](https://github.com/frappe/frappe_docker)



```
git clone https://github.com/frappe/frappe_docker
cd frappe_docker
```


Then run: `docker compose -f pwd.yml up -d`


Wait for 5 minutes for ERPNext site to be created or check `create-site` container logs before opening browser on port 8080. (username: `Administrator`, password: `admin`)



http://localhost:18888/

http://localhost:18888/app/tools


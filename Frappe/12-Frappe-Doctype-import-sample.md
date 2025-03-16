# import doctype sample

http://localhost:18888/
http://localhost:18888/app

- Module Def: Salesforce

```sh
docker exec -it frappe_docker-backend-1 bash
bench --site frontend console
```

type -> fieldtype

```python
import frappe

def create_custom_doctypes():
    doctypes = [
        {
            "name": "User__c",
            "module": "Salesforce",
            "fields": [
                {"fieldname": "api_name_1", "label": "Api Name 1", "fieldtype": "Data"},
                {"fieldname": "api_name_2", "label": "Api Name 2", "fieldtype": "Int"},
                {"fieldname": "api_name_3", "label": "Api Name 3", "fieldtype": "Button"},
                {"fieldname": "api_name_4", "label": "Api Name 4", "fieldtype": "Duration"},
                {"fieldname": "api_name_5", "label": "Api Name 5", "fieldtype": "Float"},
                {"fieldname": "api_name_6", "label": "Api Name 6", "fieldtype": "Text"},
                {"fieldname": "api_name__c", "label": "Api Name 7", "fieldtype": "Date"}
            ]
        },
        {
            "name": "Account__c",
            "module": "Salesforce",
            "fields": [
                {"fieldname": "api_name_1", "label": "Api Name 1", "fieldtype": "Date"},
                {"fieldname": "api_name_2", "label": "Api Name 2", "fieldtype": "Check"}
            ]
        }
    ]

    for doctype in doctypes:
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": doctype["name"],
            "module": doctype["module"],
            "custom": 1,  # 设为 1 表示自定义 DocType
            "fields": doctype["fields"]
        })
        doc.insert()
        print(f"Created DocType: {doctype['name']}")

# 运行脚本
create_custom_doctypes()
```
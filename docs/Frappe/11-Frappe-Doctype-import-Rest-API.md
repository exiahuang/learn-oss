

# use rest api

https://gist.github.com/vmatt/cdd3d20a7fd7f1cab8224e2b167e3c01



```python
import requests

class DocTypeImporter:
    def __init__(self, url="http://127.0.0.1:8000/api", usr="", pwd=""):
        self.s = requests.Session()
        self.base_url = url
        self.headers = {"Content-Type": "application/json","Accept": "application/json"}

        if usr and pwd:
            self.__login(usr, pwd)
    def __login(self, usr, pwd):
        response = self.s.post(f"{self.base_url}/method/login", json={"usr": usr,"pwd": pwd}, headers=self.headers)
        return response

    def create_doc_type(self, doctype: str, module: str ="Custom", fields:list=[]):
        payload = {
            "name": doctype,
            "module": module,
            "custom": 1,
            "allow_import": 1,
            "doctype": "DocType",
            "actions": [],
            "fields": fields,
            "links": [],
            "states": []
        }
        response = self.s.post(f"{self.base_url}/resource/DocType", json=payload, headers=self.headers)
        return response


customApi = DocTypeImporter("http://127.0.0.1:8000/api/", usr="Administrator", pwd="...")
fields = [
            {
                "fieldname": "source_id",
                "label": "Source ID",
                "fieldtype": "Data",
                "doctype": "DocField"
            }
        ]

res = customApi.create_doc_type("Your Doc Type",fields=fields)
print(res.json())
```



# use frappe

```python
import frappe

def create_custom_doctypes():
    doctypes = [
        {
            "name": "Custom DocType 1",
            "module": "erpnext",
            "fields": [
                {"fieldname": "field_1", "label": "Field 1", "fieldtype": "Data"},
                {"fieldname": "field_2", "label": "Field 2", "fieldtype": "Int"}
            ]
        },
        {
            "name": "Custom DocType 2",
            "module": "erpnext",
            "fields": [
                {"fieldname": "field_3", "label": "Field 3", "fieldtype": "Date"},
                {"fieldname": "field_4", "label": "Field 4", "fieldtype": "Check"}
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




[Document API](https://docs.frappe.io/framework/user/en/api/document)



在 Frappe 中，批量创建 **Field（字段）** 可以通过以下几种方式实现：


## **方法 1：使用 Python 脚本（推荐）**

Frappe 提供了 `frappe.get_doc()` 方法，可以用 Python 批量向 **某个 DocType** 添加多个字段（Field）。

### **示例：批量添加字段到一个自定义 DocType**

```
import frappe

def add_custom_fields():
    doctype_name = "YourDocType"  # 替换为你的目标 DocType
    fields = [
        {"fieldname": "new_field_1", "label": "New Field 1", "fieldtype": "Data"},
        {"fieldname": "new_field_2", "label": "New Field 2", "fieldtype": "Int"},
        {"fieldname": "new_field_3", "label": "New Field 3", "fieldtype": "Date"},
    ]

    for field in fields:
        if not frappe.db.exists("Custom Field", {"dt": doctype_name, "fieldname": field["fieldname"]}):
            doc = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": doctype_name,  # 目标 DocType
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "insert_after": "description"  # 你可以修改这个值
            })
            doc.insert()
    
    frappe.db.commit()
    print("Fields added successfully!")

# 运行该函数
add_custom_fields()
```

📌 **说明**

- `doctype_name`：指定要添加字段的目标 DocType。
- `frappe.db.exists()`：避免重复创建字段。
- `"insert_after": "description"`：字段将被插入到 `description` 之后，可更改为其他字段名。
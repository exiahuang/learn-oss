# Frappe Shell

```sh
$ bench --site frontend console
Apps in this namespace:
frappe, erpnext

In [1]: import frappe
   ...: fields = frappe.get_all("Custom Field", filters={"dt": "Item"}, fields=["fieldname", "label", "fieldtype"])
   ...: for field in fields:
   ...:     print(field)
   ...:
{'fieldname': 'new_field_2', 'label': 'New Field 2', 'fieldtype': 'Int'}
{'fieldname': 'new_field_1', 'label': 'New Field 1', 'fieldtype': 'Data'}

In [2]:
```



# mariadb

```sh
bench --site your-site mariadb

> SELECT fieldname, label, fieldtype FROM `tabCustom Field` WHERE dt = 'Item';
+-------------+-------------+-----------+
| fieldname   | label       | fieldtype |
+-------------+-------------+-----------+
| new_field_1 | New Field 1 | Data      |
| new_field_2 | New Field 2 | Int       |
+-------------+-------------+-----------+
2 rows in set (0.001 sec)

```


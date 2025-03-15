### **✅ 如何查看导入的 Fields（字段）**

你已经成功使用 `bench --site` 导入了 `Custom Field`，现在可以通过以下方式查看这些字段：

------

## **🔹 方法 1：在 Frappe 后台 UI 中查看**

1. **登录 Frappe**（浏览器访问 `http://localhost:8000` 或 `http://your-domain.com`）。

2. 打开 "Customize Form"（自定义表单）

   ：

   - 在 **"Awesome Bar"** 搜索 **"Customize Form"** 并打开。
   - 选择 **你导入字段的 DocType**（比如 `Item`）。
   - 向下滚动，检查导入的字段是否已显示。

------

## **🔹 方法 2：通过 "Custom Field" 列表查看**

1. 在 **"Awesome Bar"** 搜索 **"Custom Field"** 并打开。
2. 在 **搜索框** 输入 **目标 DocType**（如 `Item`）。
3. 你应该能看到所有关联的 **自定义字段（Custom Fields）**。

------

## **🔹 方法 3：使用 Frappe Shell 查询**

如果你想在命令行中确认字段是否导入成功：

1. 进入 Frappe Shell

   ```bash
   bench --site your-site console
   ```

2. 查询某个 DocType 的自定义字段

   ```python
   import frappe
   fields = frappe.get_all("Custom Field", filters={"dt": "Item"}, fields=["fieldname", "label", "fieldtype"])
   for field in fields:
       print(field)
   ```

   📌 

   示例输出

   ```json
   {'fieldname': 'new_field_1', 'label': 'New Field 1', 'fieldtype': 'Data'}
   {'fieldname': 'new_field_2', 'label': 'New Field 2', 'fieldtype': 'Int'}
   ```

------

## **🔹 方法 4：数据库直接查询**

如果你怀疑数据没有正确写入数据库，可以进入 MariaDB 直接查询：

1. 进入数据库：

   ```bash
   bench --site your-site mariadb
   ```

2. 查询 

   ```
   Custom Field
   ```

    表：

   ```sql
   SELECT fieldname, label, fieldtype FROM `tabCustom Field` WHERE dt = 'Item';
   ```

   示例输出

   ```
   +-------------+-------------+----------+
   | fieldname   | label       | fieldtype |
   +-------------+-------------+----------+
   | new_field_1 | New Field 1 | Data     |
   | new_field_2 | New Field 2 | Int      |
   +-------------+-------------+----------+
   ```

------

## **🔹 方法 5：使用 REST API 查询**

如果你想用 API 确认字段是否导入成功，可以调用：

```bash
curl -X GET "http://your-site.com/api/resource/Custom Field?filters=[[%22dt%22,%22=%22,%22Item%22]]" \
    -H "Authorization: token your-api-key:your-api-secret"
```

或者用 **Python** 访问：

```python
import requests

url = "http://your-site.com/api/resource/Custom Field"
params = {
    "filters": '[["dt", "=", "Item"]]'
}
headers = {
    "Authorization": "token your-api-key:your-api-secret"
}

response = requests.get(url, params=params, headers=headers)
print(response.json())
```

------

## **🔹 总结**

| 方法                   | 适用场景                 | 操作方式                                              |
| ---------------------- | ------------------------ | ----------------------------------------------------- |
| **UI: Customize Form** | 适合手动检查字段是否导入 | 在 Frappe 界面搜索 `"Customize Form"`                 |
| **UI: Custom Field**   | 直接列出所有导入的字段   | 在 Frappe 界面搜索 `"Custom Field"`                   |
| **Frappe Shell**       | 适合开发者快速查询       | `bench --site your-site console`                      |
| **数据库查询**         | 数据库级别检查           | `SELECT * FROM tabCustom Field;`                      |
| **REST API**           | 远程验证字段是否存在     | `curl http://your-site.com/api/resource/Custom Field` |

你想用哪种方式查看？😊
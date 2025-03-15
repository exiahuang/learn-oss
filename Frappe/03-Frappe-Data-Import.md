Frappe 如何批量导入DocType？

[Data Import](https://docs.frappe.io/erpnext/user/manual/en/data-import)





在 Frappe 框架中，批量导入 DocType 数据（如创建多个记录）有几种方法：

### 1. **使用 Data Import Tool**

Frappe 提供了 **Data Import Tool**，可以通过 CSV/Excel 批量导入 DocType 数据。

**步骤：**

1. **进入 Frappe 后台（Desk）**

2. 在“Awesome Bar”（顶部搜索栏）输入 **Data Import** 并进入页面。

3. 选择 **要导入的 DocType**（如 Item, Customer, Sales Invoice 等）。

4. 点击 

   Download Template

   ，选择：

   - “Only Mandatory Fields” （仅必填字段）
   - “All Fields” （所有字段）

5. 在下载的模板中填写数据，并保存为 CSV/Excel。

6. 在 Data Import 页面上传文件并点击 **Start Import**。

------

### 2. **使用 Frappe API**

如果要通过代码批量创建，可以使用 Frappe 的 REST API 或 Python 脚本：

#### 使用 REST API：

```bash
curl -X POST https://your-site.com/api/resource/YourDocType \
    -H "Authorization: token your-api-key:your-api-secret" \
    -H "Content-Type: application/json" \
    -d '{
        "fieldname1": "value1",
        "fieldname2": "value2"
    }'
```

#### 使用 Python 脚本：

```python
import frappe

def bulk_create_records():
    data = [
        {"doctype": "YourDocType", "field1": "value1", "field2": "value2"},
        {"doctype": "YourDocType", "field1": "value3", "field2": "value4"},
    ]

    for record in data:
        doc = frappe.get_doc(record)
        doc.insert()

    frappe.db.commit()  # 提交数据库事务
```

------

### 3. **使用 SQL 直接插入**

如果数据量很大，可以直接使用 SQL 进行批量插入：

```python
import frappe

def bulk_insert_via_sql():
    records = [
        ("value1", "value2"),
        ("value3", "value4"),
    ]
    query = "INSERT INTO `tabYourDocType` (`field1`, `field2`) VALUES (%s, %s)"
    frappe.db.sql(query, records, multi=True)
    frappe.db.commit()
```

⚠️ **注意**：直接使用 SQL 可能会绕过 Frappe 的业务逻辑，谨慎使用。

------

### 4. **使用 Custom Script + Background Job**

如果数据量过大，考虑使用 **Background Job** 处理：

```python
import frappe
from frappe.utils.background_jobs import enqueue

def bulk_create():
    data = [
        {"doctype": "YourDocType", "field1": "value1", "field2": "value2"},
        {"doctype": "YourDocType", "field1": "value3", "field2": "value4"},
    ]
    enqueue(create_records, queue="long", timeout=600, job_name="bulk_create_records", data=data)

def create_records(data):
    for record in data:
        doc = frappe.get_doc(record)
        doc.insert()
    frappe.db.commit()
```

------

### 5. **使用 Bench 命令行**

如果要导入 JSON 数据：

```bash
bench --site your-site execute your_app.module.create_records
```

你需要在 `your_app.module` 里定义 `create_records` 方法来处理导入。

------

## 总结

| 方法             | 适用场景                         | 难度 | 备注             |
| ---------------- | -------------------------------- | ---- | ---------------- |
| Data Import Tool | 适用于非技术用户，Excel/CSV 导入 | 简单 | 推荐             |
| REST API         | 适用于外部系统集成               | 中等 | 需 API 访问权限  |
| Python 脚本      | 适用于开发者                     | 中等 | 适合后台任务     |
| SQL 插入         | 适用于大规模数据导入             | 高   | 可能绕过业务逻辑 |
| Background Job   | 适用于批量任务                   | 高   | 避免超时         |

你更倾向哪种方式？需要更详细的示例吗？😊
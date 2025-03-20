在 Frappe 框架中，`bench data-import --doctype` 命令用于通过命令行批量导入数据到指定的 **DocType**，通常用于自动化数据导入，例如批量创建 **Item**、**Customer** 或 **Custom Field** 等。

------

## **🔹 使用 `bench data-import --doctype` 命令**

### **1. 语法**

```bash
bench --site your-site data-import --doctype "Your DocType" --file /path/to/your_file.csv --submit-after-import
```

📌 **参数说明**：

- `--site your-site`：指定要导入数据的站点（如 `site1.local`）。
- `--doctype "Your DocType"`：要导入的 **DocType**（如 `Item`、`Customer`）。
- `--file /path/to/your_file.csv`：指定要导入的 **CSV 文件路径**。
- `--submit-after-import`：如果 **DocType 支持工作流**，则导入后自动提交数据。

------

### **2. 示例：批量导入 Custom Field**

如果你想要批量为某个 **DocType** 创建自定义字段，可以这样做：

#### **📌 步骤 1：下载 CSV 模板**

```bash
bench --site your-site export-fixtures --doctype "Custom Field"
```

或者在 Frappe UI 中：

1. 进入 **Data Import** 页面（在 "Awesome Bar" 搜索 "Data Import"）。
2. 选择 **Custom Field** 作为 DocType。
3. 点击 **Download Template** 并选择 **With Data**（带现有数据）。

#### **📌 步骤 2：编辑 CSV 文件**

在下载的 CSV 文件中，添加你要创建的自定义字段，例如：

| name        | dt   | fieldname   | label       | fieldtype | insert_after |
| ----------- | ---- | ----------- | ----------- | --------- | ------------ |
| new_field_1 | Item | new_field_1 | New Field 1 | Data      | description  |
| new_field_2 | Item | new_field_2 | New Field 2 | Int       | new_field_1  |

保存为 `custom_fields.csv`。

#### **📌 步骤 3：使用 `bench data-import` 批量导入**

```bash
bench --site your-site data-import --doctype "Custom Field" --file /path/to/custom_fields.csv --submit-after-import
```



```sh
$ bench --site frontend data-import --doctype "Custom Field" --file `pwd`/custom_fields.csv --submit-after-import
Importing Custom Field: 2 records   : [========================================] 100%
```



http://localhost:18888/app/doctype/Custom%20Field

------

### **3. 其他常见场景**

#### **📌 导入 Customer**

```bash
bench --site your-site data-import --doctype "Custo
mer" --file /home/frappe/customers.csv --submit-after-import
```

#### **📌 导入 Item**

```bash
bench --site your-site data-import --doctype "Item" --file /home/frappe/items.csv --submit-after-import
```

------

## **🔹 其他有用的选项**

```bash
bench --site your-site data-import --doctype "Your DocType" --file /path/to/your_file.csv --dry-run
```

📌 **说明**：

- `--dry-run`：测试导入，不实际修改数据库，检查文件格式是否正确。

------

## **🔹 总结**

| 方法                  | 适用场景                   | 执行方式                                                     |
| --------------------- | -------------------------- | ------------------------------------------------------------ |
| **Data Import (UI)**  | 小规模导入，手动操作       | 在 Frappe Admin 界面操作                                     |
| **bench data-import** | 大规模导入，需要命令行操作 | `bench data-import --doctype "Your DocType" --file file.csv` |
| **Python API**        | 需要代码控制               | `frappe.get_doc()` 或 `frappe.insert_many()`                 |

如果你希望 **自动化批量导入**，`bench data-import` 是个不错的选择。如果你想手动操作，可以用 **Data Import Tool**。

你想导入哪个 DocType？😊
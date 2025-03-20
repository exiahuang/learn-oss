import pandas as pd
import json
import os


def dump_dt(excel_file):
    name = os.path.basename(excel_file).split(".")[0]
    print(f"File: {name}\n")
    sheets_dict = pd.read_excel(excel_file, sheet_name=None)

    # 遍历所有 Sheets 并转换为 JSON
    for sheet_name, df_sheet in sheets_dict.items():
        json_data = df_sheet.to_json(orient="records", force_ascii=False)
        print(f"Sheet: {sheet_name}\n")

        arr = []
        for item in json.loads(json_data):
            i = [v for v in item.values()]
            field = {"label": i[0], "fieldname": i[1], "fieldtype": i[2]}
            if i[3] is not None and i[3] != 0:
                field["length"] = i[3]
            arr.append(field)
        print(arr)
        dt = [{
            "name": name,
            "module": "dev",
            "fields": arr
        }]
        pretty_json = json.dumps(dt, indent=4, ensure_ascii=False)
        print(pretty_json)
        output_file = file.replace(".xlsx", "_" + sheet_name + ".json")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(pretty_json)

# 读取所有 Sheets
file = "Book__c.xlsx"
dump_dt(file)
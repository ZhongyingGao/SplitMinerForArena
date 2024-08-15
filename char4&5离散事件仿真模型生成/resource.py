import pandas as pd
import json

def final_to_json(json_file_path,excel_file_path):
    # 读取Excel文件
    excel_data = pd.read_excel(excel_file_path)

    # 将Excel数据转换为字典，使用'Name'作为键
    excel_dict = excel_data.set_index('Name').to_dict(orient='index')

    # 读取现有的JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    # 更新JSON数据
    for node_id, node_data in json_data.items():
        name = node_data.get('name')
        if name in excel_dict:
            node_data.update(excel_dict[name])

    # 将更新后的数据写回JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    print("JSON文件已更新。")
    return json_file_path

# excel_file_path = r'D:\BPMN2Arena\output\20240603_135943\activity_fitting_results_with_resources.xlsx'
# json_file_path = r'D:\BPMN2Arena\output\20240603_135943\output_20240603_135943_light_trans_final.json'
# final_to_json(json_file_path,excel_file_path)
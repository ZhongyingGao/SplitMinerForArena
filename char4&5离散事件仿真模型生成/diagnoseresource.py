import os
import re

def extract_utilization(file_path):
    utilization_data = {}

    with open(file_path, 'r') as file:
        content = file.read()

    # Use regex to find all utilization data for resources
    pattern = re.compile(r'Resource (\d+)\.Utilization\s+([\d.]+)')
    matches = pattern.findall(content)

    for match in matches:
        resource_id, utilization = match
        utilization_data[f'Resource {resource_id}'] = float(utilization)

    return utilization_data

def format_utilization(utilization_data):
    result = "资源使用情况:\n"
    result += "\n高利用率资源 (over 0.75):\n"
    for resource, utilization in utilization_data.items():
        if utilization > 0.75:
            result += f'{resource}: {utilization}\n'
    result += "\n低利用率资源 (below 0.25):\n"
    for resource, utilization in utilization_data.items():
        if utilization < 0.25:
            result += f'{resource}: {utilization}\n'
    result += "资源利用率:\n"
    for resource, utilization in utilization_data.items():
        result += f'{resource}: {utilization}\n'
    return result

def process_file(file_path):
    folder_path = os.path.dirname(file_path)
    out_file_path = os.path.join(folder_path, 'Model1.out')
    if os.path.exists(out_file_path):
        utilization_data = extract_utilization(out_file_path)
        return format_utilization(utilization_data)
    else:
        return f"文件 {out_file_path} 不存在"

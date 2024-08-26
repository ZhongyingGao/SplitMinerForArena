import os
import json
import subprocess

def generate_vbs(json_file_path):
    # 读取JSON数据
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # 创建一个空的列表，用于存储生成的VBS脚本行
    vbs_lines = []
    # 定义 px 和 py 的循环值
    px_values = [1400, 2100, 2800, 3500]
    py_values = [700, 1400, 2100]

    px_index = 0
    py_index = 0

    def get_next_coordinates():
        nonlocal px_index, py_index
        px = px_values[px_index]
        py = py_values[py_index]
        px_index = (px_index + 1) % len(px_values)
        if px_index == 0:
            py_index = (py_index + 1) % len(py_values)
        return px, py

    # 定义一个函数来递归遍历节点并生成VBS语句
    def process_node(node_id):
        if node_id not in data:
            print(f"Node ID {node_id} not found in data.")
            return

        node_info = data[node_id]
        module = node_info.get("module", "")
        name = node_info.get("name", "")
        resource = node_info.get("Resource Name(1)", "DefaultResource")
        expression = node_info.get("Expression", "")
        px, py = get_next_coordinates()

        print(f"Processing node {node_id} with module {module}")

        if module == "startEvent":
            vbs_lines.append(f'Set Process = Model.Modules.Create("BasicProcess", "Create", {px}, {py})')
            vbs_lines.append(f'Process.Data("Units") = "Minutes"')
            vbs_lines.append(f'Process.Data("Value") = "8"')
        elif module == "endEvent":
            vbs_lines.append(f'Model.Modules.Create "BasicProcess", "Dispose", {px}, {py}')
        elif module == "task":
            vbs_lines.append(f'Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)')
            vbs_lines.append(f'Process.Data("Name") = "Resource {resource}"')
            vbs_lines.append(f'Set Process = Model.Modules.Create("BasicProcess", "Process", {px}, {py})')
            vbs_lines.append(f'Process.Data("Name") = "{name}"')
            vbs_lines.append(f'Process.Data("Units") = "Seconds"')
            vbs_lines.append(f'Process.Data("Action") = "Seize Delay Release"')
            vbs_lines.append(f'Process.Data("DelayType") = "Expression"')
            vbs_lines.append(f'Process.Data("Resource Type(1)") = "Resource"')
            vbs_lines.append(f'Process.Data("Resource Name(1)") = "Resource {resource}"')
            vbs_lines.append(f'Process.Data("Expression") = "{expression}"')
            vbs_lines.append(f'Process.Shape.Selected = True')
        # 递归处理目标节点
        target_ref = node_info.get("targetRef")
        if target_ref:
            process_node(target_ref)

    # 找到startEvent节点并开始处理
    start_node_found = False
    for node_id, node_info in data.items():
        if node_info.get("module") == "startEvent":
            start_node_found = True
            process_node(node_id)
            break

    if not start_node_found:
        print("No startEvent node found.")

    # 生成VBS文件
    vbs_file_path = os.path.splitext(json_file_path)[0] + '.vbs'
    output_directory = os.path.dirname(json_file_path)
    output_doe_file = os.path.join(output_directory, "Model1.doe")

    with open(vbs_file_path, 'w') as vbs_file:
        vbs_file.write('set app = createobject("arena.application")\n')
        vbs_file.write('app.visible=true\n')
        vbs_file.write('set Model=app.models.add()\n')
        for line in vbs_lines:
            vbs_file.write(line + '\n')
        vbs_file.write('Model.ReplicationLength = 32\n')
        vbs_file.write('Model.DisableRandomness = "False"\n')
        vbs_file.write(f'Model.SaveAs "{output_doe_file}"\n')
        vbs_file.write('Model.BatchMode = True\n')
        vbs_file.write('Model.DisableRandomness = "False"\n')
        vbs_file.write('Model.DisplayDefaultReport = smAlwaysDisplay\n')
        vbs_file.write('Model.DefaultReport = "SIMAN Summary Report(.out file)"\n')
        vbs_file.write('Model.DisableReportDatabase = True\n')
        vbs_file.write('Model.GO\n')
        vbs_file.write('Model.Save\n')
        vbs_file.write('app.quit\n')

    print(f"VBS script saved to: {vbs_file_path}")
    subprocess.run(['cscript', vbs_file_path], check=True)
    return vbs_file_path


# 测试函数
# json_file_path = r"D:\BPMN2Arena\output\20240522_093812\output_20240522_093812_light_trans_final.json"
# generate_vbs(json_file_path)

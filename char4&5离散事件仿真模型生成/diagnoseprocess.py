import json

def check_process_sequence(file_path):
    # 读取 JSON 文件
    expected_sequence = ['startEvent', 'Mould', 'Assemble', 'Blend', 'Debubble', 'Grout', 'Fitting', 'Pouring', 'Clean',
                         'Cut', 'Polish', 'endEvent']
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 构建流程图
    def build_process_flow(data):
        flow = {}
        for node_id, node_info in data.items():
            source = node_info.get('sourceRef')
            target = node_info.get('targetRef')
            if source:
                if source not in flow:
                    flow[source] = []
                flow[source].append(node_id)
        return flow

    # 获取有序流程节点名称列表
    def get_ordered_process_names(flow, data, start_node):
        ordered_names = []

        def recursive_collect(node):
            node_name = data[node]['name'] if data[node]['name'] else data[node]['module']
            ordered_names.append(node_name)
            if node in flow:
                for target in flow[node]:
                    recursive_collect(target)

        recursive_collect(start_node)
        return ordered_names

    # 找到开始节点
    start_node = None
    for node_id, node_info in data.items():
        if node_info['module'] == 'startEvent':
            start_node = node_id
            break

    # 构建并获取有序流程节点名称列表
    if start_node:
        process_flow = build_process_flow(data)
        ordered_names = get_ordered_process_names(process_flow, data, start_node)
        result = "流程节点：\n" + str(ordered_names) + "\n"

        # 检查是否与预期顺序一致
        if ordered_names == expected_sequence:
            result += "流程顺序与预期一致。\n"
        else:
            result += "流程顺序与预期不一致。\n"
    else:
        result = "未找到开始节点\n"

    return result

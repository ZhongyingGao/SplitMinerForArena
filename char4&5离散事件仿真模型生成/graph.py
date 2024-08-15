import os
import json
from graphviz import Digraph

def generate_graph(json_file_path):
    # 读取JSON数据
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # 创建有向图
    dot = Digraph()

    # 用集合记录已经添加的边，以避免重复
    added_edges = set()

    # 添加节点和边
    for node_id, node_info in data.items():
        label = f"{node_info['module']} - {node_info['name']} "  # 节点标签包括模块和ID属性
        dot.node(node_id, label=label)
        target_ref = node_info["targetRef"]
        source_ref = node_info["sourceRef"]
        if target_ref and target_ref in data and (node_id, target_ref) not in added_edges:
            dot.edge(node_id, target_ref)
            added_edges.add((node_id, target_ref))
        if source_ref and source_ref in data and (source_ref, node_id) not in added_edges:
            dot.edge(source_ref, node_id)
            added_edges.add((source_ref, node_id))

    # 根据模块类型给节点着色
    node_colors = {
        "startEvent": "green",
        "endEvent": "red",
        "task": "blue",
        "decide": "yellow"
    }
    for node_id, node_info in data.items():
        module = node_info["module"]
        if module in node_colors:
            dot.node(node_id, color=node_colors[module])

    # 从JSON文件路径中提取文件夹路径
    output_directory = os.path.dirname(json_file_path)

    # 保存图形到文件夹路径下，并指定文件名为 "graph.png"
    output_file_path = os.path.join(output_directory, 'graph')
    dot.render(output_file_path, format='png', cleanup=True)

    print(f"Graph saved to: {output_file_path}")

    return output_file_path
# 测试函数
# json_file_path = r"D:\BPMN2Arena\output\20240304_190514\output_20240304_190514_light_trans_final.json"
# generate_graph(json_file_path)

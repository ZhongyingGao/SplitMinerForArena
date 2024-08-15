import xml.etree.ElementTree as ET
from datetime import datetime
import os

def process_sequence_flows(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # 用于存储节点的 sourceRef 和 targetRef 映射关系
    node_mapping = {}

    # 遍历所有序列流
    for sequenceFlow in root.findall(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"):
        sourceRef = sequenceFlow.get('sourceRef')
        targetRef = sequenceFlow.get('targetRef')

        # 获取源节点和目标节点
        sourceNode = root.find(".//*[@id='" + sourceRef + "']")
        targetNode = root.find(".//*[@id='" + targetRef + "']")

        # 将目标节点赋值给源节点的 targetRef 属性
        if sourceNode is not None:
            existing_target_refs = sourceNode.get('targetRef')
            if existing_target_refs:
                existing_target_refs_list = existing_target_refs.split(',')
            else:
                existing_target_refs_list = []
            if targetRef not in existing_target_refs_list:
                existing_target_refs_list.append(targetRef)
                sourceNode.set('targetRef', ','.join(existing_target_refs_list))
        else:
            raise ValueError("Source node with ID {} not found.".format(sourceRef))

        # 将源节点赋值给目标节点的 sourceRef 属性
        if targetNode is not None:
            existing_source_refs = targetNode.get('sourceRef')
            if existing_source_refs:
                existing_source_refs_list = existing_source_refs.split(',')
            else:
                existing_source_refs_list = []
            if sourceRef not in existing_source_refs_list:
                existing_source_refs_list.append(sourceRef)
                targetNode.set('sourceRef', ','.join(existing_source_refs_list))
        else:
            raise ValueError("Target node with ID {} not found.".format(targetRef))

    # 生成输出文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_directory = rf"D:\BPMN2Arena\output\{timestamp}"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = f"{output_directory}\\output_{timestamp}.xml"

    # 写入输出文件
    tree.write(output_file)
    print("Output file:", output_file)

    # 将processSimulationInfo的内容单独输出到另一个文件
    process_simulation_info = root.find(".//{http://www.qbp-simulator.com/Schema201212}processSimulationInfo")
    if process_simulation_info is not None:
        process_simulation_info_output_file = f"{output_directory}\\process_simulation_info_{timestamp}.xml"
        process_simulation_info_tree = ET.ElementTree(process_simulation_info)
        process_simulation_info_tree.write(process_simulation_info_output_file)
        print("Process Simulation Info output file:", process_simulation_info_output_file)
    else:
        print("Process Simulation Info not found in the input file.")

    return output_file  # 返回生成的输出文件路径

# 示例用法
# input_file = r"C:\Users\123\Desktop\Simod-2.0.0\outputs\\20240218_081312561471\ConsultaDataMining201618.bpmn"
# process_sequence_flows(input_file)

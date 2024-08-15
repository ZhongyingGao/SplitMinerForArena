import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os


def prettify(elem):
    """将 ElementTree 对象转换为格式良好的字符串"""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def extract_elements_with_attributes(input_xml_file):
    tree = ET.parse(input_xml_file)
    root = tree.getroot()

    # 创建新的根节点
    new_root = ET.Element(root.tag, attrib=root.attrib)

    # 寻找并提取开始事件、结束事件、网关和任务
    for element in root.findall(".//*[@id]"):
        element_tag = element.tag.split("}")[1]  # 获取标签名，去除命名空间
        if element_tag in ["startEvent", "endEvent", "exclusiveGateway", "parallelGateway", "inclusiveGateway", "task"]:
            new_element = ET.SubElement(new_root, element_tag, attrib=element.attrib)
            for child in element:
                new_child = ET.SubElement(new_element, child.tag, attrib=child.attrib)
                new_child.text = child.text

    # 使用 XPath 表达式寻找 processSimulationInfo 元素及其子元素
    process_simulation_info = root.find(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}processSimulationInfo")
    if process_simulation_info is not None:
        new_process_simulation_info = ET.SubElement(new_root, process_simulation_info.tag, attrib=process_simulation_info.attrib)
        for child in process_simulation_info:
            new_child = ET.SubElement(new_process_simulation_info, child.tag, attrib=child.attrib)
            new_child.text = child.text

    # 创建新的 XML 文件并保存
    output_directory = os.path.dirname(input_xml_file)
    input_file_name = os.path.basename(input_xml_file)
    filename = os.path.splitext(input_file_name)[0]
    output_xml_file = f"{output_directory}\\{filename}_light.xml"
    os.makedirs(output_directory, exist_ok=True)
    xml_content = prettify(new_root)
    with open(output_xml_file, "w") as f:
        f.write(xml_content)
    print(f"New output XML file saved: {output_xml_file}")
    return output_xml_file




# 示例用法
# input_xml_file = r"D:\BPMN2Arena\output\20240301_110623\output_20240301_110623.xml"
# input_xml_file = r"C:\Users\123\Desktop\Simod-2.0.0\outputs\\20240218_081312561471\ConsultaDataMining201618.bpmn"
#
# extract_elements_with_attributes(input_xml_file)

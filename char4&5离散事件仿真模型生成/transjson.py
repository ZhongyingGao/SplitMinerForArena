import xml.etree.ElementTree as ET
import json
import os


def xml_to_json(input_xml_file):
    """
    将 XML 文件转换为 JSON 格式

    Args:
        input_xml_file (str): XML 文件路径

    Returns:
        str: JSON 格式的字符串
    """
    try:
        # 解析 XML 文件
        tree = ET.parse(input_xml_file)
        root = tree.getroot()

        # 创建一个空字典来存储属性
        elements_dict = {}

        # 遍历每个元素
        for elem in root:
            # 检查元素是否有属性
            if elem.attrib:
                # 创建一个字典来存储元素的属性
                elem_info = {
                    'id': elem.attrib.get('id', ''),
                    'module': elem.tag,
                    'name': elem.attrib.get('name', ''),
                    'currency': elem.attrib.get('currency', ''),
                    'targetRef': elem.attrib.get('targetRef', ''),
                    'sourceRef': elem.attrib.get('sourceRef', ''),
                    'gatewayDirection': elem.attrib.get('gatewayDirection', ''),
                }

                # 使用元素的 id 作为主键
                elements_dict[elem.attrib['id']] = elem_info

        json_content = json.dumps(elements_dict, indent=4)

        # 创建新的 JSON 文件并保存
        output_directory = os.path.dirname(input_xml_file)
        input_file_name = os.path.basename(input_xml_file)
        filename = os.path.splitext(input_file_name)[0]
        output_json_file = os.path.join(output_directory, f"{filename}_trans.json")

        with open(output_json_file, "w") as f:
            f.write(json_content)

        print(f"New output JSON file saved: {output_json_file}")

        return output_json_file

    except FileNotFoundError:
        print("文件不存在，请检查文件路径是否正确。")
        return None
    except ET.ParseError:
        print("XML 文件格式错误，请检查文件内容是否符合 XML 规范。")
        return None

# # XML 文件路径
# input_xml_file = r'D:\BPMN2Arena\output\20240515_134801\output_20240515_134801.xml_light.xml'
#
# # 将 XML 属性转换为 JSON
# result_file = xml_to_json(input_xml_file)
#
# if result_file:
#     print("JSON 文件已生成:", result_file)

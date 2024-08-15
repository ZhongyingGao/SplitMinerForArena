import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
from datetime import datetime, timedelta

def transxml():
    # 读取Excel文件
    df = pd.read_excel(r'C:\Users\123\Documents\mould\output\EventLog.xlsx')

    # 创建根节点和根元素，命名空间为None
    root = ET.Element('log', attrib={'xes.version': '2.0', 'xes.features': 'nested-attributes'})

    # 创建元素工具函数
    def create_element(parent, tag, text=None, attributes=None):
        element = ET.SubElement(parent, tag)
        if text:
            element.set('value', str(text))
        if attributes:
            for key, value in attributes.items():
                element.set(key, str(value))
        return element

    # 创建字典用于存储trace
    trace_dict = {}

    # 创建Event元素
    for index, row in df.iterrows():
        case_id = str(row['CaseID'])
        activity = str(row['Activity'])
        resource = str(row['Resource'])
        start_time_str = str(row['StartTime'])  # Assuming 'StartTime' is a string in '%Y-%m-%d %H:%M:%S' format
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        start_time_iso = start_time.strftime('%Y-%m-%dT%H:%M:%S.000-05:00')  # Convert to ISO format

        end_time_str = str(row['EndTime'])  # Assuming 'EndTime' is also in '%Y-%m-%d %H:%M:%S' format
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

        # 如果该case_id的trace已存在，则添加event到该trace中
        if case_id in trace_dict:
            trace = trace_dict[case_id]
        else:
            trace = ET.SubElement(root, 'trace')
            create_element(trace, 'string', text=case_id, attributes={'key': 'concept:name'})
            create_element(trace, 'string', text='Fluxicon Disco', attributes={'key': 'creator'})
            trace_dict[case_id] = trace

        event = ET.SubElement(trace, 'event')
        create_element(event, 'string', text=activity, attributes={'key': 'concept:name'})
        create_element(event, 'string', text='start', attributes={'key': 'lifecycle:start'})
        create_element(event, 'string', text=resource, attributes={'key': 'org:resource'})
        create_element(event, 'date', text=start_time_iso, attributes={'key': 'time:timestamp'})  # Use ISO format
        create_element(event, 'string', text=activity, attributes={'key': 'Activity'})
        create_element(event, 'string', text=resource, attributes={'key': 'Resource'})

    # 创建XML文档对象
    tree = ET.ElementTree(root)
    xmlstr = ET.tostring(root, encoding='utf-8', xml_declaration=True)

    # 使用minidom解析XML字符串，添加换行和缩进
    xml_dom = minidom.parseString(xmlstr)
    pretty_xml = xml_dom.toprettyxml(indent="    ")

    # 写入XML文件
    with open(r'C:\Users\123\Documents\mould\output\EventLog.xes', 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

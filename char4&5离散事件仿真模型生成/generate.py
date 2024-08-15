import json
import os

def process_gateway(input_json_file):
    """
    处理网关相关操作，更新 JSON 文件中的数据

    Args:
        input_json_file (str): 输入的 JSON 文件路径

    Returns:
        None
    """
    # 读取 JSON 文件
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    # 需要移除的网关 ID 列表
    gateways_to_remove = []
    # 处理 JSON 数据
    for key, value in data.items():
        if 'gatewayDirection' in value:
            gateway_direction = value['gatewayDirection']
            # 检查是否为网关
            if value['module'] in ['parallelGateway', 'exclusiveGateway', 'inclusiveGateway']:
                source_refs = value['sourceRef'].split(',')
                target_refs = value['targetRef'].split(',')

                # 检查连接的节点是否与当前网关的 'gatewayDirection' 相同，如果相同则修改网关的 module 属性
                # if all(data[source_ref].get('gatewayDirection') == gateway_direction and data[target_ref].get('gatewayDirection') == gateway_direction for source_ref in source_refs for target_ref in target_refs):
                if value['module'] == 'parallelGateway':
                    if gateway_direction == 'Diverging':
                        # 修改 module 属性为 separate
                        value['module'] = 'separate'
                    elif gateway_direction == 'Converging':
                        # 修改 module 属性为 batch
                        value['module'] = 'batch'
                elif value['module'] == 'exclusiveGateway':
                    value['module'] = 'decide'
                    # continue

            # 执行流程并删除
            if value['module'] == 'parallelGateway':
                if gateway_direction == 'Diverging':
                    # 找到对应的 sourceRef
                    source_refs = value['sourceRef'].split(',')
                    for source_ref in source_refs:
                        if source_ref in data:
                            # 修改 module 和 targetRef 属性
                            data[source_ref]['module'] = 'separate'
                            data[source_ref]['targetRef'] = value['targetRef']

                            # 更新连接到该节点的 targetRef 节点的 sourceRef
                            target_refs = value['targetRef'].split(',')
                            for target_ref in target_refs:
                                if target_ref in data:
                                    data[target_ref]['sourceRef'] = source_ref

                    # 将当前网关 ID 添加到需要移除的列表中
                    gateways_to_remove.append(key)

                elif gateway_direction == 'Converging':
                    # 找到对应的 targetRef
                    target_ref = value['targetRef']
                    if target_ref in data:
                        # 修改 module 和 sourceRef 属性
                        data[target_ref]['module'] = 'batch'
                        data[target_ref]['sourceRef'] = value['sourceRef']

                        # 更新连接到该节点的 sourceRef 节点的 targetRef
                        source_refs = value['sourceRef'].split(',')
                        for source_ref in source_refs:
                            if source_ref in data:
                                data[source_ref]['targetRef'] = target_ref

                    # 将当前网关 ID 添加到需要移除的列表中
                    gateways_to_remove.append(key)

            elif value['module'] == 'exclusiveGateway':
                if gateway_direction == 'Converging':
                    # 找到对应的 sourceRef
                    source_ref = value['sourceRef'].split(',')
                    for source_ref in source_ref:
                        if source_ref in data:
                            # 修改 targetRef 属性
                            data[source_ref]['targetRef'] = value['targetRef']

                    # 找到对应的 targetRef
                    target_refs = value['targetRef'].split(',')
                    for target_ref in target_refs:
                        if target_ref in data:
                            # 修改目标的 sourceRef
                            data[target_ref]['sourceRef'] = value['sourceRef']
                    # 将当前网关 ID 添加到需要移除的列表中
                    gateways_to_remove.append(key)

            elif value['module'] == 'inclusiveGateway':
                # 找到对应的 sourceRef
                source_ref = value['sourceRef'].split(',')
                for source_ref in source_ref:
                    if source_ref in data:
                        # 修改 targetRef 属性
                        data[source_ref]['targetRef'] = value['targetRef']

                # 找到对应的 targetRef
                target_refs = value['targetRef'].split(',')
                for target_ref in target_refs:
                    if target_ref in data:
                        # 修改目标的 sourceRef
                        data[target_ref]['sourceRef'] = value['sourceRef']
                # 将当前网关 ID 添加到需要移除的列表中
                gateways_to_remove.append(key)

    # 从数据中移除网关及其相关的条目
    for gateway_id in gateways_to_remove:
        del data[gateway_id]

    # 创建新的 JSON 文件并保存
    output_directory = os.path.dirname(input_json_file)
    input_file_name = os.path.basename(input_json_file)
    filename = os.path.splitext(input_file_name)[0]
    output_json_file = os.path.join(output_directory, f"{filename}_final.json")
    os.makedirs(output_directory, exist_ok=True)

    # 写入新的 JSON 文件
    with open(output_json_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"New output JSON file saved: {output_json_file}")
    return output_json_file
# 测试代码
# input_json_file = r'D:\BPMN2Arena\output\20240304_162729\output_20240304_162729_light_trans.json'
# process_gateway(input_json_file)

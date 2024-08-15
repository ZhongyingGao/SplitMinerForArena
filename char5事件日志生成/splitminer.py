import subprocess

def miner():
    # 定义JAR文件的路径
    jar_path = 'external_tools/splitminer/splitminer.jar'

    # 定义其他参数，例如epsilon和eta
    epsilon = 0.8
    eta = 0.8
    input_log_path = r'C:\Users\123\Documents\mould\output\EventLog.xes'
    output_base_path = r'C:\Users\123\Documents\mould\output\EventLog'

    # 构建命令行参数列表
    args = ['java', '-jar', jar_path, str(epsilon), str(eta), input_log_path, output_base_path]

    # 使用subprocess.call()执行命令
    try:
        subprocess.call(args)
    except Exception as e:
        print(f"Error occurred while running splitminer: {e}")
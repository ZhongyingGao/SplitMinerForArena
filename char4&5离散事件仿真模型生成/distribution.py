import pandas as pd
from scipy.stats import norm, uniform, triang, expon, poisson
import numpy as np
import os

def fit_activity_durations(bpmn_file, result_file):
    # 读取Excel文件
    input_folder = os.path.dirname(bpmn_file)
    input_file = os.path.join(input_folder, 'EventLog.xlsx')
    output_folder = os.path.dirname(result_file)
    df = pd.read_excel(input_file)

    # 初始化结果列表
    results = []

    # 对每个活动进行拟合
    for activity in df['Activity'].unique():
        # 提取该活动的数据
        activity_data = df[df['Activity'] == activity]
        duration = activity_data['Duration (s)'].values
        resources = activity_data['Resource'].values

        # 初始化变量来记录最好的拟合结果
        best_model = None
        best_score = float('inf')

        # 尝试拟合normal分布
        try:
            mu, std = norm.fit(duration)
            norm_score = ((duration - mu) / std) ** 2
            norm_score = norm_score.mean()
            if norm_score < best_score:
                best_score = norm_score
                best_model = f"NORM({mu},{std})"
        except Exception as e:
            print(f"Failed to fit Normal Distribution for activity {activity}: {e}")

        # 尝试拟合constant分布
        try:
            constant_value = duration.mean()
            constant_score = ((duration - constant_value) ** 2).mean()
            if constant_score < best_score:
                best_score = constant_score
                best_model = f"{constant_value}"
        except Exception as e:
            print(f"Failed to fit Constant Distribution for activity {activity}: {e}")

        # # 尝试拟合triangular分布
        # try:
        #     c, loc, scale = triang.fit(duration)
        #     triangular_score = ((duration - loc) ** 2).mean()
        #     if triangular_score < best_score:
        #         best_score = triangular_score
        #         best_model = f"TRIA({loc},{c},{loc + scale})"
        # except Exception as e:
        #     print(f"Failed to fit Triangular Distribution for activity {activity}: {e}")

        # 尝试拟合uniform分布
        try:
            low = duration.min()
            high = duration.max()
            uniform_score = ((duration - low) / (high - low)) ** 2
            uniform_score = uniform_score.mean()
            if uniform_score < best_score:
                best_score = uniform_score
                best_model = f"UNIF({low},{high})"
        except Exception as e:
            print(f"Failed to fit Uniform Distribution for activity {activity}: {e}")

        # 尝试拟合指数分布
        try:
            loc, scale = expon.fit(duration)
            exp_score = ((duration - loc) / scale) ** 2
            exp_score = exp_score.mean()
            if exp_score < best_score:
                best_score = exp_score
                best_model = f"EXPO({loc})"
        except Exception as e:
            print(f"Failed to fit Exponential Distribution for activity {activity}: {e}")

        # # 尝试拟合泊松分布
        # try:
        #     mu = duration.mean()  # 计算均值作为泊松分布的参数
        #     pois_score = ((duration - mu) / mu) ** 2
        #     pois_score = pois_score.mean()
        #     if pois_score < best_score:
        #         best_score = pois_score
        #         best_model = f"POIS({mu})"
        # except Exception as e:
        #     print(f"Failed to fit Poisson Distribution for activity {activity}: {e}")

        # 将结果添加到结果列表中
        resources_str = ','.join(map(str, np.unique(resources)))  # 将资源值拼接成字符串
        results.append({'Name': activity, 'Expression': best_model, 'Resource Name(1)': resources_str})

    # 创建DataFrame
    results_df = pd.DataFrame(results)

    # 将结果DataFrame导出为Excel文件
    output_file = os.path.join(output_folder, 'activity_fitting_results_with_resources.xlsx')
    results_df.to_excel(output_file, index=False)
    return output_file
# 示例调用
# bpmn_file = r'C:\Users\123\Documents\mould\output\EventLog.bpmn'
# result_file = r'D:\BPMN2Arena\output\20240603_132223\output_20240603_132223.xml'
# fit_activity_durations(bpmn_file, result_file)

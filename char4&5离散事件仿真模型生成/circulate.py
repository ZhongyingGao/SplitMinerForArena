import pandas as pd

# 读取Excel文件
df = pd.read_excel(r'C:\Users\123\Documents\mould\output\EventLog.xlsx')

# 按案例ID和活动名称对数据进行分组，并计算每个组中活动的数量
activity_counts = df.groupby(['CaseID', 'Activity']).size().reset_index(name='Count')

# 计算每个活动的平均执行次数
average_counts = activity_counts.groupby('Activity')['Count'].mean()

# 输出结果
print("Average Execution Counts for Each Activity:")
print(average_counts)

import pandas as pd
from scipy.stats import poisson
from scipy.optimize import curve_fit

# 从 Excel 文件中读取事件日志数据
file_path = r'C:\Users\123\Documents\mould\output\EventLog.xlsx'
df = pd.read_excel(file_path)

# 提取 Mould 活动的数据
mould_data = df[df['Activity'] == 'Mould']

# 转换 StartTime 为小时
mould_data['StartTime'] = pd.to_datetime(mould_data['StartTime'])
mould_data['StartTime_hours'] = (mould_data['StartTime'] - mould_data['StartTime'].min()).dt.total_seconds() / 3600

# 计算到达函数（到达次数随时间的变化）
arrival_counts = mould_data.groupby('StartTime_hours').size()

# 定义泊松分布拟合函数
def poisson_fit(x, lambda_param):
    return poisson.pmf(x, lambda_param)

# 初始猜测的参数值
initial_guess = [8]

# 使用 curve_fit 进行拟合
popt, pcov = curve_fit(poisson_fit, arrival_counts.index, arrival_counts.values, p0=initial_guess)

# 输出拟合后的参数值
print(f"Fitted Lambda Parameter: {popt[0]}")

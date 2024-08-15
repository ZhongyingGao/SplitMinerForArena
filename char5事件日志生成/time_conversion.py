import pandas as pd
from datetime import datetime, timedelta

def convert_time(df):
    start_time = datetime(2024, 5, 1, 0, 0, 0)  # 初始时间

    # 转换StartTime列为日期格式
    df['StartTime'] = df['StartTime'].apply(lambda x: start_time + timedelta(minutes=x))
    df['StartTime'] = df['StartTime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # 转换EndTime列为日期格式
    df['EndTime'] = df['EndTime'].apply(lambda x: start_time + timedelta(minutes=x))
    df['EndTime'] = df['EndTime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return df

import pandas as pd
import os
import re
from time_conversion import convert_time

def genaratelog():
    # 第一部分：处理TXT文件并合并为Excel
    directory = r'C:\Users\123\Documents\mould\output\txt'
    txt_files = [file for file in os.listdir(directory) if file.endswith('.txt')]
    skiprows = 5
    merged_data = {}
    output_paths = {}

    for file in txt_files:
        match = re.match(r'([A-Za-z]+)(\d+)\.txt', file)
        if match:
            prefix = match.group(1)
            suffix = int(match.group(2))
            if prefix not in merged_data:
                merged_data[prefix] = {1: None, 2: None, 3: None}
                output_dir = os.path.join(directory, 'excel')
                os.makedirs(output_dir, exist_ok=True)
                output_paths[prefix] = os.path.join(output_dir, f'{prefix}_data_combined.xlsx')
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path, skiprows=skiprows, index_col=False)
            merged_data[prefix][suffix] = df

    for prefix, data_dict in merged_data.items():
        merged_df = pd.concat(data_dict.values(), axis=1)
        merged_df['event'] = prefix
        merged_df.to_excel(output_paths[prefix], index=False)
        print(f'Data from {prefix} files merged and saved to {output_paths[prefix]}')

    # 第二部分：合并所有data_combined.xlsx文件为All.xlsx
    excel_subdirectory = os.path.join(directory, 'excel')
    xlsx_files = [os.path.join(excel_subdirectory, file) for file in os.listdir(excel_subdirectory) if file.endswith('data_combined.xlsx')]
    df_all = pd.DataFrame()
    for file in xlsx_files:
        df = pd.read_excel(file)
        df_all = pd.concat([df_all, df])
    df_all.to_excel(os.path.join(excel_subdirectory, "All.xlsx"), index=False)

    # 第三部分：读取All.xlsx，处理数据，并写入新的EventLog.xlsx
    input_file = os.path.join(excel_subdirectory, "All.xlsx")
    df_all = pd.read_excel(input_file)
    df_all.rename(columns={df_all.columns[1]: 'StartTime', df_all.columns[0]: 'EndTime', df_all.columns[3]: 'CaseID', df_all.columns[6]: 'Activity', df_all.columns[5]: 'Resource'}, inplace=True)
    df_filtered = df_all[df_all['CaseID'] != -1].copy()
    df_finish = convert_time(df_filtered)
    df_finish['Duration (s)'] = (pd.to_datetime(df_finish['EndTime']) - pd.to_datetime(df_finish['StartTime'])).dt.total_seconds()
    df_finish = df_finish[['CaseID', 'Activity', 'StartTime', 'EndTime', 'Duration (s)', 'Resource']]
    df_finish = df_finish.sort_values(by='StartTime')
    output_file = r'C:\Users\123\Documents\mould\output\EventLog.xlsx'
    df_finish.to_excel(output_file, index=False)
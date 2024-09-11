import os
import pandas as pd
from sqlalchemy import create_engine
import py7zr
from tqdm import tqdm

# 创建数据库引擎，假设使用MySQL数据库
engine = create_engine('mysql+pymysql://user:password@localhost/tv_programs_db')

# 定义包含压缩包的目录路径
base_dir = './cctv'
# 获取所有7z文件的列表
archive_files = [f for f in os.listdir(base_dir) if f.endswith('.7z')]

# 处理每个压缩包
for archive_filename in tqdm(archive_files, desc='Processing Archives'):
    file_path = os.path.join(base_dir, archive_filename)
    extract_dir = os.path.join(base_dir, os.path.splitext(archive_filename)[0])

    # 解压缩文件
    with py7zr.SevenZipFile(file_path, mode='r') as archive:
        archive.extractall(path=extract_dir)

    # 获取解压缩后的CSV文件列表
    csv_files = [f for f in os.listdir(extract_dir) if f.endswith('.csv')]

    # 处理每个CSV文件
    for csv_filename in tqdm(csv_files, desc=f'Processing CSVs in {archive_filename}', leave=False):
        csv_file_path = os.path.join(extract_dir, csv_filename)

        # 读取CSV文件
        df = pd.read_csv(csv_file_path)

        # 检查并添加缺失的列
        if 'Channel_Name' not in df.columns:
            df['Channel_Name'] = None
        if 'Duration' not in df.columns:
            df['Duration'] = None

        # 统一列名
        # 确保列名与目标一致
        columns = ['Date', 'Channel_ID', 'Channel_Name', 'Time', 'Program', 'Duration']

        # 创建一个空的DataFrame，按照目标列顺序排列
        df_final = pd.DataFrame(columns=columns)

        # 重新排列列并填充缺失的列
        for col in columns:
            if col in df.columns:
                df_final[col] = df[col]
            else:
                df_final[col] = None

        # 将Date列转换为标准日期格式
        df_final['Date'] = pd.to_datetime(df_final['Date'], format='%Y%m%d', errors='coerce')


        # 将Time列转换为标准时间格式
        def parse_time(time_str):
            try:
                # 确保输入为字符串类型
                time_str = str(time_str)

                # 如果时间格式为 "21:50:", 自动补全为 "21:50:00"
                if time_str.endswith(':'):
                    time_str += '00'

                # 尝试将时间格式解析为'%H:%M:%S'
                parsed_time = pd.to_datetime(time_str, format='%H:%M:%S', errors='coerce')
                if pd.notna(parsed_time):
                    return parsed_time.time()

                # 如果第一种格式解析失败，则尝试'%H:%M'
                parsed_time = pd.to_datetime(time_str, format='%H:%M', errors='coerce')
                if pd.notna(parsed_time):
                    return parsed_time.time()
            except Exception:
                return None
            return None


        # 应用parse_time函数到Time列
        df_final['Time'] = df_final['Time'].apply(parse_time)


        # # 替换空值为默认值（例如：'00:00:00'），如果需要
        # df_final['Time'].fillna(pd.Timestamp('00:00:00').time(), inplace=True)

        # 检查哪些Time列的值为None
        missing_time_rows = df_final[df_final['Time'].isna()]

        # 打印这些行以便分析
        print(missing_time_rows)


        # 过滤掉Program列为None的行
        df_final.dropna(subset=['Program'], inplace=True)

        # 将数据写入数据库
        df_final.to_sql('tv_programs', con=engine, if_exists='append', index=False)

    # 删除解压缩目录及其内容
    for root, dirs, files in os.walk(extract_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(extract_dir)
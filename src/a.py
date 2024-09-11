import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time  # 确保正确导入time模块
from fake_useragent import UserAgent
import logging
from datetime import datetime, timedelta
from tqdm import tqdm

ua = UserAgent()

# 配置日志
logger = logging.getLogger('cctv_schedule')
logger.setLevel(logging.INFO)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# 文件处理器
file_handler = logging.FileHandler('cctv_schedule.log')
file_handler.setLevel(logging.ERROR)
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)


# def get_channel_ids(date):
#     url = f"https://www.cctv.com/tvguide/tvguide/11/01/{date}/1.shtml"
#     headers = {
#         'User-Agent': ua.random  # 使用随机的User-Agent
#     }
#     try:
#         response = requests.get(url, headers=headers, timeout=20)
#         response.raise_for_status()
#
#         soup = BeautifulSoup(response.text, 'html.parser')
#         channel_ids = []
#
#         # 首先尝试查找 div.tv_list_box
#         tv_list_box = soup.find('div', {'class': 'tv_list_box'})
#         if tv_list_box:
#             # 查找所有的a标签，并提取javascript:gotoPage('', '<channel_id>')中的channel_id
#             a_tags = tv_list_box.find_all('a', href=True)
#             for a in a_tags:
#                 href = a['href']
#                 if "javascript:gotoPage(" in href:
#                     # 提取channel_id
#                     start_idx = href.find("','") + 3
#                     end_idx = href.find("')", start_idx)
#                     if start_idx > 2 and end_idx != -1:
#                         channel_id = href[start_idx:end_idx]
#                         channel_ids.append(channel_id)
#         else:
#             # 如果 div.tv_list_box 找不到，则尝试查找 class="sjb_c5" 的 table 结构
#             logger.warning("Could not find the div with class 'tv_list_box', trying to find table structure.")
#
#             sjb_c5_table_parent = soup.find('td', {'valign': 'top', 'width': '79'})
#             if sjb_c5_table_parent:
#                 table_element = sjb_c5_table_parent.find('table', {'width': '100%', 'border': '0', 'cellspacing': '0',
#                                                                    'cellpadding': '0'})
#                 if table_element:
#                     rows = table_element.find_all('tr')
#                     for row in rows:
#                         a_tag = row.find('a', href=True)
#                         if a_tag:
#                             href = a_tag['href']
#                             if "javascript:gotoPage(" in href:
#                                 # 提取channel_id
#                                 start_idx = href.find("','") + 3
#                                 end_idx = href.find("')", start_idx)
#                                 if start_idx > 2 and end_idx != -1:
#                                     channel_id = href[start_idx:end_idx]
#                                     channel_ids.append(channel_id)
#             else:
#                 # 如果两者都找不到，则返回默认的频道列表
#                 logger.error("Could not find channel list in any known structure, returning default list.")
#                 return ['1', '2', '3', '4', '68', '69', '5', '6', '7', '8', '9', '10', '11', '12', '13', '15', '16',
#                         '17', '95']
#
#         return channel_ids
#
#     except requests.RequestException as e:
#         logger.error(f"Failed to fetch channel ids for {date}: {e}")
#         return []


# def get_channel_ids_2(date):
#     url = f"http://www.kandianshi.com/1_{date}/"
#     headers = {
#         'User-Agent': ua.random  # 使用随机的User-Agent
#     }
#     try:
#         response = requests.get(url, headers=headers, timeout=20)
#         response.raise_for_status()
#
#         soup = BeautifulSoup(response.text, 'html.parser')
#         channel_ids = ["1"]
#
#         # 首先尝试查找 div.tv_list_box
#         tv_list_box = soup.find('div', {'id': 'zhongbu_kuang_zuo'})
#         if tv_list_box:
#             # 查找所有的a标签，并提取javascript:gotoPage('', '<channel_id>')中的channel_id
#             a_tags = tv_list_box.find_all('a', href=True)
#             for a in a_tags:
#                 href = a['href']
#                 if "/" in href:
#                     # 提取channel_id
#                     numbers = re.findall(r'/(\d+)/', href)
#                     channel_ids.append(numbers[0])
#                     # start_idx = href.find("/")
#                     # end_idx = href.find("'/", start_idx)
#                     # if start_idx > 0 and end_idx != -1:
#                     #     channel_id = href[start_idx:end_idx]
#                     #     channel_ids.append(channel_id)
#         else:
#             # 如果找不到，则返回默认的频道列表
#             logger.error("Could not find channel list in any known structure, returning default list.")
#             return range(1, 25)  # 1~24
#
#         return channel_ids
#
#     except requests.RequestException as e:
#         logger.error(f"Failed to fetch channel ids for {date}: {e}")
#         return []


# def get_channel_ids_3():
#     headers = {
#         'User-Agent': 'Mozilla/5.0'  # 使用随机的User-Agent (这里建议使用固定UA作为示例)
#     }
#
#     with open('./channel_ids_list.txt', 'a') as file:  # 以追加模式打开文件
#         for r in range(1, 450):
#             url = f"http://manhuadou.com/t-12300/p{r}"
#             try:
#                 response = requests.get(url, headers=headers, timeout=20)
#                 response.raise_for_status()
#
#                 soup = BeautifulSoup(response.text, 'html.parser')
#
#                 tv_list_box = soup.find('div', {'class': 'list-wrapper'})
#                 if tv_list_box:
#                     # 查找所有的a标签，并提取href中的channel_id
#                     a_tags = tv_list_box.find_all('a', href=True)
#                     for a in a_tags:
#                         file.write(a['href'] + '\n')  # 逐行写入channel_id
#                 else:
#                     # 如果找不到，则记录错误信息
#                     logger.error("Could not find channel list in any known structure, moving to next page.")
#             except requests.RequestException as e:
#                 logger.error(f"Failed to fetch channel ids for {r}: {e}")


# def fetch_schedule(date, channel_id, retries=3):
#     url = f"http://www.cctv.com/tvguide/schedule/cctv/{date}/{channel_id}.shtml"
#     headers = {
#         'User-Agent': ua.random  # 自动生成随机User-Agent
#     }
#
#     for attempt in range(retries):
#         try:
#             response = requests.get(url, headers=headers, timeout=20)
#             response.raise_for_status()
#
#             # 检测并处理编码问题
#             if 'content-type' in response.headers:
#                 content_type = response.headers['content-type']
#                 if 'charset' in content_type:
#                     charset = content_type.split('charset=')[-1]
#                 else:
#                     # 如果header中没有charset，尝试从HTML的<meta>标签中提取
#                     soup = BeautifulSoup(response.content, 'html.parser')
#                     meta = soup.find('meta', {'http-equiv': 'content-type'})
#                     if meta:
#                         content = meta.get('content')
#                         charset = content.split('charset=')[-1]
#                     else:
#                         charset = 'utf-8'  # 默认使用utf-8
#             else:
#                 charset = 'utf-8'  # 默认使用utf-8
#
#             # 使用正确的编码解析响应内容
#             response.encoding = charset
#             soup = BeautifulSoup(response.text, 'html.parser')
#
#             table = soup.find('table', {'border': '0', 'cellspacing': '12'})
#             schedule = []
#
#             if table:
#                 rows = table.find_all('tr')
#                 for row in rows:
#                     cells = row.find_all('td')
#                     if len(cells) >= 2:
#                         r_time = cells[0].get_text(strip=True)
#                         program = cells[1].get_text(strip=True)
#                         schedule.append({
#                             'Date': date,
#                             'Channel_ID': channel_id,
#                             'Time': r_time,
#                             'Program': program
#                         })
#             return schedule
#         except requests.RequestException as e:
#             logger.error(f"Attempt {attempt + 1} failed for {url}: {e}")
#             time.sleep(random.uniform(1, 3))  # 随机延时
#     logger.error(f"Failed to fetch {url} after {retries} attempts.")
#     return []

# def fetch_schedule_2(date, channel_id, retries=3):
#     url = f"https://www.cctv.com/tvguide/tvguide/11/01/{date}/{channel_id}.shtml"
#     headers = {
#         'User-Agent': ua.random
#     }
#
#     for attempt in range(retries):
#         try:
#             response = requests.get(url, headers=headers, timeout=20)
#             response.raise_for_status()
#
#             # 检测并处理编码问题
#             if 'content-type' in response.headers:
#                 content_type = response.headers['content-type']
#                 if 'charset' in content_type:
#                     charset = content_type.split('charset=')[-1]
#                 else:
#                     soup = BeautifulSoup(response.content, 'html.parser')
#                     meta = soup.find('meta', {'http-equiv': 'content-type'})
#                     if meta:
#                         content = meta.get('content')
#                         charset = content.split('charset=')[-1]
#                     else:
#                         charset = 'utf-8'
#             else:
#                 charset = 'utf-8'
#
#             response.encoding = charset
#             soup = BeautifulSoup(response.content, 'html.parser')
#
#             schedule = []
#
#             # 尝试查找 div.tlb_right
#             div_element = soup.find('div', class_='tlb_right')
#             if div_element:
#                 ul = div_element.find('ul')
#                 if ul:
#                     list_items = ul.find_all('li')
#                     for item in list_items:
#                         time_span = item.find('span', class_='time')
#                         program_span = item.find('span', class_='tv_name')
#
#                         if time_span and program_span:
#                             r_time = time_span.get_text(strip=True)
#                             program = program_span.get_text(strip=True)
#                             schedule.append({
#                                 'Date': date,
#                                 'Channel_ID': channel_id,
#                                 'Time': r_time,
#                                 'Program': program
#                             })
#                     return schedule
#                 else:
#                     logger.warning("Could not find the 'ul' element inside 'div.tlb_right'")
#             else:
#                 logger.warning("Could not find the div with class 'tlb_right'")
#
#             # 如果找不到 div.tlb_right，尝试使用 <table> 结构
#             logger.info("Attempting to parse table structure")
#             table_element = soup.find('table', {'cellpadding': '0', 'cellspacing': '12'})
#             if table_element:
#                 rows = table_element.find_all('tr')
#                 for row in rows:
#                     columns = row.find_all('td')
#                     if len(columns) >= 2:
#                         r_time = columns[0].get_text(strip=True)
#                         program = columns[1].get_text(strip=True)
#                         schedule.append({
#                             'Date': date,
#                             'Channel_ID': channel_id,
#                             'Time': r_time,
#                             'Program': program
#                         })
#                 return schedule
#             else:
#                 logger.error("Could not find a valid table structure")
#
#         except requests.RequestException as e:
#             logger.error(f"Attempt {attempt + 1} failed for {url}: {e}")
#             time.sleep(random.uniform(1, 3))  # 随机延时
#
#     logger.error(f"Failed to fetch {url} after {retries} attempts.")
#     return []


# def fetch_schedule_3(date, channel_id, retries=3):
#     url = f"http://www.cctv.com/soushi/28/{date}{channel_id}.shtml"
#     headers = {
#         'User-Agent': ua.random  # 自动生成随机User-Agent
#     }
#
#     for attempt in range(retries):
#         try:
#             response = requests.get(url, headers=headers, timeout=20)
#             response.raise_for_status()
#
#             # 检测并处理编码问题
#             if 'content-type' in response.headers:
#                 content_type = response.headers['content-type']
#                 if 'charset' in content_type:
#                     charset = content_type.split('charset=')[-1]
#                 else:
#                     soup = BeautifulSoup(response.content, 'html.parser')
#                     meta = soup.find('meta')
#                     if meta:
#                         content = meta.get('content')
#                         charset = content.split('charset=')[-1]
#                     else:
#                         charset = 'utf-8'
#             else:
#                 charset = 'utf-8'
#
#             response.encoding = charset
#             soup = BeautifulSoup(response.text, 'html.parser')
#
#             # 定位到包含节目表的div
#             epg_grid = soup.find('div', class_='epg_grid')
#             schedule = []
#
#             if epg_grid:
#                 rows = epg_grid.find_all('tr')
#
#                 for row in rows:
#                     # 每一行第一个单元格包含频道名称
#                     channel_cell = row.find('td', class_='venue')
#                     if channel_cell:
#                         channel_name = channel_cell.get_text(strip=True)
#
#                         # 后面的单元格包含时间和节目内容
#                         time_program_cells = row.find_all('td')[1:]  # 跳过第一个单元格（频道名称）
#
#                         for cell in time_program_cells:
#                             times = cell.find_all('div', class_='ptime')
#                             programs = cell.find_all('div', class_='pname')
#
#                             for p_time, program in zip(times, programs):
#                                 r_time = p_time.get_text(strip=True)
#                                 program_name = program.get_text(strip=True)
#                                 schedule.append({
#                                     'Date': date,
#                                     'Channel_ID': channel_id,
#                                     'Channel_Name': channel_name,
#                                     'Time': r_time,
#                                     'Program': program_name
#                                 })
#
#             return schedule
#
#         except requests.RequestException as e:
#             logger.error(f"Attempt {attempt + 1} failed for {url}: {e}")
#             time.sleep(random.uniform(1, 3))
#
#     logger.error(f"Failed to fetch {url} after {retries} attempts.")
#     return []

# def fetch_schedule_4(date, channel_id, retries=3):
#     url = f"http://www.kandianshi.com/{channel_id}_{date}/"
#     headers = {
#         'User-Agent': ua.random  # 自动生成随机User-Agent
#     }
#
#     for attempt in range(retries):
#         try:
#             response = requests.get(url, headers=headers, timeout=20)
#             response.raise_for_status()
#
#             # 检测并处理编码问题
#             if 'content-type' in response.headers:
#                 content_type = response.headers['content-type']
#                 if 'charset' in content_type:
#                     charset = content_type.split('charset=')[-1]
#                 else:
#                     soup = BeautifulSoup(response.content, 'html.parser')
#                     meta = soup.find('meta')
#                     if meta:
#                         content = meta.get('content')
#                         charset = content.split('charset=')[-1]
#                     else:
#                         charset = 'utf-8'
#             else:
#                 charset = 'utf-8'
#
#             response.encoding = charset
#             soup = BeautifulSoup(response.text, 'html.parser')
#
#             # 定位到包含节目表的table
#             schedule_table = soup.find('table', {'width': '100%', 'border': '0', 'cellpadding': '8', 'cellspacing': '1'})
#             schedule = []
#
#             if schedule_table:
#                 rows = schedule_table.find_all('tr')
#
#                 for row in rows[1:]:  # 跳过表头行
#                     cells = row.find_all('td', class_='td_nr')
#                     if len(cells) == 3:
#                         r_time = cells[0].get_text(strip=True)
#                         program_name = cells[1].get_text(strip=True)
#                         duration = cells[2].get_text(strip=True)
#
#                         schedule.append({
#                             'Date': date,
#                             'Channel_ID': channel_id,
#                             'Time': r_time,
#                             'Program': program_name,
#                             'Duration': duration
#                         })
#
#             return schedule
#
#         except requests.RequestException as e:
#             logger.error(f"Attempt {attempt + 1} failed for {url}: {e}")
#             time.sleep(random.uniform(1, 3))
#
#     logger.error(f"Failed to fetch {url} after {retries} attempts.")
#     return []


def fetch_schedule_5(retries=3):
    headers = {
        'User-Agent': ua.random  # 自动生成随机User-Agent
    }

    with open('channel_ids_list.txt', 'r') as file:
        lines = file.readlines()
        current_month = None

        # 使用tqdm包裹lines列表以展示进度
        for line in tqdm(lines, desc="Fetching schedules"):
            channel_id = line.strip()  # 去除行尾的换行符

            for attempt in range(retries):
                try:
                    response = requests.get(channel_id, headers=headers, timeout=20)
                    response.raise_for_status()

                    # 检测并处理编码问题
                    if 'content-type' in response.headers:
                        content_type = response.headers['content-type']
                        if 'charset' in content_type:
                            charset = content_type.split('charset=')[-1]
                        else:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            meta = soup.find('meta')
                            if meta:
                                content = meta.get('content')
                                charset = content.split('charset=')[-1]
                            else:
                                charset = 'utf-8'
                    else:
                        charset = 'utf-8'

                    response.encoding = charset
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # 获取频道名称
                    channel_name = soup.find('h1', class_='title').get_text(strip=True)

                    # 获取更新时间
                    time_tag = soup.find('p', class_='time')
                    if time_tag:
                        date_match = re.search(r'\d{4}-\d{2}-\d{2}', time_tag.get_text())
                        if date_match:
                            date = date_match.group(0).replace("-", "")
                        else:
                            logger.error(f"Failed to extract date for {channel_id}")
                            break  # 退出重试循环
                    else:
                        logger.error(f"No time tag found for {channel_id}")
                        break  # 退出重试循环

                    # 提取当前处理的月份
                    year_month = date[:6]  # YYYYMM格式
                    if current_month is None:
                        current_month = year_month
                    elif year_month != current_month:
                        current_month = year_month

                    # 定位到包含节目表的div
                    mancon_div = soup.find('div', class_='mancon')
                    schedule = []

                    if mancon_div:
                        paragraphs = mancon_div.find_all('p')

                        # 跳过特定的非节目段落（如"上午节目", "下午节目"）
                        for paragraph in paragraphs:
                            text = paragraph.get_text(strip=True)
                            if text.startswith("上午节目") or text.startswith("下午节目") or "manhuadou" in text:
                                continue
                            if ":" in text:
                                parts = text.split(' ', 1)
                                if len(parts) == 2:
                                    r_time, program_name = parts
                                    schedule.append({
                                        'Date': date,
                                        'Channel_ID': channel_id,
                                        'Channel_Name': channel_name,
                                        'Time': r_time,
                                        'Program': program_name
                                    })

                    if schedule:
                        save_to_csv(schedule, current_month)  # 实时保存到 CSV
                    break  # 成功获取数据，退出重试循环

                except requests.RequestException as e:
                    logger.error(f"Attempt {attempt + 1} failed for {channel_id}: {e}")
                    time.sleep(random.uniform(1, 3))  # 在重试之间添加一个随机的延迟

                if attempt == retries - 1:
                    logger.error(f"Failed to fetch {channel_id} after {retries} attempts.")

            time.sleep(random.uniform(1, 5))  # Random delay between requests


def save_to_csv(schedule, month):
    filename = f"cctv_schedules_{month}.csv"
    df = pd.DataFrame(schedule)

    # 如果文件不存在，则创建新文件并写入表头，否则追加数据
    with open(filename, 'a', encoding='utf-8-sig', newline='') as f:
        df.to_csv(f, index=False, header=f.tell() == 0)  # 只有文件为空时写入表头


def generate_dates(start_date, end_date):
    start = datetime.strptime(start_date, "%Y%m%d")
    end = datetime.strptime(end_date, "%Y%m%d")
    delta = timedelta(days=1)

    current = start
    while current <= end:
        yield current.strftime("%Y%m%d")
        current += delta


def main():
    start_date = "20160719"
    end_date = "20170730"
    # channel_ids_1 = range(1, 18)  # Channel IDs from 1 to 17
    # channel_ids_3 = ["0006", "0612", "1218", "1824"]
    # get_channel_ids_3()
    # current_month = None
    #
    # for date in generate_dates(start_date, end_date):
    #     year_month = date[:6]  # Extract YYYYMM format
    #     if current_month is None:
    #         current_month = year_month
    #     if year_month != current_month:
    #         current_month = year_month
    #
    #     # channel_ids_2 = get_channel_ids(date)
    #     # channel_ids_4 = get_channel_ids_2(date)
    #     for channel_id in channel_ids_5:
    #         logger.info(f"Fetching schedule for {date}, Channel {channel_id}...")
    #         # schedule = fetch_schedule(date, channel_ids_1)
    #         # schedule = fetch_schedule_2(date, channel_ids_2)
    #         # schedule = fetch_schedule_3(date, channel_id)
    #         schedule = fetch_schedule_4(date, channel_id)
    #         if schedule:
    #             save_to_csv(schedule, current_month)  # Save to CSV immediately
    #         time.sleep(random.uniform(1, 5))  # Random delay between requests

    fetch_schedule_5()

if __name__ == "__main__":
    main()

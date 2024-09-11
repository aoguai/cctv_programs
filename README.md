## CCTV-PROGRAMS

该项目爬取了可以从网络中可寻找到的CCTV央视网历史节目单，包括节目名称、播出时间、播出频道等信息。

### 项目结构

```
cctv_programs
├─ LICENSE
├─ README.md
├─ data # 存放爬取的数据
├─ requirements.txt
└─ src # 存放源代码
```

### 使用方法

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 运行爬虫

```bash
python src/a.py
python src/b.py
python src/c.py
```

#### 已爬取的数据

如果你没有代码阅览需求，可以直接下载已经处理好的 [已爬取的数据](https://github.com/aoguai/cctv_programs/tree/master/data)

| 下载方式      | 链接                                                                                             | 提取码/密码   |
|---------------|--------------------------------------------------------------------------------------------------|---------------|
| 百度网盘      | [https://pan.baidu.com/s/1nXWSkugRxnWsv6toM-jpdw](https://pan.baidu.com/s/1nXWSkugRxnWsv6toM-jpdw) | prtz          |
| 蓝奏云盘      | [https://aoguai.lanzn.com/iv2Q129saipi](https://aoguai.lanzn.com/iv2Q129saipi)                     | g3aw          |
| Google Drive  | [https://drive.google.com/file/d/1va-qE6agu4uEajfAnCwETD_pgfT3rlwU/](https://drive.google.com/file/d/1va-qE6agu4uEajfAnCwETD_pgfT3rlwU/) | 无            |
| Github        | [https://github.com/aoguai/cctv_programs/tree/master/data](https://github.com/aoguai/cctv_programs/tree/master/data) | 无            |


包括：
```
data
├─ cctv_2003年4月28日-2006年4月30日.7z
├─ cctv_2006年4月24日-2008年4月6日.7z
├─ cctv_2008年3月2日-2016年7月18日.7z
├─ cctv_2016年7月19日-2017年7月30日.7z
├─ cctv_2018年10月17日-2024年8月17日.7z
├─ tv_programs_all.sql.zip
└─ tv_programs_db.sql
```
- 7z 压缩包内均为对应时间段的节目单CSV数据和对应的cctv_schedule.log日志文件
- tv_programs_all.sql.zip 内为所有数据的合并后的SQL文件，由 `b.py` 生成
- tv_programs_db.sql 为表结构的SQL文件

同时我们搭建了一个在线查询 [tv.aoguai.top](https://tv.aoguai.top) 网站，可以直接浏览并查询已爬取的数据。

#### 注意

由于爬取的数据年份跨越长，采用了多来源的数据，因此爬取的数据可能存在重复。在数据处理时，可以根据自己的需求进行去重。

**由于采用了多来源的数据，因此数据的格式可能存在差异，需要根据实际情况进行处理。已经处理好的 [已爬取的数据](https://github.com/aoguai/cctv_programs/data) 中的 SQL 文件数据已经进行了处理。 而 CSV 为原始数据。**

同时对于来源说明：

| 时间范围                      | 查询网址格式                                                                                           |
|-------------------------------|-------------------------------------------------------------------------------------------------------|
| 2003年4月28日 - 2006年4月30日 | `http://www.cctv.com/tvguide/schedule/cctv/{date}/{channel_id}.shtml`                                  |
| 2006年4月24日 - 2008年4月6日  | `https://www.cctv.com/tvguide/tvguide/11/01/{date}/{channel_id}.shtml`                                |
| 2008年3月1日 - 2016年7月18日  | `http://www.cctv.com/soushi/28/{date}{channel_id}.shtml`                                               |
| 2016年7月19日 - 2017年7月30日 | `http://www.kandianshi.com/{channel_id}_{date}/`                                                       |
| 2018年10月17日 - 至今         | `http://manhuadou.com/t-12300/p{r}`                                                                    |

##### 字段说明：
- **{date}**：表示日期的占位符，具体日期应根据实际查询需求替换。
- **{channel_id}**：表示频道ID的占位符，具体频道ID应根据实际查询需求替换。
- **{r}**：在最后一行的URL格式中，`{r}`是页码或序列号的占位符。

中间缺失了 2017 年 7 月 31 日-2018 年 10 月 16 日的数据，如果有更多的数据来源，欢迎提交 PR。

同时2016年7月19日-2017年7月30日的节目单和2018年10月17日-2024年8月17日的节目单数据的来源非来自CCTV官方网站，可能存在一定的不准确性。

## License 说明

[cctv_programs](https://github.com/aoguai/cctv_programs) 使用 AGPL-3.0 license 进行开源，详情请参阅 [LICENSE](./LICENSE) 文件。
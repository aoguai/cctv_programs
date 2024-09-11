from sqlalchemy import create_engine, text

# 创建数据库连接
engine = create_engine('mysql+pymysql://user:password@localhost/tv_programs_db')

# 获取所有不同的 channel_id
with engine.connect() as conn:
    result = conn.execute(text("SELECT DISTINCT channel_id FROM tv_programs"))
    channel_ids = [row[0] for row in result.fetchall()]  # 使用索引访问数据

# 为每个 channel_id 创建新表
for channel_id in channel_ids:
    table_name = f"tv_programs_{channel_id.replace('-', '_')}"  # 替换非法字符
    create_table_sql = f"""
    CREATE TABLE {table_name} AS
    SELECT *
    FROM tv_programs
    WHERE channel_id = :channel_id
    """
    with engine.connect() as conn:
        conn.execute(text(create_table_sql), {'channel_id': channel_id})

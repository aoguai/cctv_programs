-- 创建数据库
CREATE DATABASE IF NOT EXISTS tv_programs_db;

-- 选择数据库
USE tv_programs_db;

-- 创建表
CREATE TABLE tv_programs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    channel_id VARCHAR(255) NOT NULL,
    channel_name VARCHAR(255) DEFAULT NULL,
    time TIME NOT NULL,
    program VARCHAR(255) NOT NULL,
    duration VARCHAR(255) DEFAULT NULL,
    INDEX idx_date (date),
    INDEX idx_channel_id (channel_id),
    INDEX idx_time (time)
);
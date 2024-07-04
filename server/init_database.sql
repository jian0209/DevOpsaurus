CREATE DATABASE IF NOT EXISTS `devopsaurus` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE USER IF NOT EXISTS 'devopsaurus'@'%' IDENTIFIED BY 'devopsaurus';
GRANT ALL PRIVILEGES ON `devopsaurus`.* TO 'devopsaurus'@'%';
FLUSH PRIVILEGES;

USE `devopsaurus`;

CREATE TABLE `d_user_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'unique username',
  `password` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'password for username',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'email for sending message',
  `group` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'group name to which the user belongs, e.g. admin, user',
  `mfa_status` int DEFAULT 0 NOT NULL COMMENT 'mfa status, to check is user has secret key, 0: disable, 1: enable',
  `mfa_secret_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'mfa secret key',
  `is_password_force_reset` int DEFAULT 0 NOT NULL COMMENT 'password force reset status, 0: disable, 1: enable',
  `role` int DEFAULT 0 NOT NULL COMMENT 'user role, 0: visitor, 1: reader, 2: writer, 3: admin',
  `status` int DEFAULT 0 NOT NULL COMMENT 'status, 0: inactive, 1: active',
  `created_at` int NOT NULL DEFAULT 0 COMMENT 'created unix timestamp',
  PRIMARY KEY (`id`), -- 将 id 字段设置为主键
  UNIQUE KEY `uni_username` (`username`), -- 将 username 字段设置为唯一索引
  INDEX idx_email (`email`),
  INDEX idx_username (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `d_login_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT 'user id',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'username',
  `last_login_time` int NOT NULL DEFAULT 0 COMMENT 'last login unix timestamp',
  `last_login_ip` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'last login ip',
  `user_agent` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'user logged in user agent',
  `status` int DEFAULT 0 NOT NULL COMMENT 'status, 0: failed, 1: success',
  `reason` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'reason for login status',
  PRIMARY KEY (`id`), -- 将 id 字段设置为主键
  INDEX idx_user_id (`user_id`),
  INDEX idx_username (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `d_system_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'username',
  `role` int DEFAULT 0 NOT NULL COMMENT 'user role, 0: visitor, 1: reader, 2: writer, 3: admin',
  `action` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'user action',
  `source` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'source of user action',
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'description of user action',
  `created_at` int NOT NULL DEFAULT 0 COMMENT 'created unix timestamp',
  PRIMARY KEY (`id`), -- 将 id 字段设置为主键
  INDEX idx_username (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

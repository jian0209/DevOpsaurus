CREATE DATABASE IF NOT EXISTS `devopsaurus` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE USER IF NOT EXISTS 'devopsaurus'@'%' IDENTIFIED BY 'devopsaurus';
GRANT ALL PRIVILEGES ON `devopsaurus`.* TO 'devopsaurus'@'%';
FLUSH PRIVILEGES;

USE `devopsaurus`;

CREATE TABLE `devopsaurus`.`d_user_info` (
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

CREATE TABLE `devopsaurus`.`d_login_log` (
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

CREATE TABLE `devopsaurus`.`d_system_log` (
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

CREATE TABLE `devopsaurus`.`d_command` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'command name (unique)',
  `host` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'host ip / name',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'username for login',
  `ssh_key` MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ssh public key',
  `ssh_port` int DEFAULT 22 NOT NULL COMMENT 'port for ssh',
  `command` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'command to execute',
  `status` int DEFAULT 0 NOT NULL COMMENT 'status, 0: inactive, 1: active',
  `created_at` int NOT NULL DEFAULT 0 COMMENT 'created unix timestamp',
  PRIMARY KEY (`id`), -- 将 id 字段设置为主键
  INDEX idx_name (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `devopsaurus`.`d_system_integration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_email_allow` int NOT NULL COMMENT 'send email, 0: disable, 1: enable',
  `is_telegram_allow` int NOT NULL COMMENT 'send telegram message, 0: disable, 1: enable',
  `is_slack_allow` int NOT NULL COMMENT 'send slack message, 0: disable, 1: enable',
  `email_smtp_server` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'email smtp server',
  `email_smtp_port` int DEFAULT 0 COMMENT 'email smtp port',
  `email_smtp_username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'email smtp username',
  `email_smtp_password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'email smtp password',
  `email_from` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'email from',
  `email_helo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'email helo domain',
  `email_allow_ssl_tls` int DEFAULT 0 COMMENT 'email allow ssl tls, 0: disable, 1: enable',
  `email_allow_start_tls` int DEFAULT 0 COMMENT 'email allow start tls, 0: disable, 1: enable',
  `telegram_bot_token` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'telegram bot token',
  `telegram_chat_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'telegram chat id',
  `telegram_parse` int DEFAULT 0 COMMENT 'telegram parse mode, 0: normal, 1: markdown',
  `slack_bot_token` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'slack bot token',
  `slack_channel` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'slack channel',
  `slack_token` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'slack token',
  PRIMARY KEY (`id`) -- 将 id 字段设置为主键
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `devopsaurus`.`d_system_integration` VALUES (1, 0, 0, 0, null, null, null, null, null, null, null, null, null, null, null, null, null, null);

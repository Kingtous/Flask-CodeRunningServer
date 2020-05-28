-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Apr 21, 2020 at 10:30 AM
-- Server version: 5.7.25
-- PHP Version: 7.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `cloud`
--

-- --------------------------------------------------------

--
-- Table structure for table `Cart`
--

CREATE TABLE `Cart`
(
    `id`          int(11) NOT NULL,
    `user_id`     int(11) NOT NULL,
    `item_id`     int(11) NOT NULL,
    `create_date` datetime DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Code`
--

CREATE TABLE `Code`
(
    `id`          int(11)      NOT NULL,
    `user_id`     int(11)      NOT NULL,
    `code_type`   int(11)  DEFAULT NULL,
    `local_path`  varchar(256) NOT NULL,
    `create_date` datetime DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- --------------------------------------------------------

--
-- Table structure for table `CodeBought`
--

CREATE TABLE `CodeBought`
(
    `id`      int(11) NOT NULL,
    `user_id` int(11) NOT NULL,
    `code_id` int(11) NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- --------------------------------------------------------

--
-- Table structure for table `CodeResult`
--

CREATE TABLE `CodeResult`
(
    `id`      int(11) NOT NULL,
    `user_id` int(11) NOT NULL,
    `code_id` int(11) NOT NULL,
    `status`  int(11) DEFAULT NULL,
    `result`  mediumtext
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- --------------------------------------------------------

--
-- Table structure for table `CodeSharing`
--

CREATE TABLE `CodeSharing`
(
    `id`           int(11) NOT NULL,
    `user_id`      int(11) NOT NULL,
    `code_id`      int(11) NOT NULL,
    `like_nums`    int(11)    DEFAULT NULL,
    `dislike_nums` int(11)    DEFAULT NULL,
    `is_private`   tinyint(1) DEFAULT NULL,
    `credits`      int(11)    DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Comments`
--

CREATE TABLE `Comments`
(
    `id`          int(11) NOT NULL,
    `user_id`     int(11) NOT NULL,
    `code_id`     int(11)  DEFAULT NULL,
    `threads_id`  int(11) NOT NULL,
    `content`     text,
    `parent_id`   int(11)  DEFAULT NULL,
    `next_id`     int(11)  DEFAULT NULL,
    `create_date` datetime DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

--
-- Dumping data for table `Comments`
--

INSERT INTO `Comments` (`id`, `user_id`, `code_id`, `threads_id`, `content`, `parent_id`, `next_id`, `create_date`)
VALUES (1, 1, NULL, 21, '沙发！', NULL, NULL, '2020-04-21 14:12:44'),
       (2, 2, NULL, 21, '加油！', 1, NULL, '2020-04-21 17:09:29'),
       (3, 1, NULL, 21, '赚一点积分，水个贴', 1, NULL, '2020-04-21 18:23:43'),
       (4, 1, NULL, 21, '！！❤️', 1, NULL, '2020-04-21 18:24:08');

-- --------------------------------------------------------

--
-- Table structure for table `Item`
--

CREATE TABLE `Item`
(
    `id`      int(11) NOT NULL,
    `name`    varchar(128)  DEFAULT NULL,
    `detail`  varchar(1024) DEFAULT NULL,
    `credits` int(11)       DEFAULT NULL,
    `isOn`    tinyint(1)    DEFAULT NULL,
    `img`     varchar(255)  DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

--
-- Dumping data for table `Item`
--

INSERT INTO `Item` (`id`, `name`, `detail`, `credits`, `isOn`, `img`)
VALUES (1, '联通5G 10M流量包', '当月有效，不结转', 10, 1,
        'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3172885702,2605102988&fm=26&gp=0.jpg'),
       (5, '移动5G 10M流量包', '当月有效，不结转', 10, 1,
        'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3172885702,2605102988&fm=26&gp=0.jpg'),
       (6, '电信5G 10M流量包', '当月有效，不结转', 10, 1,
        'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3172885702,2605102988&fm=26&gp=0.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `Points`
--

CREATE TABLE `Points`
(
    `user_id` int(11) NOT NULL,
    `points`  int(11) DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Repository`
--

CREATE TABLE `Repository`
(
    `id`          int(11) NOT NULL,
    `user_id`     int(11) NOT NULL,
    `item_id`     int(11) NOT NULL,
    `create_date` datetime DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- --------------------------------------------------------

--
-- Table structure for table `SignIn`
--

CREATE TABLE `SignIn`
(
    `user_id`      int(11) NOT NULL,
    `sign_in_time` datetime DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Threads`
--

CREATE TABLE `Threads`
(
    `id`         int(11) NOT NULL,
    `user_id`    int(11) NOT NULL,
    `code_id`    int(11) DEFAULT NULL,
    `comment_id` int(11) DEFAULT NULL,
    `title`      tinytext,
    `subtitle`   text
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

--
-- Dumping data for table `Threads`
--

INSERT INTO `Threads` (`id`, `user_id`, `code_id`, `comment_id`, `title`, `subtitle`)
VALUES (1, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (2, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (3, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (4, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (5, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (6, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (7, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (8, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (9, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (10, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (11, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (12, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (13, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (14, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (15, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (16, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (17, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (18, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (19, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (20, 1, NULL, NULL, '武汉加油', '中国加油！'),
       (21, 1, NULL, 1, '武汉加油', '中国加油！');

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE `User`
(
    `id`            int(11)      NOT NULL,
    `username`      varchar(32)  DEFAULT NULL,
    `nickname`      varchar(50)  DEFAULT NULL,
    `mail`          varchar(128) NOT NULL,
    `avatar_url`    varchar(255) DEFAULT NULL,
    `password_hash` varchar(128) DEFAULT NULL,
    `credits`       int(11)      DEFAULT NULL,
    `likes`         int(11)      DEFAULT NULL,
    `role`          int(11)      DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`id`, `username`, `nickname`, `mail`, `avatar_url`, `password_hash`, `credits`, `likes`, `role`)
VALUES (1, 'Kingtous', '天龙八部2', '827628836@qq.com',
        'http://t7.baidu.com/it/u=3616242789,1098670747&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg?sec=1588059201&t=8218326acdc202f2aee2eb0e4eb15ca9',
        '$6$rounds=656000$d9bju7hZeWiiaJ.I$JjtPq.nZm.Q4V834OQXukhCCcZ7ExMk4Cn2Y17pVbhzBoNeqZdkFpxu/3XEHa0TgRu1Hxbevp5i0wjSHZCBHj1',
        11, 0, 1),
       (2, 'Kingtouss', '开心每一天！！', 'kingtous@qq.com',
        'http://t8.baidu.com/it/u=1484500186,1503043093&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg?sec=1588064944&t=dd289ffb5bcf3a9d5355f461e7bd3eff',
        '$6$rounds=656000$iXFgjB9Pf1DPSZdl$f.2fqOnMB.04R0hH6yGeaquCFHKLsczGgbin2pcahmNBJiUjAWux3D1AzkOklRLkomIoKxn9lCS/MTTCb.5NJ0',
        0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `UserLikes`
--

CREATE TABLE `UserLikes`
(
    `user_id`   int(11) NOT NULL,
    `like_user` int(11) NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Cart`
--
ALTER TABLE `Cart`
    ADD PRIMARY KEY (`id`, `user_id`, `item_id`),
    ADD KEY `user_id` (`user_id`),
    ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `Code`
--
ALTER TABLE `Code`
    ADD PRIMARY KEY (`id`),
    ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `CodeBought`
--
ALTER TABLE `CodeBought`
    ADD PRIMARY KEY (`id`),
    ADD KEY `user_id` (`user_id`),
    ADD KEY `code_id` (`code_id`);

--
-- Indexes for table `CodeResult`
--
ALTER TABLE `CodeResult`
    ADD PRIMARY KEY (`id`),
    ADD KEY `code_id` (`code_id`),
    ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `CodeSharing`
--
ALTER TABLE `CodeSharing`
    ADD PRIMARY KEY (`id`),
    ADD KEY `user_id` (`user_id`),
    ADD KEY `code_id` (`code_id`);

--
-- Indexes for table `Comments`
--
ALTER TABLE `Comments`
    ADD PRIMARY KEY (`id`),
    ADD KEY `code_id` (`code_id`),
    ADD KEY `next_id` (`next_id`),
    ADD KEY `threads_id` (`threads_id`),
    ADD KEY `user_id` (`user_id`),
    ADD KEY `parent_id` (`parent_id`);

--
-- Indexes for table `Item`
--
ALTER TABLE `Item`
    ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Points`
--
ALTER TABLE `Points`
    ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `Repository`
--
ALTER TABLE `Repository`
    ADD PRIMARY KEY (`id`),
    ADD KEY `user_id` (`user_id`),
    ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `SignIn`
--
ALTER TABLE `SignIn`
    ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `Threads`
--
ALTER TABLE `Threads`
    ADD PRIMARY KEY (`id`),
    ADD KEY `comment_id` (`comment_id`),
    ADD KEY `code_id` (`code_id`),
    ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
    ADD PRIMARY KEY (`id`),
    ADD UNIQUE KEY `ix_User_mail` (`mail`),
    ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `UserLikes`
--
ALTER TABLE `UserLikes`
    ADD PRIMARY KEY (`user_id`, `like_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Cart`
--
ALTER TABLE `Cart`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 12;

--
-- AUTO_INCREMENT for table `Code`
--
ALTER TABLE `Code`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 5;

--
-- AUTO_INCREMENT for table `CodeBought`
--
ALTER TABLE `CodeBought`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `CodeResult`
--
ALTER TABLE `CodeResult`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 3;

--
-- AUTO_INCREMENT for table `CodeSharing`
--
ALTER TABLE `CodeSharing`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Comments`
--
ALTER TABLE `Comments`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 5;

--
-- AUTO_INCREMENT for table `Item`
--
ALTER TABLE `Item`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 8;

--
-- AUTO_INCREMENT for table `Repository`
--
ALTER TABLE `Repository`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 11;

--
-- AUTO_INCREMENT for table `SignIn`
--
ALTER TABLE `SignIn`
    MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Threads`
--
ALTER TABLE `Threads`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 22;

--
-- AUTO_INCREMENT for table `User`
--
ALTER TABLE `User`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Cart`
--
ALTER TABLE `Cart`
    ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
    ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `Item` (`id`);

--
-- Constraints for table `Code`
--
ALTER TABLE `Code`
    ADD CONSTRAINT `code_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `CodeBought`
--
ALTER TABLE `CodeBought`
    ADD CONSTRAINT `codebought_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE,
    ADD CONSTRAINT `codebought_ibfk_2` FOREIGN KEY (`code_id`) REFERENCES `Code` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `CodeResult`
--
ALTER TABLE `CodeResult`
    ADD CONSTRAINT `coderesult_ibfk_1` FOREIGN KEY (`code_id`) REFERENCES `Code` (`id`) ON DELETE CASCADE,
    ADD CONSTRAINT `coderesult_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `CodeSharing`
--
ALTER TABLE `CodeSharing`
    ADD CONSTRAINT `codesharing_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
    ADD CONSTRAINT `codesharing_ibfk_2` FOREIGN KEY (`code_id`) REFERENCES `Code` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `Comments`
--
ALTER TABLE `Comments`
    ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`code_id`) REFERENCES `Code` (`id`),
    ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`next_id`) REFERENCES `Comments` (`id`),
    ADD CONSTRAINT `comments_ibfk_3` FOREIGN KEY (`threads_id`) REFERENCES `Threads` (`id`),
    ADD CONSTRAINT `comments_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
    ADD CONSTRAINT `comments_ibfk_5` FOREIGN KEY (`parent_id`) REFERENCES `Comments` (`id`);

--
-- Constraints for table `Points`
--
ALTER TABLE `Points`
    ADD CONSTRAINT `points_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `Repository`
--
ALTER TABLE `Repository`
    ADD CONSTRAINT `repository_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
    ADD CONSTRAINT `repository_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `Item` (`id`);

--
-- Constraints for table `Threads`
--
ALTER TABLE `Threads`
    ADD CONSTRAINT `threads_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `Comments` (`id`),
    ADD CONSTRAINT `threads_ibfk_2` FOREIGN KEY (`code_id`) REFERENCES `Code` (`id`),
    ADD CONSTRAINT `threads_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`);

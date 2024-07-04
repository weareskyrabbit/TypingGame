-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2024-07-04 02:55:43
-- サーバのバージョン： 10.4.25-MariaDB
-- PHP のバージョン: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- データベース: `dakend`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `rankboard`
--

CREATE TABLE `rankboard` (
  `usernum` int(255) NOT NULL,
  `easyScore` int(255) NOT NULL,
  `normalScore` int(255) NOT NULL,
  `hardScore` int(255) NOT NULL,
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp(),
  `updateAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- テーブルのデータのダンプ `rankboard`
--

INSERT INTO `rankboard` (`usernum`, `easyScore`, `normalScore`, `hardScore`, `createdAt`, `updateAt`) VALUES
(1, 0, 0, 0, '2024-06-27 01:49:38', '2024-06-27 01:49:38'),
(2, 1, 1, 1, '2024-06-27 01:49:38', '2024-06-27 03:04:32'),
(3, 0, 0, 0, '2024-06-27 01:48:08', '2024-06-27 01:48:08');

-- --------------------------------------------------------

--
-- テーブルの構造 `users`
--

CREATE TABLE `users` (
  `usernum` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `accountName` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp(),
  `updateAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- テーブルのデータのダンプ `users`
--

INSERT INTO `users` (`usernum`, `email`, `accountName`, `password`, `createdAt`, `updateAt`) VALUES
(1, 'test1@test.jp', 'test1', '1b4f0e9851971998e732078544c96b36c3d01cedf7caa332359d6f1d83567014', '2024-05-23 03:20:31', '2024-06-20 01:37:16'),
(2, 'test2@test.jp', 'test2', '60303ae22b998861bce3b28f33eec1be758a213c86c93c076dbe9f558c11c752', '2024-06-13 01:26:25', '2024-06-13 01:26:25'),
(3, 'test3@test.jp', 'test3', 'fd61a03af4f77d870fc21e05e7e80678095c92d808cfb3b5c279ee04c74aca13', '2024-06-27 01:45:26', '2024-06-27 01:45:26');

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `rankboard`
--
ALTER TABLE `rankboard`
  ADD PRIMARY KEY (`usernum`);

--
-- テーブルのインデックス `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`usernum`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `rankboard`
--
ALTER TABLE `rankboard`
  MODIFY `usernum` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- テーブルの AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `usernum` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

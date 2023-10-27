SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE `users`
(
  `serial` int(11) NOT NULL,
  `guild_id` bigint(64) DEFAULT NULL,
  `user_id` bigint(64) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `total_messages` int(11) DEFAULT 0,
  `total_voice` float DEFAULT 0.0,
  `level` int(11) DEFAULT 0,
  `xp` int(11) DEFAULT 0
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

ALTER TABLE `users`
  ADD PRIMARY KEY (`serial`);
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `serial` int(24) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

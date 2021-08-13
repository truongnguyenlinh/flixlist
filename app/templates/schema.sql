--
-- Database: `db`
--

-- --------------------------------------------------

--
-- Table structure for table `flixes`
--

DROP TABLE IF EXISTS `flixes`;
CREATE TABLE IF NOT EXISTS `flixes` (
  `flix_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `status` enum('Currently Watching', 'Completed', 'On Hold', 'Dropped', 'Plan to Watch')
  `media_name` varchar(250) NOT NULL,
  `media_type` enum('Show', 'Movie', 'Anime', 'Short/temporary series', 'Docuseries', 'Documentary', 'Other') NOT NULL,
  `media_genre` varchar(50) NOT NULL,
  `year` varchar(50) NOT NULL,
  `duration_estimate` double NOT NULL,
  `longitude` double NOT NULL,
  `image_key` varchar(250) NOT NULL,
  `recommender_id` varchar(50),
  `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`flix_id`),
  KEY `flixes_fk_user_id` (`user_id`)
) DEFAULT CHARSET=latin1;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`)
) DEFAULT CHARSET=latin1;

--
-- Constraints for table `flixes`
--

ALTER TABLE `flixes`
  ADD CONSTRAINT `flixes_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
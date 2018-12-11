use test; 
CREATE TABLE `fbtag_scrapy` (
  `user_id` bigint,
  `post_id` bigint NOT NULL,
  `discussion_id` bigint NOT NULL,
  `post_content_html` text, 
  `post_content_text` text,
  `discussion_title` text,
  `image_urls` text,
  `url` text,
  `user_name` varchar(255) DEFAULT NULL,
  `discussion_comments_count` int,
  discussion_tags varchar(255),
  discussion_participants_count int, 
  `created_time_text` varchar(255) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `inserted_time` datetime DEFAULT NULL,
  post_number int, 
  PRIMARY KEY (`post_id`, `discussion_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

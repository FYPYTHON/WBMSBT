# Host: localhost  (Version 5.7.24-log)
# Date: 2019-08-02 17:25:38
# Generator: MySQL-Front 6.0  (Build 2.20)


#
# Structure for table "tbl_account"
#

DROP TABLE IF EXISTS `tbl_account`;
CREATE TABLE `tbl_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `nickname` varchar(20) DEFAULT '龙卷风' COMMENT '昵称',
  `password` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `userstate` int(11) DEFAULT NULL COMMENT '0=正常，1=不可用',
  `userrole` int(11) DEFAULT NULL COMMENT '0=管理员，1=普通用户',
  `register_time` datetime DEFAULT NULL,
  `avatar_path` varchar(100) DEFAULT NULL COMMENT '用户头像地址',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

#
# Data for table "tbl_account"
#

INSERT INTO `tbl_account` VALUES (1,'a123456','龙卷风','6e9c7dc639c154afaf9041230f7caa92','1823218990@qq.com',0,0,'2019-01-15 09:59:53',NULL),(2,'ff','龙卷风','123456','11@qq.com',0,1,'2019-01-16 14:05:34',NULL),(3,'test1','龙卷风','6e9c7dc639c154afaf9041230f7caa92','1234567@qq.com',0,1,'2019-01-19 11:01:07',NULL),(4,'test2','龙卷风','6e9c7dc639c154afaf9041230f7caa92','11@qq.com',0,1,'2019-01-19 11:07:08',NULL),(5,'test4','龙卷风','6e9c7dc639c154afaf9041230f7caa92','1234@sdf.com',0,1,'2019-01-19 11:08:47',NULL),(6,'test3','龙卷风','6e9c7dc639c154afaf9041230f7caa92','11@qq.com',0,1,'2019-01-19 11:08:47',NULL),(7,'test5','龙卷风','23becbd28cf34b382639a42cb6b75710','111@ld.com',0,1,'2019-01-19 11:10:47',NULL),(8,'feiying','龙卷风','6e9c7dc639c154afaf9041230f7caa92','18234343@126.com',0,1,'2019-01-19 11:15:02',NULL),(9,'tewt1','龙卷风','f7090ebd059087180672cf4c46decaae','11@qq.com',0,1,'2019-01-19 11:16:24',NULL),(10,'ceshi','龙卷风','6e9c7dc639c154afaf9041230f7caa92','113@182.com',0,0,'2019-01-19 11:18:15',NULL),(15,'zhangsan','龙卷风','zhangsan','zhangsan@126.com',0,1,'2019-06-25 14:42:16',NULL),(17,'zhangsan1','龙卷风','zahngsan','zang@126.com',0,1,'2019-06-25 14:44:00',NULL),(18,'zhangsan2','龙卷风','zhangsan','zhang@126.com',0,1,'2019-06-25 15:00:06',NULL),(19,'zhangsan3','龙卷风','zhangsan','zhang@126.com',0,1,'2019-06-26 09:09:15',NULL);

#
# Structure for table "tbl_admin"
#

DROP TABLE IF EXISTS `tbl_admin`;
CREATE TABLE `tbl_admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) DEFAULT NULL COMMENT '变量名',
  `value` varchar(60) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

#
# Data for table "tbl_admin"
#

INSERT INTO `tbl_admin` VALUES (1,'__MAIL__','1823218990@qq.com',1),(2,'__MAILPASSWORD__','mjiymnbjzbarcdbb',1),(3,'currentname','feiying',0),(4,'description','test only',0),(5,'admin_email','1490726887@qq.com',0),(6,'can_register','1',1),(7,'can_comment','1',1),(8,'comments_notify','1',1),(9,'default_category','default_category',0),(10,'page_size','10',1),(11,'rss_size','10',1),(12,'rss_excerpt','1',1),(13,'new_rss_size','5',1),(14,'new_page_size','5',1);

#
# Structure for table "tbl_browsing_history"
#

DROP TABLE IF EXISTS `tbl_browsing_history`;
CREATE TABLE `tbl_browsing_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_ip` varchar(100) DEFAULT NULL,
  `user_account` varchar(100) DEFAULT NULL,
  `uri` varchar(255) DEFAULT NULL,
  `request_method` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `browsing_date` varchar(20) DEFAULT NULL,
  `browsing_time` varchar(20) DEFAULT NULL,
  `user_agent` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

#
# Data for table "tbl_browsing_history"
#

INSERT INTO `tbl_browsing_history` VALUES (1,'::1','ok','GET','/signin','200','20190801','192504','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'),(2,'::1','ok','POST','/admin/verifyCode','200','20190801','192505','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'),(3,'::1','ok','POST','/signin','200','20190801','192510','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'),(4,'::1','a123456','GET','/home','200','20190801','192512','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'),(5,'::1','a123456','GET','/extra','200','20190801','192611','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36');

#
# Structure for table "tbl_bug_list"
#

DROP TABLE IF EXISTS `tbl_bug_list`;
CREATE TABLE `tbl_bug_list` (
  `bug_id` int(11) NOT NULL AUTO_INCREMENT,
  `bug_find_by` int(11) NOT NULL,
  `bug_name` varchar(1024) NOT NULL,
  `bug_describe` text,
  `bug_solution` text,
  `bug_date_plan` date DEFAULT NULL,
  `bug_date_done` date DEFAULT NULL,
  `bug_user_done` int(11) NOT NULL,
  `bug_project_id` int(11) NOT NULL,
  `bug_status` int(11) DEFAULT NULL COMMENT '0=on,1=off',
  PRIMARY KEY (`bug_id`),
  UNIQUE KEY `bug_id` (`bug_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "tbl_bug_list"
#


#
# Structure for table "tbl_bug_track"
#

DROP TABLE IF EXISTS `tbl_bug_track`;
CREATE TABLE `tbl_bug_track` (
  `bug_id` int(11) NOT NULL AUTO_INCREMENT,
  `bug_date_receive` date DEFAULT NULL COMMENT '接收时间',
  `bug_find_by` int(11) NOT NULL COMMENT '接口人',
  `bug_component` int(11) NOT NULL COMMENT '问题所属模块',
  `component_belong` int(11) NOT NULL COMMENT '模块维护人',
  `component_community` varchar(256) DEFAULT NULL COMMENT '模块社区讨论(新功能开发)',
  `bug_project_id` int(11) NOT NULL COMMENT '项目名称',
  `project_version` varchar(16) NOT NULL COMMENT '所属版本',
  `bug_describe` text COMMENT '问题描述',
  `bug_level` int(11) DEFAULT NULL COMMENT '优先级:0=低,1=中,2=高,3=急',
  `bug_reason` text COMMENT '问题原因',
  `bug_solution` text COMMENT '解决措施',
  `bug_progress` text COMMENT '进展（6/10）',
  `bug_date_plan` date DEFAULT NULL COMMENT '承诺解决日期',
  `bug_date_done` date DEFAULT NULL COMMENT '实际解决日期',
  `bug_user_done` int(11) NOT NULL COMMENT '负责人',
  `bug_version` varchar(16) NOT NULL COMMENT '所属版本',
  PRIMARY KEY (`bug_id`),
  UNIQUE KEY `bug_id` (`bug_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

#
# Data for table "tbl_bug_track"
#

INSERT INTO `tbl_bug_track` VALUES (1,'2019-06-30',8,3,3,'非社区项目',2,'V1.0','',0,'','','0%','2019-07-01','2019-07-02',1,'V1.0.1'),(2,'2019-07-02',10,5,0,'非社区项目',5,'V1.0','sso',0,'127.0.0.1连不上','127.0.0.1连不上','50%','2019-07-02','2019-07-02',10,'V1.0.1'),(3,'2019-07-02',10,5,0,'非社区项目',5,'V1.0','sso',0,'','','0%','2019-07-02','2019-07-02',10,'V1.0.1'),(4,'2019-07-01',10,5,0,'非社区模块',5,'1.1','端口号冲突',0,'端口号冲突','端口号冲突','已解决','2019-07-01','2019-07-01',10,'1.1');

#
# Structure for table "tbl_component_maintenance"
#

DROP TABLE IF EXISTS `tbl_component_maintenance`;
CREATE TABLE `tbl_component_maintenance` (
  `comp_id` int(11) NOT NULL AUTO_INCREMENT,
  `comp_belong_to` int(11) DEFAULT NULL COMMENT 'user belong to this component',
  `comp_type` int(11) NOT NULL COMMENT '0=增加新功能,1=问题排查,2=优化调整,3=其他',
  `comp_new` text COMMENT '新功能内容',
  `comp_status` int(11) NOT NULL COMMENT '0=未解决,1=已解决',
  `comp_describe` text COMMENT '问题描述',
  `comp_reason` text COMMENT '问题原因',
  `comp_solution` text COMMENT '解决方式',
  `create_time` datetime DEFAULT NULL,
  `modify_time` datetime DEFAULT NULL,
  `comment` varchar(256) DEFAULT NULL COMMENT '备注,不超过200字',
  `user_belong_to` int(11) DEFAULT '0',
  PRIMARY KEY (`comp_id`),
  UNIQUE KEY `comp_id` (`comp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

#
# Data for table "tbl_component_maintenance"
#

INSERT INTO `tbl_component_maintenance` VALUES (1,5,1,'add new content',0,'# 创建数据库\r\ncreate database cmdb default charset utf8;','# 创建数据库\r\ncreate database cmdb default charset utf8;','# 创建数据库\r\ncreate database cmdb default charset utf8;','2019-07-02 14:07:11','2019-07-02 14:07:11','add new content',10),(2,4,0,'add new content cc',1,'','','','2019-07-02 10:19:50','2019-07-02 10:19:50','',5);

#
# Structure for table "tbl_discuss"
#

DROP TABLE IF EXISTS `tbl_discuss`;
CREATE TABLE `tbl_discuss` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) DEFAULT NULL COMMENT '话题',
  `discuss` text COMMENT '评论',
  `create` datetime DEFAULT NULL,
  `original` int(11) NOT NULL COMMENT '来源',
  `author` int(11) DEFAULT NULL COMMENT '作者',
  `status` int(11) DEFAULT NULL COMMENT '0=正常',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

#
# Data for table "tbl_discuss"
#

INSERT INTO `tbl_discuss` VALUES (1,1,'not like','2019-08-02 10:11:03',0,2,0),(2,1,'sub discuss','2019-08-02 10:58:43',1,2,0),(3,1,'sub discuss','2019-08-02 10:58:54',1,3,0),(4,1,'12','2019-08-02 16:11:06',1,1,0),(5,1,'测试','2019-08-02 16:27:34',1,1,0);

#
# Structure for table "tbl_post_list"
#

DROP TABLE IF EXISTS `tbl_post_list`;
CREATE TABLE `tbl_post_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent` int(11) NOT NULL,
  `author` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `title` text NOT NULL,
  `content` text,
  `excerpt` text,
  `status` varchar(20) DEFAULT NULL,
  `comment_status` varchar(20) DEFAULT NULL,
  `authorname` varchar(32) DEFAULT NULL,
  `guid` varchar(255) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `mime_type` varchar(20) DEFAULT NULL,
  `comment_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

#
# Data for table "tbl_post_list"
#

INSERT INTO `tbl_post_list` VALUES (1,1,1,'2017-12-30 01:00:00','2017-12-30 01:00:00','测试数据','内容测试','1','enabled','1','1','1','post',1,'1',1);

#
# Structure for table "tbl_project"
#

DROP TABLE IF EXISTS `tbl_project`;
CREATE TABLE `tbl_project` (
  `project_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(256) NOT NULL,
  `describe` text,
  `top_project_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `progress` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL COMMENT '0=enable,1=disable',
  PRIMARY KEY (`project_id`),
  UNIQUE KEY `project_name` (`project_name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

#
# Data for table "tbl_project"
#

INSERT INTO `tbl_project` VALUES (1,'ce','ceshi',0,1,'2019-01-16 14:05:34',0,0),(2,'ce1','ss',1,1,'2019-01-16 14:13:21',0,0),(3,'GCC','GCC测试',0,1,'2019-06-28 16:24:39',0,0),(4,'CBS','大数据服务器',0,1,'2019-07-01 15:34:56',0,0),(5,'kdfs','存储',4,1,'2019-07-01 16:47:28',0,0),(8,'tt','sdf',0,1,'2019-07-01 17:12:33',0,1);

#
# Structure for table "tbl_project_progress"
#

DROP TABLE IF EXISTS `tbl_project_progress`;
CREATE TABLE `tbl_project_progress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `modify_time` datetime DEFAULT NULL,
  `cur_progress` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "tbl_project_progress"
#


#
# Structure for table "tbl_project_user"
#

DROP TABLE IF EXISTS `tbl_project_user`;
CREATE TABLE `tbl_project_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `project_id` (`project_id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `tbl_project_user_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `tbl_project` (`project_id`),
  CONSTRAINT `tbl_project_user_ibfk_2` FOREIGN KEY (`account_id`) REFERENCES `tbl_account` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

#
# Data for table "tbl_project_user"
#

INSERT INTO `tbl_project_user` VALUES (1,3,10),(2,4,10),(3,4,1),(4,5,10),(5,8,1);

#
# Structure for table "tbl_topic"
#

DROP TABLE IF EXISTS `tbl_topic`;
CREATE TABLE `tbl_topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author` int(11) NOT NULL,
  `title` varchar(128) NOT NULL COMMENT '标题',
  `content` text COMMENT '内容',
  `discuss` int(11) DEFAULT NULL COMMENT '回复',
  `likes` int(11) DEFAULT NULL COMMENT '点赞',
  `status` int(11) DEFAULT NULL COMMENT '0=正常，1=删除',
  `category` int(11) DEFAULT NULL COMMENT '类别',
  `create` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

#
# Data for table "tbl_topic"
#

INSERT INTO `tbl_topic` VALUES (1,1,'python topic 2019-08-02 10:06:28.812836','topic中文',5,0,0,0,'2019-08-02 10:06:29');

CREATE TABLE `flight` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ifid` varchar(6) DEFAULT NULL,
  `ofid` varchar(6) DEFAULT NULL,
  `from` char(3) DEFAULT NULL,
  `to` char(3) DEFAULT NULL,
  `sta` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `eta` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `std` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `etd` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `checkinctr` text DEFAULT NULL,
  `status` enum('security','boarding','finalcall','bclosed') NOT NULL,
  `beltstatus` enum('delayed','ontime','early','dsted') NOT NULL,
  `gate` varchar(6) DEFAULT NULL,
  `belt` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1
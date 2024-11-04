CREATE TABLE `Orders` (
    `_id` varchar(255) PRIMARY KEY,
    `order_id` varchar(255),
    `type` varchar(255),
    `createdAt` datetime,
    `updatedAt` datetime,
    `collectedFromBusiness` datetime,
    `confirmation_id` varchar(255),
    `dropOffAddress_id` varchar(255),
    `pickupAddress_id` varchar(255),
    `receiver_id` varchar(255),
    `star_id` varchar(255),
    `tracker_id` varchar(255),
    `cod_id` varchar(255),
    # foreign keys
    CONSTRAINT `fk_orders_confirmation` FOREIGN KEY (`confirmation_id`) REFERENCES `Confirmation` (`_id`),
    CONSTRAINT `fk_orders_dropoffaddress` FOREIGN KEY (`dropOffAddress_id`) REFERENCES `Address` (`_id`),
    CONSTRAINT `fk_orders_pickupaddress` FOREIGN KEY (`pickupAddress_id`) REFERENCES `Address` (`_id`),
    CONSTRAINT `fk_orders_receiver` FOREIGN KEY (`receiver_id`) REFERENCES `Receiver` (`_id`),
    CONSTRAINT `fk_orders_star` FOREIGN KEY (`star_id`) REFERENCES `Star` (`_id`),
    CONSTRAINT `fk_orders_tracker` FOREIGN KEY (`tracker_id`) REFERENCES `Tracker` (`_id`),
    CONSTRAINT `fk_orders_cod` FOREIGN KEY (`cod_id`) REFERENCES `COD` (`_id`),
    # indexes
    INDEX `idx_orders_order_id` (`order_id`),
    INDEX `idx_orders_type` (`type`),
);

CREATE TABLE `COD` (
    `_id` varchar(255) PRIMARY KEY,
    `amount` int,
    `isPaidBack` tinyint(1),
    `collectedAmount` int
);

CREATE TABLE `Confirmation` (
    `_id` varchar(255) PRIMARY KEY,
    `isConfirmed` tinyint(1),
    `numberOfSmsTrials` int
);

CREATE TABLE `Address` (
    `_id` varchar(255) PRIMARY KEY,
    `floor` varchar(255),
    `apartment` varchar(255),
    `secondLine` varchar(255),
    `district` varchar(255),
    `firstLine` varchar(255),
    `geoLocation_lat` float,
    `geoLocation_long` float,
    `city_id` varchar(255),
    `zone_id` varchar(255),
    `country_id` varchar(255),
    # foreign keys
    CONSTRAINT `fk_address_city` FOREIGN KEY (`city_id`) REFERENCES `City` (`_id`),
    CONSTRAINT `fk_address_zone` FOREIGN KEY (`zone_id`) REFERENCES `Zone` (`_id`),
    CONSTRAINT `fk_address_country` FOREIGN KEY (`country_id`) REFERENCES `Country` (`_id`)
);

CREATE TABLE `City` (
    `_id` varchar(255) PRIMARY KEY,
    `name` varchar(255),
    # indexes
    INDEX `idx_city_name` (`name`)
);

CREATE TABLE `Zone` (
    `_id` varchar(255) PRIMARY KEY,
    `name` varchar(255),
    # indexes
    INDEX `idx_zone_name` (`name`)
);

CREATE TABLE `Country` (
    `_id` varchar(255) PRIMARY KEY,
    `name` varchar(255),
    `code` varchar(255),
    # indexes
    INDEX `idx_country_name` (`name`),
);

CREATE TABLE `Receiver` (
    `_id` varchar(255) PRIMARY KEY,
    `firstName` varchar(255),
    `lastName` varchar(255),
    `phone` varchar(255)
);

CREATE TABLE `Star` (
    `_id` varchar(255) PRIMARY KEY,
    `name` varchar(255),
    `phone` varchar(255)
);

CREATE TABLE `Tracker` (
    `_id` varchar(255) PRIMARY KEY,
    `trackerId` varchar(255),
    `order_id` varchar(255)
);

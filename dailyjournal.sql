CREATE TABLE `JournalEntry` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`date`	TEXT NOT NULL,
	`concept`	TEXT NOT NULL,
    `entry` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Mood` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`mood`	TEXT NOT NULL
);

INSERT INTO `JournalEntry` VALUES (null, "07/24/2025", "HTML & CSS", "We talked about HTML components and flexbox.", 2);
INSERT INTO `JournalEntry` VALUES (null, "07/15/2028", "Javascript Objects", "We talked about javascript objects.", 1);
INSERT INTO `JournalEntry` VALUES (null, "07/20/2014", "Git and Github", "We talked about proper workflow within a team.", 1);


INSERT INTO `Mood` VALUES (null, "Happy");
INSERT INTO `Mood` VALUES (null, "OK");
INSERT INTO `Mood` VALUES (null, "Frustrated");
INSERT INTO `Mood` VALUES (null, "Sad");
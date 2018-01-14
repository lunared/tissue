CREATE TABLE "Projects" ( `id` INTEGER, `name` TEXT NOT NULL, `description` TEXT, `homepage` TEXT, PRIMARY KEY(`id`) );
CREATE TABLE "Issues" ( `id` INTEGER, `project_id` INTEGER NOT NULL, `issue_num` INTEGER NOT NULL, `author` INTEGER NOT NULL, `email` TEXT, `title` TEXT, `body` TEXT, `opened` TEXT NOT NULL, `last_updated` TEXT NOT NULL, `state` TEXT DEFAULT 'Open', UNIQUE(`project_id`,`issue_num`), PRIMARY KEY(`id`), FOREIGN KEY(`project_id`) REFERENCES `Projects`(`id`) );
CREATE TABLE "Comments" ( `id` INTEGER, `issue_id` INTEGER, `author` TEXT NOT NULL, `email` TEXT, `body` TEXT NOT NULL, `created_at` TEXT NOT NULL, FOREIGN KEY(`issue_id`) REFERENCES `Issues`(`id`), PRIMARY KEY(`id`) );
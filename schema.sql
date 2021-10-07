BEGIN;
--
-- Create model TGMessage
--
CREATE TABLE "tg_message" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "id_msg" integer NOT NULL,
    "date_msg" datetime,
    "edited_msg" datetime,
    "from_author" varchar(200),
    "from_author_id" integer NOT NULL,
    "text_msg" varchar(4000),
    "tg_group_id" integer NOT NULL
);
CREATE UNIQUE INDEX tg_message_id_msg_from_author_id_tg_group_id_uindex
	ON "tg_message" ("id_msg", "from_author_id", "tg_group_id");
--
-- Create model UserAttribute
--
CREATE TABLE "user_attribute" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "from_author_id" integer NOT NULL,
    "name_attr" varchar(4000),
    "val_attr" varchar(4000)
);
CREATE UNIQUE INDEX user_attribute_from_author_id_name_attr_uindex
	ON "user_attribute" ("from_author_id", "name_attr");

COMMIT;

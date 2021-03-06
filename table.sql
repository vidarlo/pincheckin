CREATE TABLE "checkins" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user"	INTEGER,
	"checkin"	INTEGER,
	"checkout"	INTEGER,
	FOREIGN KEY("user") REFERENCES "users"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"email"	TEXT,
	"tag"	TEXT NOT NULL UNIQUE,
	"phone" TEXT,
	"name" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

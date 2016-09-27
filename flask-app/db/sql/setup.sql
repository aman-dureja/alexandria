CREATE TABLE books(
id INT NOT NULL AUTO_INCREMENT,
title TEXT,
author TEXT,
language TEXT,
difficulty_level TEXT,
times_subscribed INT,
PRIMARY KEY (id)
);

CREATE TABLE snippets(
id INT NOT NULL AUTO_INCREMENT,
book_id INT NOT NULL,
section INT,
content TEXT,
PRIMARY KEY (id)
);

CREATE TABLE users(
id INT NOT NULL AUTO_INCREMENT,
phone_number TEXT,
active_book_id INT NOT NULL,
book_section INT NOT NULL,
PRIMARY KEY ( id )
);

DROP TABLE if EXISTS post;
DROP TABLE if EXISTS user1;

CREATE TABLE "user1"(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL ,
    password TEXT NOT NULL
);

CREATE TABLE "post"(
    id SERIAL PRIMARY KEY,
    author_id INTEGER Not NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL ,
    constraint fk_author FOREIGN KEY (author_id) references user1 (id) on DELETE CASCADE
);

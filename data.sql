\c dndboards

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS boards;
DROP TABLE IF EXISTS pieces;

CREATE TABLE users (
    id serial PRIMARY KEY,
    usernameid text UNIQUE NOT NULL,
    username text NOT NULL,
    discriminator integer NOT NULL,
    role text NOT NULL,
    first_name text,
    last_name text,
    style text,
    join_date date DEFAULT CURRENT_DATE NOT NULL,
    last_login date
);

CREATE TABLE boards (
    id serial PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users,
    title text NOT NULL,
    link text NOT NULL
    )
);

CREATE TABLE pieces (
    id serial PRIMARY KEY,
    board_id integer NOT NULL REFERENCES boards,
    image text NOT NULL,
    content text NOT NULL,
    size text NOT NULL
    )
);
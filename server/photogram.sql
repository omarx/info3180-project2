-- Create a new database named Photogram
CREATE DATABASE photogram;

-- Connect to the database
\c photogram;

-- Create table "Users"
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    location VARCHAR(255),
    biography TEXT,
    profile_photo VARCHAR(255),
    joined_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create table "Posts"
CREATE TABLE Posts (
    id SERIAL PRIMARY KEY,
    caption TEXT,
    photo VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- Create table "Likes"
CREATE TABLE Likes (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- Create table "Follows"
CREATE TABLE Follows (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (follower_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

---------------------------------------------
-- Users Table
---------------------------------------------
-- If any other information is needed about the users, make another table. This is the minimum needed for authentication.
CREATE TABLE IF NOT EXISTS users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    EMAIL TEXT UNIQUE NOT NULL,
    HASHED_PASSWORD TEXT NOT NULL
);

---------------------------------------------
-- Token Signup Table
---------------------------------------------
CREATE TABLE IF NOT EXISTS token_signup (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    EMAIL TEXT UNIQUE NOT NULL,
    TOKEN TEXT UNIQUE NOT NULL,
    DURATION_SECONDS INTEGER DEFAULT 86400, -- 1 day

    -- Trigger columns
    CREATED_UNIX_TIME INTEGER,
    CREATED_DATETIME DATETIME,

    EXPIRATION_UNIX_TIME INTEGER,
    EXPIRATION_DATETIME DATETIME
);

CREATE TRIGGER token_signup_trigger
AFTER INSERT ON token_signup
FOR EACH ROW
BEGIN
    -- First update for the CREATED_UNIX_TIME
    UPDATE token_signup
    SET CREATED_UNIX_TIME = strftime('%s', 'now')
    WHERE ID = NEW.ID;

    -- Second update for all other fields (expiration times and datetimes)
    UPDATE token_signup
    SET 
        EXPIRATION_UNIX_TIME = CREATED_UNIX_TIME + NEW.DURATION_SECONDS,
        CREATED_DATETIME = strftime('%Y-%m-%d %H:%M:%S', datetime(CREATED_UNIX_TIME, 'unixepoch')),  -- Convert Unix timestamp to datetime format
        EXPIRATION_DATETIME = strftime('%Y-%m-%d %H:%M:%S', datetime(CREATED_UNIX_TIME + NEW.DURATION_SECONDS, 'unixepoch'))  -- Expiration converted to readable datetime format
    WHERE ID = NEW.ID;
END;

---------------------------------------------
-- Menu Table: Contains all the menu items
---------------------------------------------
CREATE TABLE IF NOT EXISTS menu (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    DESCRIPTION TEXT,
    PRICE REAL NOT NULL,
    IMAGE_URL TEXT
);


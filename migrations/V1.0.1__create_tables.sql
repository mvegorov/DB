

CREATE TABLE IF NOT EXISTS "User" (
    user_id INT PRIMARY KEY,
    user_name CHAR(50) NOT NULL,
    level CHAR(1),
    is_verified BOOLEAN,
    is_editor BOOLEAN,
    subscribe_end TIME
);

CREATE TABLE IF NOT EXISTS "Category" (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(256) NOT NULL
);

CREATE TABLE IF NOT EXISTS "Subcategory" (
    subcategory_id INT PRIMARY KEY,
    category_id INT REFERENCES "Category" (category_id) ON DELETE CASCADE,
    subcategory_name VARCHAR(256) NOT NULL
);

CREATE TABLE IF NOT EXISTS "Word" (
    word_id INT PRIMARY KEY,
    word VARCHAR(256) NOT NULL,
    meaning_A VARCHAR(256),
    meaning_B VARCHAR(256),
    meaning_C VARCHAR(256),
    level CHAR(1),
    subcategory_id INT REFERENCES "Subcategory" (subcategory_id),
    tags VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS "Collection" (
    collection_id INT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "User" (user_id),
    description VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS "Collections_Info" (
    word_id INT NOT NULL REFERENCES "Word" (word_id),
    collection_id INT NOT NULL REFERENCES "Collection" (collection_id),
    meaning VARCHAR(256),
    PRIMARY KEY (word_id, collection_id)
);

CREATE TABLE IF NOT EXISTS "Studying_session" (
    session_id INT PRIMARY KEY,
    collection_id INT NOT NULL REFERENCES "Collection" (collection_id),
    user_id INT NOT NULL REFERENCES "User" (user_id),
    time_start TIME,
    duration TIME,
    total_words INT
);

CREATE TABLE IF NOT EXISTS "Users_progress" (
    user_id INT NOT NULL REFERENCES "User" (user_id),
    word_id INT NOT NULL REFERENCES "Word" (word_id),
    last_success TIME NOT NULL,
    successes_in_row INT NOT NULL,
    PRIMARY KEY (user_id, word_id)
);

CREATE TABLE IF NOT EXISTS "Editing_log" (
    log_id INT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "User" (user_id),
    word_id INT NOT NULL REFERENCES "Word" (word_id),
    log_text VARCHAR(256)
);
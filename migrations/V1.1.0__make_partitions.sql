
CREATE TABLE IF NOT EXISTS users_verified (
    user_id INT PRIMARY KEY,
    user_name CHAR(50) NOT NULL,
    level CHAR(1),
    is_verified BOOLEAN,
    is_editor BOOLEAN,
    subscribe_end TIME,
    CHECK (is_verified = true)  -- Условие для партиции с проверенными пользователями
) INHERITS ("User");

CREATE TABLE IF NOT EXISTS users_unverified (
    user_id INT PRIMARY KEY,
    user_name CHAR(50) NOT NULL,
    level CHAR(1),
    is_verified BOOLEAN,
    is_editor BOOLEAN,
    subscribe_end TIME,
    CHECK (is_verified = false)  -- Условие для партиции с непроверенными пользователями
) INHERITS ("User");
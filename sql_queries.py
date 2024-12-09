create_table_user = """
CREATE TABLE IF NOT EXISTS profile(
    tg_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    name TEXT,
    age INTEGER,
    balance INTEGER DEFAULT 0 NOT NULL,
    is_admin BOOL DEFAULT 0 NOT NULL,
    referer_id INTEGER,
    FOREIGN KEY (referer_id) REFERENCES profile (tg_id)
);
"""

create_super_user = """
INSERT INTO profile (tg_id, username, is_admin)
VALUES ({}, '{}', 1)
ON CONFLICT(tg_id) 
DO NOTHING;
"""

create_table_move = """
CREATE TABLE IF NOT EXISTS acc_movements(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    money_flow INTEGER,
    profile_id INTEGER,
    FOREIGN KEY (profile_id) REFERENCES profile (tg_id)
);
"""
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

insert_user = """
INSERT INTO profile (tg_id, username, age, name, referer_id)
VALUES ({}, '{}', {}, '{}', {})
ON CONFLICT(tg_id) 
DO NOTHING;
"""

select_user_id = """
SELECT 1
FROM profile
WHERE tg_id = '{}'
"""

create_table_move = """
CREATE TABLE IF NOT EXISTS acc_movements(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    money_flow INTEGER,
    profile_id INTEGER,
    FOREIGN KEY (profile_id) REFERENCES profile (tg_id)
);
"""

select_user_balance = """
SELECT balance
FROM profile
WHERE tg_id = {}
"""

select_top_referals = """
SELECT p2.username, COUNT(*) as ref_count
FROM profile p1 
join profile p2 on p1.referer_id = p2.tg_id
GROUP BY p2.referer_id,  p2.username
ORDER BY ref_count DESC
LIMIT 10
"""

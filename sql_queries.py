create_table_user = """
CREATE TABLE IF NOT EXISTS profile(
    tg_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    name TEXT,
    age INTEGER,
    balance INTEGER DEFAULT 0 NOT NULL,
    is_admin BOOL DEFAULT 0 NOT NULL,
    is_blocked BOOL DEFAULT 0 NOT NULL,
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

create_table_switches = """
CREATE TABLE IF NOT EXISTS switches(
    id INTEGER PRIMARY KEY,    
    parameter TEXT UNIQUE NOT NULL,
    value BOOL DEFAULT 0 NOT NULL
);
"""

insert_registration_parameter = """
insert or replace into switches (parameter) 
values ('registration');
"""

insert_game_parameter = """
insert or replace into switches (parameter) 
values ('game');
"""

insert_user = """
INSERT INTO profile (tg_id, username, age, name, referer_id)
VALUES ({}, '{}', {}, '{}', {})
ON CONFLICT(tg_id) 
DO NOTHING;
"""

select_user_by_tg_id = """
SELECT 1
FROM profile
WHERE tg_id = {}
"""

select_user_by_username = """
SELECT 1
FROM profile
WHERE username = '{}'
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

increase_balance = """
UPDATE profile SET balance = balance + {} WHERE username = '{}'
"""

decrease_balance = """
UPDATE profile SET balance = balance - {} WHERE username = '{}'
"""

set_balance = """
UPDATE profile SET balance = {} WHERE username = '{}'
"""


select_user_by_tg_id = """
SELECT 1
FROM profile
WHERE tg_id = {}
"""


is_admin = """
SELECT 1
FROM profile
WHERE tg_id = {} AND
is_admin = 1
"""


select_all_users = """
SELECT tg_id, username, name
FROM profile
"""


block_user = """
UPDATE profile SET is_blocked = 1 WHERE username = '{}'
"""


is_blocked = """
SELECT 1
FROM profile
WHERE tg_id = {} AND
is_blocked = 1
"""


select_top_money_users = """
SELECT username, balance
FROM profile
ORDER BY balance DESC
"""

select_reg = """
SELECT value
FROM switches
where parameter = 'registration'
"""

select_game = """
SELECT value
FROM switches
where parameter = 'game'
"""

reg_off = """
UPDATE switches SET value = False WHERE parameter = 'registration'
"""

reg_on = """
UPDATE switches SET value = True WHERE parameter = 'registration'
"""

game_off = """
UPDATE switches SET value = False WHERE parameter = 'game'
"""

game_on = """
UPDATE switches SET value = True WHERE parameter = 'game'
"""
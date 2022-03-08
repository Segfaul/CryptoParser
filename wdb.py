import sqlite3
def Check_loc(db_name, tg_id):
    base = sqlite3.connect(f'{db_name}')
    cur = base.cursor()
    '''TEXT, INTEGER, REAL, BLOB, NULL'''  # Типы данных sqlite3(blob - любой тип, null - нулевой)
    base.execute('CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY, loc, lid)')
    base.commit()
    try:
        loc = cur.execute('SELECT loc FROM users WHERE id == ?', (f'{tg_id}',)).fetchone()[0]
    except: return -1
    finally: base.close()
    return loc
def Check_lid(db_name, tg_id):
    base = sqlite3.connect(f'{db_name}')
    cur = base.cursor()
    '''TEXT, INTEGER, REAL, BLOB, NULL'''  # Типы данных sqlite3(blob - любой тип, null - нулевой)
    base.execute('CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY, loc, lid)')
    base.commit()
    try:
        nid = cur.execute('SELECT lid FROM users WHERE id == ?', (f'{tg_id}',)).fetchone()[0]
    except: return -1
    finally: base.close()
    return nid
def Input_data(db_name, tg_id):
    base = sqlite3.connect(f'{db_name}')
    cur = base.cursor()
    '''TEXT, INTEGER, REAL, BLOB, NULL'''  # Типы данных sqlite3(blob - любой тип, null - нулевой)
    base.execute('CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY, loc, lid)')
    base.commit()
    try:
        cur.execute('INSERT INTO users VALUES(?, ?, ?)', (f'{tg_id}', f'{"none"}', 'none',))#Добавление 1 записи в таблицу
        base.commit()
    except: return 1
    finally: base.close()
    return 0
def Check_on_exist(db_name, tg_id):
    base = sqlite3.connect(f'{db_name}')
    cur = base.cursor()
    '''TEXT, INTEGER, REAL, BLOB, NULL'''  # Типы данных sqlite3(blob - любой тип, null - нулевой)
    base.execute('CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY, loc, lid)')
    base.commit()
    try:
        res = cur.execute('SELECT EXISTS(SELECT id FROM users WHERE id = ?)', (f'{tg_id}',)).fetchone()[0]
        base.commit()
    except: return 3
    finally: base.close()
    return res
def Change_loc(db_name, tg_id, loc):
    base = sqlite3.connect(f'{db_name}')
    cur = base.cursor()
    '''TEXT, INTEGER, REAL, BLOB, NULL'''  # Типы данных sqlite3(blob - любой тип, null - нулевой)
    base.execute('CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY, loc, lid)')
    base.commit()
    try:
        cur.execute('UPDATE users SET loc == ? WHERE id == ?', (f'{loc}', f'{tg_id}'))
        base.commit()
    except: return 1
    finally: base.close()
    return 0
def Change_lid(db_name, tg_id, lid):
    base = sqlite3.connect(f'{db_name}')
    cur = base.cursor()
    '''TEXT, INTEGER, REAL, BLOB, NULL'''  # Типы данных sqlite3(blob - любой тип, null - нулевой)
    base.execute('CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY, loc, lid)')
    base.commit()
    try:
        cur.execute('UPDATE users SET lid == ? WHERE id == ?', (f'{lid}', f'{tg_id}'))
        base.commit()
    except: return 1
    finally: base.close()
    return 0
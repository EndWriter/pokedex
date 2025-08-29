import sqlite3

# le fichier SQLite 
SQLITE_PATH = 'c:/Users/UIMM/Desktop/stage/Dernière dance/pokedex/database.sqlite'

def extract_sqlite_tables():
    conn = sqlite3.connect(SQLITE_PATH)
    cursor = conn.cursor()

    # les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("tables :", tables)

    # test extraction pour table
    for table_name, in tables:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"extrait {len(rows)}, nbr de ligne : {table_name}")

    conn.close()

if __name__ == '__main__':
    extract_sqlite_tables()

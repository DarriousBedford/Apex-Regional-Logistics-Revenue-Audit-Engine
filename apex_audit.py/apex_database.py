import sqlite3

DATABASE_FILE = 'apex.db' # sqlite file name

# creates and stores the tables
def create_schema():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    try:
        cur.execute('PRAGMA foreign_keys=ON')
        cur.execute('''CREATE TABLE IF NOT EXISTS Stores(
                        StoreID INTEGER PRIMARY KEY NOT NULL,
                        StoreName TEXT NOT NULL,
                        Region TEXT,
                        TierCode TEXT)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS Departments (
                        StoreID INTEGER,
                        DeptNumber INTEGER,
                        Sales REAL,
                        LedgerScan BLOB,
                        PRIMARY KEY(StoreID, DeptNumber),
                        FOREIGN KEY(StoreID) REFERENCES Stores(storeID))''')
        conn.commit()
    finally:
        conn.close()
def reset_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    try:
        cur.execute('DROP TABLE IF EXISTS Departments')
        cur.execute('DROP TABLE IF EXISTS Stores')
        cur.execute('DROP TABLE Archive')
        conn.commit()
    except sqlite3.Error as err:
        print(f'Database error: {err}')
    finally:
        conn.close()
def save_store(store_id, name, region, tier_code):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO Stores (StoreID, StoreName, Region, TierCode) VALUES (?, ?, ?, ?)',
                    (store_id, name, region, tier_code))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f'Store {store_id} already exists')
    finally:
        conn.close()


def save_department(store_id, dept_number, sales):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    try:
        cur.execute('PRAGMA foreign_keys=ON')
        cur.execute('INSERT INTO Departments (StoreID, DeptNumber, Sales) VALUES (?, ?, ?)',
                    (store_id, dept_number, sales))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f'Store {store_id}, Dept {dept_number} already exists')
    finally:
            conn.close()

def query_audit_results():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Stores')
        all_stores = cur.fetchall()
        print('All stores:', all_stores)

        cur.execute('SELECT StoreName, Region FROM Stores')
        print('Names and regions:', cur.fetchall())

        cur.execute('SELECT * FROM Stores WHERE StoreID == ?', (1,))
        print('Store 1 (==):', cur.fetchone())
        cur.execute('SELECT * FROM Stores WHERE StoreID = ?', (1,))
        print('Store 1 (=):', cur.fetchone())

        cur.execute('SELECT StoreName FROM Stores WHERE Region !=?', ('North',))
        print('Not North (!=):', cur.fetchall())
        cur.execute('SELECT StoreName FROM Stores WHERE Region <> ?', ('North',))
        print('Not North (<>):', cur.fetchall())

        cur.execute('SELECT * FROM Departments WHERE Sales > ?', (1000,))
        print('Sales > 1000:', cur.fetchall())
        cur.execute('SELECT * FROM Departments WHERE Sales < ?', (500,))
        print('Sales < 500:', cur.fetchall())
        cur.execute('SELECT * FROM Departments WHERE Sales >= ?', (500,))
        print('Sales >= 500:', cur.fetchall())
        cur.execute('SELECT * FROM Departments WHERE Sales <= ?', (500,))
        print('sales <= 500:', cur.fetchall())

        cur.execute('SELECT StoreName FROM Stores WHERE Region == ? AND TierCode == ?', ('North', 'A'))
        print('North AND Tier A:', cur.fetchall())
        cur.execute('SELECT StoreName FROM Stores WHERE Region == ? OR Region == ?', ('North', 'South'))
        print('North OR South:', cur.fetchall())
        cur.execute("SELECT StoreName FROM Stores WHERE NOT TierCode == 'C'")
        print('Not Tier C:', cur.fetchall())

        cur.execute('SELECT * FROM Stores WHERE lower(storeName) == ?',('store 1',))
        print('Case-insensitive match:', cur.fetchall())

        cur.execute("SELECT StoreName FROM Stores WHERE StoreName LIKE '%Depot%'")
        print('Contains Depot:', cur.fetchall())
        cur.execute("SELECT StoreName FROM Stores WHERE StoreName NOT LIKE '%Depot%'")
        print('No Depot:', cur.fetchall())

        cur.execute('SELECT * FROM Departments ORDER BY Sales DESC')
        print('Ranked departments:', cur.fetchall())

        cur.execute('SELECT AVG(Sales), SUM(Sales), MIN(Sales), MAX(Sales), COUNT(*) FROM Departments')
        print('Avg, Sum, Min, Max, Count:', cur.fetchone())

        cur.execute('SELECT RowID, StoreName FROM Stores')
        print('Row IDs:', cur.fetchall())
        return all_stores
    finally:
        conn.close()
def update_and_purge(store_id, new_tier):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    try:
        cur.execute('UPDATE Stores SET TierCode = ? WHERE StoreID == ?', (new_tier, store_id))
        print(f'Rows updated: {cur.rowcount}')
        cur.execute('DELETE FROM Departments WHERE Sales ==0')
        print(f'Rows deleted: {cur.rowcount}')
        conn.commit()
    finally:
        conn.close()

def regional_join_report():
    conn =sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    try:
        cur.execute('''SELECT Stores.StoreName, Departments.DeptNumber, Departments.Sales
                        FROM Stores, Departments
                        WHERE Stores.StoreID == Departments.StoreID''')
        for name, dept, sales in cur.fetchall():
            print(f'{name:<12} Dept {dept} {sales:>12,.2f}')
    finally:
        conn.close()
                    
                
            
                    
                        

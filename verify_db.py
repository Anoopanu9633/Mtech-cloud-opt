import sqlite3

conn = sqlite3.connect('cloud_cost_optimizer.db')
cursor = conn.cursor()

print('=== Database Tables ===')
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
    count = cursor.fetchone()[0]
    print(f'\n{table_name}: {count} records')
    
    # Show schema
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    print('  Columns:', ', '.join([col[1] for col in columns]))

conn.close()
print('\n✅ Database verification complete')

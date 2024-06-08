from sqlalchemy import create_engine, MetaData

# Replace with your actual connection details
DATABASE_URL = 'postgresql://quickassistdb_e8yi_user:GIj8c92qF31H7Y6KJPdqH8dyPN9jjrz8@dpg-cpi53luct0pc73fmg5c0-a.oregon-postgres.render.com/quickassistdb_e8yi'

# Create an engine
engine = create_engine(DATABASE_URL)

# Create a connection
connection = engine.connect()


# Reflect the database
metadata = MetaData()
metadata.reflect(bind=engine)

for table_name in metadata.tables.keys():
    table = metadata.tables[table_name]
    print(f"Table: {table_name}")
    
    # Get the columns of the table
    columns = table.columns.keys()
    print("Columns:")
    for column in columns:
        print(column)
    
    result = connection.execute(table.select())
    rows = result.fetchall()
    for row in rows:
        print(row)
    print("\n")

# Close the connection
connection.close()


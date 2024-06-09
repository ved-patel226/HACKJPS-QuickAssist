from sqlalchemy import create_engine, MetaData


DATABASE_URL = 'postgresql://quickassistdb_h5bg_user:BQTkvSdgb5vOnlJyuaFeth6YWihiQ9jN@dpg-cpiant4f7o1s73bf1c80-a.oregon-postgres.render.com/quickassistdb_h5bg'


engine = create_engine(DATABASE_URL)

connection = engine.connect()

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

connection.close()


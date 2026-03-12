from sqlalchemy import create_engine, text

server = "PC-PRACCOM\SQLEXPRESS"
database = "DATA_WAREHOUSE"

connection_string = (
    "mssql+pyodbc://@"+server+"/"+database+
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

engine = create_engine(connection_string)

with engine.begin() as conn:

    print("Ejecutando Data Warehouse...")

    conn.execute(text("EXEC sp_cargar_dw"))

print("DW actualizado correctamente")
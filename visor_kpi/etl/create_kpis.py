from sqlalchemy import create_engine, text

server = "PC-PRACCOM\SQLEXPRESS"
database = "DATA_WAREHOUSE"

connection_string = (
    "mssql+pyodbc://@"+server+"/"+database+
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

engine = create_engine(connection_string)

print("Creando KPIs...")

with open("sql/create_kpis.sql") as f:
    sql = f.read()

with engine.begin() as conn:
    for statement in sql.split("GO"):
        if statement.strip():
            conn.execute(text(statement))

print("KPIs creados correctamente")
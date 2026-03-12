import pandas as pd
from sqlalchemy import create_engine, text

# Ruta del Excel
excel_file = r"C:/Users/prac.rparedes/Documents/Proyectos/excel-to-kpi-dashboard/visor_kpi/data/raw/DATA_WAREHOUSE.xlsx"

# Conexión SQL Server
server = "PC-PRACCOM\SQLEXPRESS"
database = "DATA_WAREHOUSE"

connection_string = (
    "mssql+pyodbc://@"+server+"/"+database+
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

engine = create_engine(connection_string)

# Hojas del Excel
tables = {
    "DIM_CLIENTE": "stg.DIM_CLIENTE",
    "DIM_TIPO_CONTRATO": "stg.DIM_TIPO_CONTRATO",
    "DIM_MERCADO": "stg.DIM_MERCADO",
    "DIM_TIPO_CENTRAL": "stg.DIM_TIPO_CENTRAL",
    "DIM_CENTRAL": "stg.DIM_CENTRAL",
    "DIM_CONCEPTO": "stg.DIM_CONCEPTO",
    "DIM_DIVISION": "stg.DIM_DIVISION",
    "DIM_FRECUENCIA": "stg.DIM_FRECUENCIA",
    "DIM_FECHA": "stg.DIM_FECHA",
    "CONTRATO": "stg.CONTRATO",
    "ACTIVIDAD": "stg.ACTIVIDAD",
    "FACT_VENTA": "stg.FACT_VENTA",
    "FACT_COMPRA": "stg.FACT_COMPRA",
    "FACT_PRODUCCION": "stg.FACT_PRODUCCION",
    "FACT_CONSUMO_TIPO_CENTRAL": "stg.FACT_CONSUMO_TIPO_CENTRAL",
    "FACT_MOVIMIENTO_CONCEPTO": "stg.FACT_MOVIMIENTO_CONCEPTO",
    "FACT_INDICADOR_MENSUAL": "stg.FACT_INDICADOR_MENSUAL"
}

with engine.begin() as conn:

    for sheet, table in tables.items():

        print(f"Cargando {sheet} → {table}")

        # Limpiar staging
        conn.execute(text(f"DELETE FROM {table}"))

        # Leer Excel
        df = pd.read_excel(excel_file, sheet_name=sheet)

        # Insertar datos
        df.to_sql(
            table.split(".")[1],
            conn,
            schema="stg",
            if_exists="append",
            index=False
        )

print("Carga STG completada.")
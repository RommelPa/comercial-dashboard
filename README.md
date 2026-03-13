# ⚡ excel-to-kpi-dashboard | Energy DW Analytics

Proyecto de portafolio orientado a **Data Engineering + Analytics Engineering + BI**.

## Arquitectura

```text
Excel (DATA_WAREHOUSE.xlsx)
   ↓
ETL Python (load_stg.py → run_dw.py → create_kpis.py)
   ↓
SQL Server DATA_WAREHOUSE (stg, dim, fact, kpi)
   ↓
Streamlit Dashboard
```

## Pipeline ETL

El pipeline ETL existente se ejecuta con:

```bash
python -m etl.pipeline
```

> Este repositorio mantiene el ETL sin cambios y consume datos desde el esquema `kpi`.

## Conexión SQL Server del dashboard

La aplicación usa **Windows Authentication** y conexión centralizada en `visor_kpi/src/database.py`:

```python
server = "PC-PRACCOM\\SQLEXPRESS"
database = "DATA_WAREHOUSE"

connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)
```

## Vistas KPI consumidas por la app

- `kpi.vw_ventas_mensuales`
- `kpi.vw_margen_cliente`
- `kpi.vw_produccion_por_central`
- `kpi.vw_balance_compra_venta`
- `kpi.vw_actividades_por_division`

Definidas/actualizadas en:

- `visor_kpi/sql/views_dashboard.sql`

## Páginas del dashboard

- `Overview`
- `Comercial`
- `Operaciones`
- `Gestión de obligaciones`

## Ejecutar

```bash
streamlit run visor_kpi/app.py
```

## Screenshots (placeholders)

- `![Overview](docs/screenshots/overview.png)`
- `![Comercial](docs/screenshots/comercial.png)`
- `![Operaciones](docs/screenshots/operaciones.png)`
- `![Gestión](docs/screenshots/gestion.png)`

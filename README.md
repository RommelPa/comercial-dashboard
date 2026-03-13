# ⚡ Comercial Dashboard | BI End-to-End

Proyecto de **Data Engineering + BI** con flujo productivo:

```text
Excel
  → ETL Python
  → SQL Server Data Warehouse (stg, dim, fact, kpi)
  → Streamlit Dashboard
```

## Arquitectura

- **Fuente**: Excel (`visor_kpi/data/raw/DATA_WAREHOUSE.xlsx`).
- **Pipeline ETL**:
  1. `etl.load_stg` (carga `stg`)
  2. `etl.run_dw` (transforma a `dim` y `fact`)
  3. `etl.create_kpis` (crea vistas en `kpi`)
- **Dashboard**: Streamlit multipágina consumiendo vistas del schema `kpi` vía `src/data_access.py`.

## Estructura final

```text
visor_kpi/
  app.py
  pages/
    1_Overview.py
    2_Comercial.py
    3_Operaciones.py
    4_Gestion_obligaciones.py
  src/
    database.py
    data_access.py
    queries.py
    charts.py
    filters.py
  etl/
    pipeline.py
    load_stg.py
    run_dw.py
    create_kpis.py
  sql/
    sp_cargar_dw.sql
    views_dashboard.sql
    create_kpis.sql
  assets/
    style.css
  tests/
    test_smoke_dashboard_modules.py
```

## Esquemas del DW

- `stg`: staging cargado desde Excel.
- `dim`: dimensiones de negocio.
- `fact`: tablas de hechos.
- `kpi`: vistas analíticas para BI.

## Requisitos

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Dependencias principales:
- `streamlit`
- `pandas`
- `sqlalchemy`
- `pyodbc`
- `plotly`
- `openpyxl`

## Cómo ejecutar el pipeline

Desde la raíz del repo:

```bash
cd visor_kpi
python -m etl.pipeline
```

## Cómo ejecutar el dashboard

Desde la raíz del repo:

```bash
streamlit run visor_kpi/app.py
```

Configurar `.streamlit/secrets.toml` con:

```toml
[db]
server = "PC-PRACCOM\\SQLEXPRESS"
database = "DATA_WAREHOUSE"
driver = "ODBC Driver 17 for SQL Server"
```

La conexión usa `trusted_connection=yes`.

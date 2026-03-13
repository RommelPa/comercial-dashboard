from pathlib import Path


def test_core_structure_exists():
    required = [
        Path('visor_kpi/app.py'),
        Path('visor_kpi/src/database.py'),
        Path('visor_kpi/src/data_access.py'),
        Path('visor_kpi/src/queries.py'),
        Path('visor_kpi/src/charts.py'),
        Path('visor_kpi/src/filters.py'),
        Path('visor_kpi/etl/pipeline.py'),
        Path('visor_kpi/etl/load_stg.py'),
        Path('visor_kpi/etl/run_dw.py'),
        Path('visor_kpi/etl/create_kpis.py'),
    ]
    for path in required:
        assert path.exists(), f'Missing required file: {path}'

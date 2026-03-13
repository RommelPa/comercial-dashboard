import subprocess
import sys


def run_stage(module: str, label: str) -> None:
    print(label)
    subprocess.run([sys.executable, "-m", module], check=True)


if __name__ == "__main__":
    print("----- INICIANDO PIPELINE -----")
    run_stage("etl.load_stg", "1️⃣ Cargando STG...")
    run_stage("etl.run_dw", "2️⃣ Procesando Data Warehouse...")
    run_stage("etl.create_kpis", "3️⃣ Creando KPIs...")
    print("PIPELINE COMPLETADO")

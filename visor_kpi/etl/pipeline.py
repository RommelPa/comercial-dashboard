import subprocess
import sys

print("----- INICIANDO PIPELINE -----")

print("1️⃣ Cargando STG...")
subprocess.run([sys.executable, "-m", "etl.load_stg"])

print("2️⃣ Procesando Data Warehouse...")
subprocess.run([sys.executable, "-m", "etl.run_dw"])

print("3️⃣ Creando KPIs...")
subprocess.run([sys.executable, "-m", "etl.create_kpis"])

print("PIPELINE COMPLETADO")
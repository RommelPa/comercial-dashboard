"""
generate_mock_data.py
=====================
Genera datos mock realistas para el Visor KPI Comercial.
Empresa ficticia: Distribuidora Del Sur S.A.
Período: Enero 2023 – Marzo 2026 (27 meses completos + mes en curso)

Ejecutar desde la raíz del proyecto:
    python data/mock/generate_mock_data.py
"""

import os
import sys
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# ── Reproducibilidad ────────────────────────────────────────
random.seed(42)
np.random.seed(42)
fake = Faker("es_AR")
fake.seed_instance(42)

# ── Período ──────────────────────────────────────────────────
FECHA_INICIO = date(2023, 1, 1)
FECHA_FIN    = date(2026, 3, 8)   # "hoy" para el demo

# ── Directorio de salida ─────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR  = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "mock_data.xlsx")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# 1. VENDEDORES
# ═══════════════════════════════════════════════════════════════

def generar_vendedores() -> pd.DataFrame:
    """12 vendedores con perfiles de rendimiento diferenciados."""
    vendedores = [
        # id          nombre                          zona          perfil         obj_base    antig  sup
        ("V001", "Martín Eduardo Gómez",        "GBA Norte", "estrella",     2_200_000,  8, "SUP01", True),
        ("V002", "Laura Beatriz Fernández",     "GBA Norte", "estrella",     2_100_000,  6, "SUP01", True),
        ("V003", "Diego Alberto Ramírez",       "GBA Sur",   "estrella",     2_000_000, 10, "SUP02", True),
        ("V004", "Ana María Rodríguez",         "GBA Norte", "estable",      1_800_000,  5, "SUP01", True),
        ("V005", "Carlos Héctor López",         "GBA Sur",   "estable",      1_600_000,  7, "SUP02", True),
        ("V006", "Sandra Verónica Martínez",    "Interior",  "estable",      1_400_000,  4, "SUP02", True),
        ("V007", "Roberto Javier Sánchez",      "Interior",  "estable",      1_300_000,  3, "SUP02", True),
        ("V008", "Valeria Noelia Torres",       "GBA Norte", "desarrollo",   1_100_000,  2, "SUP01", True),
        ("V009", "Lucas Damián Ruiz",           "GBA Sur",   "desarrollo",   1_000_000,  2, "SUP02", True),
        ("V010", "Gabriela Inés Flores",        "Interior",  "desarrollo",     900_000,  1, "SUP02", True),
        ("V011", "Sebastián Omar García",       "GBA Norte", "problematico", 1_200_000,  3, "SUP01", True),
        ("V012", "Patricia Elena Vargas",       "GBA Sur",   "problematico", 1_100_000, 12, "SUP02", False),
    ]
    df = pd.DataFrame(vendedores, columns=[
        "id_vendedor", "nombre_completo", "zona", "perfil",
        "objetivo_mensual_base", "antiguedad_años", "supervisor_id", "activo"
    ])
    return df


# ═══════════════════════════════════════════════════════════════
# 2. CLIENTES
# ═══════════════════════════════════════════════════════════════

NOMBRES_CLIENTES = [
    # Tradicional
    "Almacén Don Pedro", "Super La Esquina", "Kiosco El Sol", "Minimercado López",
    "Despensa San Martín", "Almacén El Progreso", "Super Familiar Ruiz", "Kiosco La Esperanza",
    "Minimercado Torres", "Despensa La Fortuna", "Almacén Los Andes", "Super Don Carlos",
    "Kiosco El Parque", "Minimercado González", "Despensa El Centro", "Almacén La Paz",
    "Super Barrio Norte", "Kiosco Las Flores", "Minimercado Del Sur", "Despensa La Amistad",
    "Almacén San José", "Super El Barrio", "Kiosco Primavera", "Minimercado La Unión",
    "Despensa Los Pinos", "Almacén El Carmen", "Super Don Miguel", "Kiosco La Victoria",
    "Minimercado Flores", "Despensa El Jardín", "Almacén La Estrella", "Super Don Roberto",
    "Kiosco El Cielo", "Minimercado Palermo", "Despensa Los Cedros", "Almacén El Triunfo",
    "Super La Paloma", "Kiosco El Roble", "Minimercado Villa", "Despensa Los Álamos",
    "Almacén San Pedro", "Super El Ombú", "Kiosco La Armonía", "Minimercado Central",
    "Despensa La Colina", "Almacén Villa Nueva", "Super Don Luis", "Kiosco El Laurel",
    "Minimercado Rivadavia", "Despensa El Manantial", "Almacén La Cruz", "Super Don Héctor",
    "Kiosco El Árbol", "Minimercado Sarmiento", "Despensa El Faro", "Almacén La Cima",
    "Super Don Antonio", "Kiosco El Nido", "Minimercado Moreno", "Despensa La Cumbre",
    "Almacén El Puente", "Super El Palo Verde", "Kiosco La Sierra", "Minimercado Güemes",
    "Despensa El Rancho", "Almacén La Pampa", "Super Don Jorge", "Kiosco El Molino",
    "Minimercado Belgrano", "Despensa La Pradera", "Almacén El Portal", "Super Don Oscar",
    "Kiosco La Ruta", "Minimercado Mitre", "Despensa La Loma", "Almacén El Puesto",
    "Super Don Fernando", "Kiosco El Campo", "Minimercado San Juan", "Despensa El Otoño",
    "Almacén La Rivera", "Super El Trigal", "Kiosco La Pampa", "Minimercado Corrientes",
    "Despensa La Cantera", "Almacén El Rancho", "Super Don Ramón", "Kiosco El Potrero",
    "Minimercado Tucumán", "Despensa El Bosque", "Almacén La Quebrada",
    # Supermercados
    "Supermercado El Sol S.A.", "Hipermercado Norte", "Super Mayorista Palermo",
    "Carrefour Express Villa", "Supermercado Día Belgrano", "Super Vea Quilmes",
    "Hipermercado Sur", "Supermercado La Cadena", "Super Express Lomas",
    "Supermercado El Trébol", "Hipermercado Centro", "Super La Red Avellaneda",
    "Supermercado Ahorro Plus", "Super Familiar La Plata", "Disco Express Sur",
    "Supermercado Cordiez", "Super Nini Wilde", "Hipermercado Del Valle",
    "Supermercado Marsupi", "Super El Timón", "Supermercado Roa", "Soper La Bahía",
    "Supermercado Los Piletones", "Super El Navegante", "Hipermercado Oeste",
    "Supermercado Vital", "Super La Patagonia", "Supermercado El Arca",
    "Super Multiahorro Mar del Plata", "Supermercado Full", "Supermercado Fresh",
    "Super La Abundancia", "Supermercado Premier", "Hipermercado Bonaerense",
    "Super Ahorrista", "Supermercado El Puente",
    # Mayoristas
    "Distribuidora García Hnos.", "Mayorista El Depósito", "Cash&Carry Norte",
    "Makro Quilmes", "Distribuidora López S.R.L.", "Mayorista Del Sur",
    "Centro Mayorista Palermo", "Distribuidora Gómez", "Mayorista La Bodega",
    "Distribuidora Torres S.A.", "Cash Mayorista Lomas", "Makro Interior",
    "Distribuidora Ramírez", "Mayorista El Almacén Grande", "Distribuidora Flores",
    "Mayorista El Surtidor", "Distribuidora Vargas", "Bodega Mayorista Sur",
    "Distribuidora Ruiz Hnos.", "Mayorista Central", "Distribuidora Martínez",
    "Mayorista El Proveedor", "Distribuidora Rodríguez", "Mayorista La Fuente",
    "Distribuidora Sánchez", "Mayorista El Nodo", "Centro Distribuidor Norte",
    # HoReCa
    "Restaurante La Pergola", "Hotel Meridian Buenos Aires", "Cafetería El Encuentro",
    "Pizzería Don Pepito", "Restaurant El Gaucho", "Parrilla Los Amigos",
    "Hotel Costa del Sol", "Confitería La Giralda", "Restaurant El Rancho",
    "Bar El Bodegón", "Hotel Plaza Belgrano", "Cafetería Central",
    "Restaurant Mar y Tierra", "Parrilla El Asador", "Hotel Del Centro",
    "Bar La Esquina Italiana", "Restaurant Don Quijote", "Confitería La Flor",
    "Pizzería El Horno", "Hotel Savoy Quilmes", "Bar El Almacén",
    "Restaurant Los Compadres", "Parrilla El Chiripá", "Hotel La Ribera",
    "Cafetería El Momento", "Restaurant Buenos Días", "Bar El Fortín",
]


def generar_clientes(df_vendedores: pd.DataFrame) -> pd.DataFrame:
    """
    180 clientes distribuidos por canal y asignados a vendedores.
    Canal:      Trad=90, Super=36, Mayor=27, HoReCa=27
    Inactivos:  15% = 27 clientes
    """
    canales_config = [
        ("Canal Tradicional",  90, (50_000,  300_000)),
        ("Supermercadismo",    36, (200_000, 800_000)),
        ("Mayorista",          27, (150_000, 600_000)),
        ("HoReCa",             27, (50_000,  250_000)),
    ]

    vendedores_por_zona = df_vendedores[df_vendedores["activo"]].groupby("zona")["id_vendedor"].apply(list).to_dict()

    clientes = []
    cli_idx  = 0
    nombre_idx = 0

    # Índices de nombres por categoría
    nombres_trad  = NOMBRES_CLIENTES[:90]
    nombres_super = NOMBRES_CLIENTES[90:126]
    nombres_mayor = NOMBRES_CLIENTES[126:153]
    nombres_horeca = NOMBRES_CLIENTES[153:]
    nombres_por_canal = {
        "Canal Tradicional": nombres_trad,
        "Supermercadismo":   nombres_super,
        "Mayorista":         nombres_mayor,
        "HoReCa":            nombres_horeca,
    }

    # 27 inactivos distribuidos proporcionalmente
    inactivos_set = set()

    for canal, n, (obj_min, obj_max) in canales_config:
        n_inact = round(n * 0.15)
        inact_positions = set(random.sample(range(n), n_inact))

        names_pool = nombres_por_canal[canal]

        for i in range(n):
            cli_idx += 1
            cli_id = f"CLI{cli_idx:03d}"

            # Asignar zona aleatoriamente con pesos
            zona = random.choices(
                ["GBA Norte", "GBA Sur", "Interior"],
                weights=[4, 3, 3]
            )[0]

            # Vendedor de esa zona (o cualquiera si no hay)
            vendedores_zona = vendedores_por_zona.get(zona, [])
            if not vendedores_zona:
                vendedores_zona = df_vendedores[df_vendedores["activo"]]["id_vendedor"].tolist()
            vendedor = random.choice(vendedores_zona)

            activo = i not in inact_positions

            # Fecha de alta escalonada a lo largo del período
            dias_total = (FECHA_FIN - FECHA_INICIO).days
            fecha_alta = FECHA_INICIO + timedelta(days=random.randint(0, int(dias_total * 0.7)))

            nombre = names_pool[i % len(names_pool)]

            clientes.append({
                "id_cliente":               cli_id,
                "razon_social":             nombre,
                "canal":                    canal,
                "zona":                     zona,
                "id_vendedor_asignado":     vendedor,
                "objetivo_mensual_cliente": round(random.randint(obj_min, obj_max), -3),
                "fecha_alta":               fecha_alta,
                "activo":                   activo,
                "categoria_pareto":         None,  # se calcula después
            })

    df = pd.DataFrame(clientes)
    return df


# ═══════════════════════════════════════════════════════════════
# 3. PRODUCTOS
# ═══════════════════════════════════════════════════════════════

PRODUCTOS_CATALOGO = [
    # (descripcion, categoria, precio, unidad)
    # Lácteos (10)
    ("Leche Entera Sachet 1L",     "Lácteos",    950,  "unidad"),
    ("Leche Descremada Sachet 1L", "Lácteos",    980,  "unidad"),
    ("Yogur Entero Frutado 200g",  "Lácteos",    680,  "unidad"),
    ("Yogur Bebible 1kg",          "Lácteos",    1250, "unidad"),
    ("Queso Cremoso x400g",        "Lácteos",    2800, "unidad"),
    ("Queso Rallado x100g",        "Lácteos",    1350, "unidad"),
    ("Manteca x200g",              "Lácteos",    2100, "unidad"),
    ("Crema de Leche x200ml",      "Lácteos",    1150, "unidad"),
    ("Dulce de Leche Repostero 1kg","Lácteos",   2600, "unidad"),
    ("Leche UHT Caja 1L",          "Lácteos",    1050, "caja"),
    # Almacén (15)
    ("Aceite Girasol 1.5L",        "Almacén",    3200, "unidad"),
    ("Aceite de Oliva 500ml",      "Almacén",    5800, "unidad"),
    ("Yerba Mate 500g",            "Almacén",    2100, "unidad"),
    ("Yerba Mate Selección 1kg",   "Almacén",    3900, "unidad"),
    ("Azúcar Blanca 1kg",          "Almacén",    1100, "unidad"),
    ("Harina 0000 1kg",            "Almacén",    890,  "unidad"),
    ("Arroz Largo Fino 1kg",       "Almacén",    1200, "unidad"),
    ("Fideos Spaghetti 500g",      "Almacén",    780,  "unidad"),
    ("Fideos Moñito 500g",         "Almacén",    780,  "unidad"),
    ("Puré de Tomate 520g",        "Almacén",    950,  "unidad"),
    ("Tomate Triturado 390g",      "Almacén",    870,  "unidad"),
    ("Sal Fina 500g",              "Almacén",    560,  "unidad"),
    ("Galletitas Surtidas 200g",   "Almacén",    850,  "unidad"),
    ("Mermelada Durazno 454g",     "Almacén",    1380, "unidad"),
    ("Mayonesa 500g",              "Almacén",    2100, "unidad"),
    # Bebidas (15)
    ("Agua Mineral 2.25L",         "Bebidas",    780,  "unidad"),
    ("Agua Saborizada 1.5L",       "Bebidas",    950,  "unidad"),
    ("Gaseosa Cola 2.25L",         "Bebidas",    1450, "unidad"),
    ("Gaseosa Lima Limón 2.25L",   "Bebidas",    1450, "unidad"),
    ("Gaseosa Naranja 1.5L",       "Bebidas",    1350, "unidad"),
    ("Jugo en Polvo 20g",          "Bebidas",    480,  "unidad"),
    ("Jugo Exprimido 1L",          "Bebidas",    1850, "unidad"),
    ("Cerveza Lager 1L Retornable","Bebidas",    1650, "unidad"),
    ("Cerveza Rubia Lata 473ml",   "Bebidas",    1150, "unidad"),
    ("Vino Tinto Tetra 1L",        "Bebidas",    1950, "unidad"),
    ("Vino Blanco Tetra 1L",       "Bebidas",    1950, "unidad"),
    ("Soda 2.25L",                 "Bebidas",    680,  "unidad"),
    ("Energizante 473ml",          "Bebidas",    2200, "unidad"),
    ("Té 25 saquitos",             "Bebidas",    1250, "unidad"),
    ("Café Molido 250g",           "Bebidas",    3100, "unidad"),
    # Limpieza (10)
    ("Lavandina 1L",               "Limpieza",   890,  "unidad"),
    ("Detergente Vajilla 500ml",   "Limpieza",   1350, "unidad"),
    ("Jabón en Polvo 1kg",         "Limpieza",   2800, "unidad"),
    ("Suavizante Ropa 900ml",      "Limpieza",   2600, "unidad"),
    ("Limpiador Multiuso 500ml",   "Limpieza",   1450, "unidad"),
    ("Lustramuebles 400ml",        "Limpieza",   1650, "unidad"),
    ("Desengrasante 500ml",        "Limpieza",   1550, "unidad"),
    ("Enjuague Bucal 350ml",       "Limpieza",   2100, "unidad"),
    ("Esponja Doble Faz x3",       "Limpieza",   980,  "unidad"),
    ("Bolsas Residuos x10 60L",    "Limpieza",   1100, "unidad"),
    # Perfumería (10)
    ("Shampoo 400ml",              "Perfumería", 3200, "unidad"),
    ("Acondicionador 400ml",       "Perfumería", 3400, "unidad"),
    ("Jabón de Tocador x3",        "Perfumería", 1650, "unidad"),
    ("Desodorante Aerosol 150ml",  "Perfumería", 2800, "unidad"),
    ("Crema Corporal 400ml",       "Perfumería", 4200, "unidad"),
    ("Afeitadora Desechable x3",   "Perfumería", 2100, "unidad"),
    ("Pasta Dental 90ml",          "Perfumería", 1850, "unidad"),
    ("Cepillo Dental",             "Perfumería", 1450, "unidad"),
    ("Papel Higiénico x4",         "Perfumería", 2200, "unidad"),
    ("Pañuelos Descartables x30",  "Perfumería", 890,  "unidad"),
]


def generar_productos() -> pd.DataFrame:
    productos = []
    for i, (desc, cat, precio, unidad) in enumerate(PRODUCTOS_CATALOGO):
        prd_id = f"PRD{i+1:03d}"
        costo_pct = random.uniform(0.55, 0.75)
        # 20% de productos con baja rotación → tendrán menos ventas
        baja_rotacion = i >= 48  # últimos 12 productos
        productos.append({
            "id_producto":    prd_id,
            "descripcion":    desc,
            "categoria":      cat,
            "precio_unitario": precio,
            "costo_unitario":  round(precio * costo_pct),
            "unidad_medida":   unidad,
            "activo":          True,
            "baja_rotacion":   baja_rotacion,
        })
    return pd.DataFrame(productos)


# ═══════════════════════════════════════════════════════════════
# 4. OBJETIVOS MENSUALES
# ═══════════════════════════════════════════════════════════════

def generar_objetivos(df_vendedores: pd.DataFrame) -> pd.DataFrame:
    """Objetivo mensual por vendedor, con aumento del 5% anual."""
    meses = _generar_lista_meses()
    rows = []
    for _, v in df_vendedores.iterrows():
        obj_base = v["objetivo_mensual_base"]
        for mes in meses:
            anios_transcurridos = (mes.year - FECHA_INICIO.year) + (mes.month - FECHA_INICIO.month) / 12
            obj = round(obj_base * (1.05 ** anios_transcurridos), -3)
            rows.append({
                "id_vendedor": v["id_vendedor"],
                "año":         mes.year,
                "mes":         mes.month,
                "periodo":     mes,
                "objetivo":    obj,
            })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════
# 5. TRANSACCIONES
# ═══════════════════════════════════════════════════════════════

# Factores de estacionalidad por mes
ESTACIONALIDAD = {
    1: 1.25,  # enero
    2: 1.00,
    3: 1.05,
    4: 1.00,
    5: 1.05,
    6: 0.95,
    7: 0.85,  # julio
    8: 0.95,
    9: 1.00,
    10: 1.05,
    11: 1.10,
    12: 1.25, # diciembre
}

# Frecuencia de compra mensual por canal (min, max) de transacciones por cliente
FRECUENCIA_CANAL = {
    "Canal Tradicional": (1, 2),
    "Supermercadismo":   (3, 4),
    "Mayorista":         (2, 3),
    "HoReCa":            (1, 2),
}

# Descuento promedio por canal
DESCUENTO_CANAL = {
    "Canal Tradicional": (0.00, 0.03),
    "Supermercadismo":   (0.05, 0.08),
    "Mayorista":         (0.08, 0.12),
    "HoReCa":            (0.00, 0.05),
}

# Pesos de categorías por canal
MEZCLA_PRODUCTOS = {
    "Canal Tradicional": {"Lácteos": 15, "Almacén": 40, "Bebidas": 20, "Limpieza": 15, "Perfumería": 10},
    "Supermercadismo":   {"Lácteos": 20, "Almacén": 25, "Bebidas": 25, "Limpieza": 20, "Perfumería": 10},
    "Mayorista":         {"Lácteos": 10, "Almacén": 40, "Bebidas": 30, "Limpieza": 15, "Perfumería":  5},
    "HoReCa":            {"Lácteos": 10, "Almacén": 20, "Bebidas": 50, "Limpieza": 15, "Perfumería":  5},
}

# Perfiles de performance → factor multiplicador mensual
PERFILES_FACTOR = {
    "estrella":     {"base": 1.20, "sd": 0.08, "mejora": 0.002},
    "estable":      {"base": 0.95, "sd": 0.08, "mejora": 0.001},
    "desarrollo":   {"base": 0.75, "sd": 0.10, "mejora": 0.005},
    "problematico": {"base": 0.62, "sd": 0.15, "mejora": 0.000},
}


def _generar_lista_meses():
    meses = []
    current = FECHA_INICIO.replace(day=1)
    fin = FECHA_FIN.replace(day=1)
    while current <= fin:
        meses.append(current)
        current = (current + relativedelta(months=1)).replace(day=1)
    return meses


def _dias_en_mes(año: int, mes: int) -> list:
    """Lista de fechas del mes dado."""
    inicio = date(año, mes, 1)
    if mes == 12:
        fin = date(año + 1, 1, 1) - timedelta(days=1)
    else:
        fin = date(año, mes + 1, 1) - timedelta(days=1)
    # Excluir domingos para más realismo
    dias = [inicio + timedelta(days=i) for i in range((fin - inicio).days + 1)]
    dias = [d for d in dias if d.weekday() != 6]  # sin domingos
    return dias


def _factor_crecimiento(mes: date) -> float:
    """Factor de crecimiento acumulado: 8% anual ≈ 0.64% mensual."""
    meses_transcurridos = (mes.year - FECHA_INICIO.year) * 12 + (mes.month - FECHA_INICIO.month)
    return (1.0064) ** meses_transcurridos


def _factor_vendedor(vendedor_id: str, perfil: str, mes: date, idx: int) -> float:
    """Performance mensual del vendedor."""
    cfg = PERFILES_FACTOR[perfil]
    meses_transcurridos = (mes.year - FECHA_INICIO.year) * 12 + (mes.month - FECHA_INICIO.month)
    base = min(cfg["base"] + cfg["mejora"] * meses_transcurridos, 1.30)
    noise = np.random.normal(0, cfg["sd"])
    return max(0.30, base + noise)


def _seleccionar_producto(canal: str, productos_por_cat: dict) -> str:
    """Selecciona un producto según mezcla de canal."""
    mezcla = MEZCLA_PRODUCTOS[canal]
    categoria = random.choices(list(mezcla.keys()), weights=list(mezcla.values()))[0]
    return random.choice(productos_por_cat[categoria])


def generar_transacciones(
    df_vendedores: pd.DataFrame,
    df_clientes: pd.DataFrame,
    df_productos: pd.DataFrame,
    df_objetivos: pd.DataFrame,
) -> pd.DataFrame:
    """Genera el dataset de transacciones de venta."""

    # Índice de productos por categoría
    productos_por_cat = df_productos.groupby("categoria")["id_producto"].apply(list).to_dict()
    prod_map = df_productos.set_index("id_producto")
    vend_map = df_vendedores.set_index("id_vendedor")

    meses = _generar_lista_meses()
    transacciones = []
    id_venta = 1

    # Mes 18 = fecha de baja de V012 (junio 2024)
    fecha_baja_v012 = date(2024, 7, 1)  # A partir de julio 2024, V012 inactivo

    for mes_idx, mes in enumerate(meses):
        season = ESTACIONALIDAD[mes.month]
        growth = _factor_crecimiento(mes)
        dias_mes = _dias_en_mes(mes.year, mes.month)

        if not dias_mes:
            continue

        # Clientes activos en este mes
        clientes_activos = df_clientes[
            (df_clientes["activo"] == True) |
            (df_clientes["fecha_alta"] <= mes + relativedelta(months=1))
        ].copy()

        # Excluir clientes inactivos que se dieron de baja antes de este mes
        # (simplificación: los inactivos dejan de comprar en el último mes disponible)

        for _, cliente in clientes_activos.iterrows():
            canal        = cliente["canal"]
            vendedor_id  = cliente["id_vendedor_asignado"]
            cli_id       = cliente["id_cliente"]

            # V012 inactivo a partir de julio 2024
            if vendedor_id == "V012" and mes >= fecha_baja_v012.replace(day=1):
                # Reasignar a otro vendedor de la misma zona ocasionalmente
                if random.random() < 0.8:
                    continue  # cliente sin actividad en ese mes

            if vendedor_id not in vend_map.index:
                continue

            perfil = vend_map.loc[vendedor_id, "perfil"]
            vend_factor = _factor_vendedor(vendedor_id, perfil, mes, mes_idx)

            # Frecuencia de compra del canal
            freq_min, freq_max = FRECUENCIA_CANAL[canal]
            n_compras = random.randint(freq_min, freq_max)

            # Clientes inactivos no compran en los últimos N meses
            if not cliente["activo"]:
                # Inactivos: última compra entre 3 y 18 meses antes de FECHA_FIN
                meses_sin_compra = random.randint(3, 18)
                ultimo_mes_activo = FECHA_FIN - relativedelta(months=meses_sin_compra)
                if mes >= ultimo_mes_activo.replace(day=1):
                    continue

            for _ in range(n_compras):
                fecha = random.choice(dias_mes)

                # 3% de excepción: compra con otro vendedor
                vendedor_transaccion = vendedor_id
                if random.random() < 0.03:
                    otros = df_vendedores[df_vendedores["activo"] &
                                         (df_vendedores["id_vendedor"] != vendedor_id)
                                         ]["id_vendedor"].tolist()
                    if otros:
                        vendedor_transaccion = random.choice(otros)

                # Cantidad de productos en esta transacción
                n_productos = random.randint(1, 4)

                for _ in range(n_productos):
                    prd_id   = _seleccionar_producto(canal, productos_por_cat)

                    # Baja rotación → probabilidad extra de no aparecer
                    if prod_map.loc[prd_id, "baja_rotacion"] and random.random() < 0.80:
                        continue

                    precio_base  = prod_map.loc[prd_id, "precio_unitario"]
                    # Variación de precio ±5% por negociación
                    precio_real  = round(precio_base * random.uniform(0.95, 1.05))

                    # Cantidad según canal
                    if canal == "Mayorista":
                        cantidad = random.randint(6, 48)
                    elif canal == "Supermercadismo":
                        cantidad = random.randint(4, 24)
                    else:
                        cantidad = random.randint(1, 12)

                    # Descuento
                    dsc_min, dsc_max = DESCUENTO_CANAL[canal]
                    descuento = round(random.uniform(dsc_min, dsc_max), 3)

                    importe_bruto = round(precio_real * cantidad)
                    importe_neto  = round(importe_bruto * (1 - descuento))

                    # Aplicar factor de vendedor y estacionalidad al importe
                    # (simulamos que el vendedor impacta en el volumen total, no en precio)
                    factor_total = vend_factor * season * growth
                    importe_neto  = round(importe_neto  * factor_total)
                    importe_bruto = round(importe_bruto * factor_total)
                    cantidad_adj  = max(1, round(cantidad * factor_total))

                    if importe_neto <= 0:
                        continue

                    transacciones.append({
                        "id_venta":        f"VTA{id_venta:06d}",
                        "fecha":           fecha,
                        "id_vendedor":     vendedor_transaccion,
                        "id_cliente":      cli_id,
                        "id_producto":     prd_id,
                        "cantidad":        cantidad_adj,
                        "precio_unitario": precio_real,
                        "descuento_pct":   descuento,
                        "importe_bruto":   importe_bruto,
                        "importe_neto":    importe_neto,
                    })
                    id_venta += 1

        # ── Outliers: 2-3 pedidos especiales por mes ──────────
        n_outliers = random.randint(2, 3)
        for _ in range(n_outliers):
            cli = df_clientes[df_clientes["activo"]].sample(1).iloc[0]
            prd = df_productos[~df_productos["baja_rotacion"]].sample(1).iloc[0]
            fecha = random.choice(dias_mes)
            cantidad = random.randint(50, 200)
            precio = prd["precio_unitario"]
            importe_neto = round(precio * cantidad * 0.92)  # 8% descuento especial
            transacciones.append({
                "id_venta":        f"VTA{id_venta:06d}",
                "fecha":           fecha,
                "id_vendedor":     cli["id_vendedor_asignado"],
                "id_cliente":      cli["id_cliente"],
                "id_producto":     prd["id_producto"],
                "cantidad":        cantidad,
                "precio_unitario": precio,
                "descuento_pct":   0.08,
                "importe_bruto":   round(precio * cantidad),
                "importe_neto":    importe_neto,
            })
            id_venta += 1

    df = pd.DataFrame(transacciones)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df


# ═══════════════════════════════════════════════════════════════
# 6. VALIDACIÓN Y EXPORTACIÓN
# ═══════════════════════════════════════════════════════════════

def validar_y_resumir(df_ventas, df_vendedores, df_clientes, df_productos):
    print("\n" + "="*55)
    print("  RESUMEN DE VALIDACIÓN — Visor KPI Mock Data")
    print("="*55)

    # Vendedores
    n_v = len(df_vendedores)
    print(f"{'✅' if n_v == 12 else '❌'} Vendedores generados: {n_v}")

    # Clientes
    n_c    = len(df_clientes)
    n_act  = df_clientes["activo"].sum()
    n_inact= n_c - n_act
    print(f"{'✅' if n_c == 180 else '❌'} Clientes generados: {n_c} ({n_act} activos, {n_inact} inactivos)")

    # Productos
    n_p = len(df_productos)
    print(f"{'✅' if n_p == 60 else '❌'} Productos generados: {n_p}")

    # Transacciones
    n_t = len(df_ventas)
    ok_t = 8_000 <= n_t <= 15_000
    print(f"{'✅' if ok_t else '⚠️'} Transacciones generadas: {n_t:,}")

    # Período
    f_min = df_ventas["fecha"].min().date()
    f_max = df_ventas["fecha"].max().date()
    print(f"✅ Período cubierto: {f_min.strftime('%b-%Y')} a {f_max.strftime('%b-%Y')}")

    # Importe total
    total = df_ventas["importe_neto"].sum()
    print(f"✅ Importe total: ${total:,.0f}".replace(",", "."))

    # Coherencia vendedor-cliente
    cli_vend = df_clientes.set_index("id_cliente")["id_vendedor_asignado"].to_dict()
    df_ventas["vendedor_asignado"] = df_ventas["id_cliente"].map(cli_vend)
    n_coherente = (df_ventas["id_vendedor"] == df_ventas["vendedor_asignado"]).sum()
    pct_coh = n_coherente / len(df_ventas) * 100
    print(f"{'✅' if pct_coh >= 96 else '⚠️'} Coherencia vendedor-cliente: {pct_coh:.1f}% (esperado >96%)")

    # Estacionalidad
    df_ventas["mes_num"] = df_ventas["fecha"].dt.month
    df_ventas["año"]     = df_ventas["fecha"].dt.year
    mensual = df_ventas.groupby(df_ventas["fecha"].dt.to_period("M"))["importe_neto"].sum()
    promedio_general = mensual.mean()
    meses_dic_ene = df_ventas[df_ventas["mes_num"].isin([12, 1])].groupby(
        df_ventas[df_ventas["mes_num"].isin([12, 1])]["fecha"].dt.to_period("M")
    )["importe_neto"].sum()
    factor_estac = meses_dic_ene.mean() / promedio_general - 1 if promedio_general > 0 else 0
    print(f"{'✅' if factor_estac >= 0.15 else '⚠️'} Estacionalidad dic/ene: +{factor_estac*100:.1f}% (esperado ~25%)")

    # Clientes sin compras últimos 90 días
    ultima_compra = df_ventas.groupby("id_cliente")["fecha"].max()
    corte = pd.Timestamp(FECHA_FIN) - pd.Timedelta(days=90)
    sin_compras = (ultima_compra < corte).sum()
    print(f"✅ Clientes sin compras últimos 90 días: {sin_compras}")

    # Productos baja rotación
    por_prod = df_ventas.groupby("id_producto")["importe_neto"].sum()
    total_importe = por_prod.sum()
    pct_prod = (por_prod / total_importe * 100).sort_values()
    n_baja = (pct_prod.cumsum() < 5).sum()
    print(f"{'✅' if n_baja >= 10 else '⚠️'} Productos bajo rotación (<5% acumulado): {n_baja} (esperado ~12)")

    # Nulls críticos
    criticos = ["id_venta", "fecha", "id_vendedor", "id_cliente", "id_producto", "importe_neto"]
    n_nulls = df_ventas[criticos].isnull().sum().sum()
    print(f"{'✅' if n_nulls == 0 else '❌'} Nulls en campos críticos: {n_nulls}")

    print("="*55 + "\n")


def exportar_excel(df_ventas, df_vendedores, df_clientes, df_productos, df_objetivos):
    """Exporta todo a un Excel multi-hoja."""
    # Limpiar columna temporal
    if "vendedor_asignado" in df_ventas.columns:
        df_ventas = df_ventas.drop(columns=["vendedor_asignado"])
    if "mes_num" in df_ventas.columns:
        df_ventas = df_ventas.drop(columns=["mes_num"])
    if "año" in df_ventas.columns:
        df_ventas = df_ventas.drop(columns=["año"])

    with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
        df_ventas.to_excel(   writer, sheet_name="Ventas",    index=False)
        df_vendedores.to_excel(writer, sheet_name="Vendedores", index=False)
        df_clientes.to_excel(  writer, sheet_name="Clientes",   index=False)
        df_productos.to_excel( writer, sheet_name="Productos",  index=False)
        df_objetivos.to_excel( writer, sheet_name="Objetivos",  index=False)

    print(f"📁 Excel guardado en: {OUTPUT_FILE}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("Generando datos mock...")

    print("  • Vendedores...")
    df_vendedores = generar_vendedores()

    print("  • Clientes...")
    df_clientes = generar_clientes(df_vendedores)

    print("  • Productos...")
    df_productos = generar_productos()

    print("  • Objetivos...")
    df_objetivos = generar_objetivos(df_vendedores)

    print("  • Transacciones (puede demorar ~30s)...")
    df_ventas = generar_transacciones(df_vendedores, df_clientes, df_productos, df_objetivos)

    validar_y_resumir(df_ventas, df_vendedores, df_clientes, df_productos)
    exportar_excel(df_ventas, df_vendedores, df_clientes, df_productos, df_objetivos)

    print("✅ Generación completada.")


if __name__ == "__main__":
    main()

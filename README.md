# 📊 Visor KPI Comercial — Dashboard con Streamlit

Demo de carta de presentación de nivel producción.  
Análisis completo de KPIs para una distribuidora de consumo masivo.

---

## 🚀 Quick Start

```bash
# 1. Clonar el repositorio
git clone https://github.com/ricardobing/excel-to-kpi-dashboard.git
cd excel-to-kpi-dashboard

# 2. Crear entorno virtual (Python 3.10–3.12 recomendado)
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# 3. Instalar dependencias
pip install -r visor_kpi/requirements.txt

# 4. Generar datos mock (primera vez)
cd visor_kpi
python data/mock/generate_mock_data.py

# 5. Lanzar la app
streamlit run app.py
```

---

## 🗂️ Estructura del Proyecto

```
visor_kpi/
├── app.py                     # Resumen Ejecutivo (página principal)
├── config.py                  # Colores, umbrales, formatos
├── requirements.txt
│
├── pages/
│   ├── 1_gerencia.py          # Vista consolidada gerencial
│   ├── 2_vendedores.py        # Vista individual por vendedor
│   ├── 3_clientes.py          # Análisis de cartera de clientes
│   ├── 4_productos.py         # Ranking y análisis de productos
│   └── 5_alertas.py           # Centro de alertas y oportunidades
│
├── src/
│   ├── data_loader.py         # Lectura y filtrado del Excel
│   ├── kpi_engine.py          # Cálculo de todos los KPIs
│   ├── pareto.py              # Análisis 80/20
│   ├── alerts_engine.py       # Motor de alertas (ALT001–ALT007)
│   └── reports.py             # Generación de reportes exportables
│
├── components/
│   ├── kpi_card.py            # Tarjetas de KPI con semáforo
│   ├── charts.py              # Todos los gráficos Plotly
│   ├── filters.py             # Filtros laterales con session_state
│   └── rankings.py            # Tablas de ranking con HTML estilizado
│
├── assets/
│   └── style.css              # Estilos dark-theme global
│
├── data/
│   ├── mock/
│   │   └── generate_mock_data.py   # Generador de datos de demostración
│   └── raw/
│       └── mock_data.xlsx          # ← generado localmente
│
└── tests/
    ├── test_mock_data.py       # Validación del dataset
    ├── test_kpis.py            # Tests del motor de KPIs
    └── test_alerts.py          # Tests del motor de alertas
```

---

## 📐 Stack Técnico

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.10+ | Runtime |
| Streamlit | 1.32 | UI / Multi-page app |
| Plotly | 5.19 | Visualizaciones interactivas |
| Pandas | 2.2 | Análisis de datos |
| NumPy | 1.26 | Cálculos numéricos |
| Faker | 23.2 | Generación de datos mock (es_AR) |
| openpyxl | ≥3.1.5 | Lectura/escritura Excel |
| pytest | 8.0 | Tests automatizados |

---

## 📊 Páginas del Dashboard

### 🏠 Resumen Ejecutivo (`app.py`)
- 4 KPI cards con semáforo (ventas, margen, cobertura, cumplimiento)
- Gauge de cumplimiento + evolución mensual
- Rankings top-5: vendedores, clientes y productos
- Alertas activas + distribución de cartera

### 📋 Vista Gerencial (`1_gerencia.py`)
- KPI consolidado del equipo completo
- Gráficos de evolución + barras por vendedor
- Heatmap de ventas por mes/zona
- Ranking completo con delta vs mes anterior

### 👤 Vista por Vendedor (`2_vendedores.py`)
- Selector de vendedor individual
- Gauge personal + comparativa vs equipo
- Posición de ranking con flecha de movimiento
- Cartera de clientes y productos top

### 🧑‍🤝‍🧑 Clientes (`3_clientes.py`)
- Análisis Pareto A/B/C con chart y scatter
- Concentración de cartera e índice Gini
- Clientes en riesgo y oportunidades de crecimiento
- Detalle expandible por cliente

### 📦 Productos (`4_productos.py`)
- Treemap por categoría y ventas
- Pareto de productos con baja rotación
- Filtros por categoría y análisis de crecimiento

### 🚨 Centro de Alertas (`5_alertas.py`)
- 7 reglas de alerta (ALT001–ALT007)
- Filtro por severidad y tipo
- Marcar alertas como revisadas (session_state)
- Historial de revisadas

---

## 🧪 Tests

```bash
cd visor_kpi
pytest tests/ -v
# → 51 tests passed
```

Tests cubren:
- Validación del dataset mock (coherencia, volumen, nulls, fechas)
- Motor de KPIs (estructura, valores, deltaS)
- Análisis Pareto (escala, categorías, monotonicidad)
- Motor de alertas (cada regla ALT001–ALT004, ALT006)

---

## 🎨 Sistema de Diseño

- **Paleta dark**: `bg_dark=#0F1923`, `bg_card=#1A2535`
- **Semáforo**: `success=#00C49F` | `warning=#FFB347` | `danger=#E84855`
- **Tipografía**: Inter (Google Fonts)
- **Responsive**: breakpoint en 768px

---

## 📈 Datos de Demostración

El generador crea datos realistas para **Distribuidora Del Sur S.A.**:

- **Período**: Enero 2023 – Marzo 2026 (27 meses)
- **12 vendedores** con perfiles de performance (estrella/estable/desarrollo/problemático)
- **180 clientes** en 4 canales (Tradicional, Supermercadismo, Mayorista, HoReCa)
- **60 productos** en 5 categorías
- **~30.000 transacciones** con estacionalidad, tendencia de crecimiento y coherencia de datos

---

## 📄 Licencia

MIT License — libre para uso en demos y portfolios.

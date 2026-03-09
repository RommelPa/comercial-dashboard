# 📊 Visor KPI Comercial — Sales Intelligence Dashboard

> **Transforming raw Excel sales data into automated commercial intelligence, real-time KPI monitoring and actionable business alerts for FMCG distribution teams.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red?logo=streamlit)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.19-3F4F75?logo=plotly)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?logo=pandas)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 ¿Qué problema resuelve?

Los equipos comerciales en distribuidoras de consumo masivo pierden **horas semanales** consolidando archivos Excel manualmente, sin visibilidad en tiempo real del rendimiento de vendedores, clientes y productos.

**Visor KPI Comercial** automatiza ese proceso de punta a punta:

- **Elimina el análisis manual** → convierte archivos Excel de ventas en KPIs procesados automáticamente
- **Centraliza la inteligencia comercial** → gerentes y vendedores acceden a sus métricas desde un único dashboard
- **Anticipa problemas** → un motor de alertas detecta caídas de rendimiento, clientes en riesgo y oportunidades de crecimiento antes de que impacten en los resultados
- **Democratiza los datos** → cada vendedor accede a su propio reporte individual; la gerencia obtiene la vista consolidada

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

## 📈 Métricas Clave del Sistema

| Indicador | Valor |
|---|---|
| 📅 Cobertura histórica | 27 meses (Ene 2023 – Mar 2026) |
| 👤 Vendedores monitoreados | 12 (perfiles: estrella / estable / desarrollo / problemático) |
| 🏢 Clientes en cartera | 180 (4 canales comerciales) |
| 📦 SKUs analizados | 60 productos en 5 categorías |
| 🔁 Transacciones procesadas | ~30.000 registros |
| 🚨 Reglas de alerta activas | 7 (ALT001–ALT007) |
| ✅ Tests automatizados | 51 tests pasando |
| ⚡ Tiempo de carga del dashboard | < 3 segundos con dataset completo |

---

## 🧠 Capacidades de Business Intelligence

### ETL Automatizado
- **Ingesta de Excel** sin configuración manual: el sistema lee, valida y transforma el archivo de ventas en un pipeline reproducible con `pandas` + `openpyxl`
- Detección automática de nulos, fechas inconsistentes y valores atípicos
- Normalización de datos por canal, zona y período

### Motor de KPIs
Cálculo automatizado de los indicadores comerciales más críticos:

| KPI | Descripción |
|---|---|
| 💰 Ventas del período | Facturación total y por segmento |
| 📊 Margen bruto | Rentabilidad por vendedor, cliente y producto |
| 🎯 Cumplimiento de cuota | % de objetivo alcanzado vs meta mensual |
| 🌍 Cobertura de cartera | % de clientes activos sobre el total asignado |
| 📉 Variación vs período anterior | Delta absoluto y relativo MoM / YoY |
| 🔄 Frecuencia de compra | Recurrencia por cliente y canal |
| 📦 Rotación de productos | SKUs activos vs inactivos por período |

### Análisis Pareto 80/20
- Clasificación automática de clientes y productos en categorías **A / B / C**
- Cálculo del **índice de concentración Gini** de la cartera
- Identificación de los clientes que generan el 80% de la facturación
- Detección de SKUs de baja rotación con potencial de quiebre de stock

### Motor de Alertas Inteligentes
7 reglas de negocio preconfiguradas que disparan alertas en tiempo real:

| ID | Alerta | Severidad |
|---|---|---|
| ALT001 | Vendedor con cumplimiento < 70% | 🔴 Crítica |
| ALT002 | Cliente sin compra en los últimos 30 días | 🟠 Alta |
| ALT003 | Producto con caída de ventas > 30% MoM | 🟠 Alta |
| ALT004 | Cartera de clientes con concentración excesiva (Gini > 0.6) | 🟡 Media |
| ALT005 | Margen por debajo del umbral mínimo | 🔴 Crítica |
| ALT006 | Cobertura de cartera < 60% | 🟠 Alta |
| ALT007 | Oportunidad: cliente con alta frecuencia y ticket bajo | 🟢 Oportunidad |

---

## 📊 Páginas del Dashboard

### 🏠 Resumen Ejecutivo (`app.py`)
Vista de alto nivel para decisores. Incluye 4 KPI cards con semáforo de estado, gauge de cumplimiento, evolución mensual de ventas, rankings top-5 de vendedores / clientes / productos y panel de alertas activas.

### 📋 Vista Gerencial (`1_gerencia.py`)
Consolidado del equipo completo. Gráficos de evolución temporal, comparativa de rendimiento entre vendedores, heatmap de ventas por mes y zona, y ranking completo con delta vs mes anterior.

### 👤 Vista por Vendedor (`2_vendedores.py`)
Dashboard individual para cada comercial. Gauge de cumplimiento personal vs promedio del equipo, posición en el ranking con indicador de movimiento, detalle de cartera propia y productos top.

### 🧑‍🤝‍🧑 Análisis de Clientes (`3_clientes.py`)
Inteligencia de cartera completa. Segmentación Pareto A/B/C con gráfico acumulado y scatter, índice Gini, identificación de clientes en riesgo de churn y oportunidades de crecimiento con detalle expandible.

### 📦 Análisis de Productos (`4_productos.py`)
Visibilidad del portafolio. Treemap por categoría y volumen de ventas, Pareto de productos con baja rotación, filtros por categoría y análisis de tendencia de crecimiento por SKU.

### 🚨 Centro de Alertas (`5_alertas.py`)
Hub de acción comercial. Visualización de las 7 reglas ALT001–ALT007, filtrado por severidad y tipo, marcado de alertas como revisadas con persistencia en session state e historial de acciones.

---

## 🗂️ Arquitectura del Proyecto

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
├── src/                       # Core de la lógica de negocio
│   ├── data_loader.py         # ETL: lectura, validación y filtrado del Excel
│   ├── kpi_engine.py          # Motor de cálculo de todos los KPIs
│   ├── pareto.py              # Análisis 80/20 y clasificación A/B/C
│   ├── alerts_engine.py       # Motor de alertas (ALT001–ALT007)
│   └── reports.py             # Generación de reportes exportables
│
├── components/                # UI reusable
│   ├── kpi_card.py            # Tarjetas de KPI con semáforo
│   ├── charts.py              # Visualizaciones Plotly
│   ├── filters.py             # Filtros laterales con session_state
│   └── rankings.py            # Tablas de ranking con HTML estilizado
│
├── assets/
│   └── style.css              # Dark theme global
│
├── data/
│   ├── mock/
│   │   └── generate_mock_data.py   # Generador de datos demo (Faker es_AR)
│   └── raw/
│       └── mock_data.xlsx          # ← generado localmente
│
└── tests/
    ├── test_mock_data.py       # Validación del dataset
    ├── test_kpis.py            # Tests del motor de KPIs
    └── test_alerts.py          # Tests del motor de alertas
```

**Separación clara entre capas:**
- `src/` → lógica de negocio pura, 100% testeable e independiente de la UI
- `components/` → presentación reusable
- `pages/` → orquestación de vistas multi-página de Streamlit

---

## 🔧 Stack Tecnológico

| Tecnología | Versión | Rol en el sistema |
|---|---|---|
| **Python** | 3.10+ | Runtime principal |
| **Streamlit** | 1.32 | Framework de UI / Multi-page app |
| **Plotly** | 5.19 | Visualizaciones interactivas (charts, treemaps, gauges) |
| **Pandas** | 2.2 | Pipeline ETL y análisis de datos |
| **NumPy** | 1.26 | Cálculos numéricos y estadísticos |
| **openpyxl** | ≥3.1.5 | Lectura/escritura de archivos Excel |
| **Faker** | 23.2 | Generación de datos mock localizados (es_AR) |
| **pytest** | 8.0 | Suite de tests automatizados |

---

## 🧪 Testing

```bash
cd visor_kpi
pytest tests/ -v
# → 51 tests passed ✅
```

La suite cubre:
- **Dataset mock**: coherencia referencial, volumen de registros, integridad de nulos y rangos de fechas
- **Motor de KPIs**: estructura del output, valores calculados correctamente, deltas MoM/YoY
- **Análisis Pareto**: escala acumulada, asignación de categorías A/B/C, monotonicidad
- **Motor de alertas**: disparo correcto de cada regla ALT001–ALT004 y ALT006

---

## 🎨 Sistema de Diseño

- **Paleta dark**: `bg_dark=#0F1923` · `bg_card=#1A2535`
- **Semáforo de estado**: `success=#00C49F` · `warning=#FFB347` · `danger=#E84855`
- **Tipografía**: Inter via Google Fonts
- **Responsive**: breakpoint en 768px, optimizado para uso en tablet y mobile

---

## 📐 Contexto y Origen del Proyecto

**Visor KPI Comercial** nació de una necesidad real en distribuidoras de consumo masivo: los equipos de ventas dependían de análisis manuales en Excel que consumían tiempo, introducían errores y no escalaban.

El proyecto tomó como punto de partida un archivo Excel existente ("Clientes SF 2023") con la lógica comercial ya definida, y lo transformó en un sistema automatizado end-to-end que entrega:

- **A cada vendedor**: su reporte individual con su posición en el ranking, su cartera de clientes y sus productos top
- **A la gerencia**: una vista consolidada del equipo completo con alertas accionables y análisis de tendencias

El resultado es una plataforma de **Sales Intelligence** que reduce el tiempo de generación de reportes de horas a segundos, y convierte datos históricos de ventas en decisiones comerciales informadas.

---

## 🗺️ Roadmap

- [x] **Fase 1 – MVP**: ETL de Excel, motor de KPIs, rankings, dashboard multi-página, reportes exportables
- [x] **Fase 2**: Memoria histórica de datos, motor de alertas, análisis Pareto avanzado
- [ ] **Fase 3** *(planeado)*: Distribución automatizada de reportes vía WhatsApp / Telegram
- [ ] **Fase 4** *(planeado)*: Módulo de "Business Review" mensual con narrativa automatizada
- [ ] **Fase 5** *(planeado)*: Integración con fuentes de datos en tiempo real (ERP / CRM)

---

## 📄 Licencia

MIT License — libre para uso en demos, portfolios y adaptaciones comerciales.

---

<p align="center">
  Desarrollado con 🐍 Python · 📊 Streamlit · 📈 Plotly · 🐼 Pandas
</p>

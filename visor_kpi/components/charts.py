"""
components/charts.py
====================
Funciones de gráficos Plotly reutilizables.
Todas retornan go.Figure con el tema visual del dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from config import COLORS, PLOTLY_THEME, fmt_moneda


# ─── Aplicar tema global a una figura ─────────────────────────
def _apply_theme(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(
        paper_bgcolor = PLOTLY_THEME["paper_bgcolor"],
        plot_bgcolor  = PLOTLY_THEME["plot_bgcolor"],
        font          = PLOTLY_THEME["font"],
        margin        = PLOTLY_THEME["margin"],
        title         = dict(text=title, font=dict(size=15, color=COLORS["text_primary"])),
        legend        = dict(
            bgcolor    = COLORS["bg_card"],
            bordercolor= COLORS["border"],
            borderwidth= 1,
            font       = dict(color=COLORS["text_secondary"]),
        ),
    )
    fig.update_xaxes(
        gridcolor  = COLORS["border"],
        linecolor  = COLORS["border"],
        tickfont   = dict(color=COLORS["text_secondary"]),
        zerolinecolor = COLORS["border"],
    )
    fig.update_yaxes(
        gridcolor  = COLORS["border"],
        linecolor  = COLORS["border"],
        tickfont   = dict(color=COLORS["text_secondary"]),
        zerolinecolor = COLORS["border"],
    )
    return fig


# ═══════════════════════════════════════════════════════════════
# EVOLUCIÓN DE VENTAS
# ═══════════════════════════════════════════════════════════════

def chart_evolucion_ventas(
    df_mensual: pd.DataFrame,
    mostrar_objetivo: bool = True,
    title: str = "Evolución de Ventas vs Objetivo",
) -> go.Figure:
    """
    Línea de ventas mensuales + línea de objetivo.
    Área rellena bajo la curva de ventas.
    """
    fig = go.Figure()

    if df_mensual.empty:
        return _apply_theme(fig, title)

    periodos = df_mensual["periodo_str"].tolist() if "periodo_str" in df_mensual else \
               df_mensual["periodo"].astype(str).tolist()
    ventas   = df_mensual["importe"].tolist()

    # Área bajo la curva
    fig.add_trace(go.Scatter(
        x          = periodos,
        y          = ventas,
        fill       = "tozeroy",
        fillcolor  = "rgba(46,95,163,0.15)",
        line       = dict(color=COLORS["primary_light"], width=2.5),
        name       = "Ventas",
        mode       = "lines+markers",
        marker     = dict(size=6, color=COLORS["primary_light"]),
        hovertemplate = "<b>%{x}</b><br>Ventas: $%{y:,.0f}<extra></extra>",
    ))

    # Línea de objetivo
    if mostrar_objetivo and "objetivo" in df_mensual.columns:
        objetivos = df_mensual["objetivo"].tolist()
        fig.add_trace(go.Scatter(
            x          = periodos,
            y          = objetivos,
            line       = dict(color=COLORS["warning"], width=1.5, dash="dot"),
            name       = "Objetivo",
            mode       = "lines",
            hovertemplate = "<b>%{x}</b><br>Objetivo: $%{y:,.0f}<extra></extra>",
        ))

    # Anotación de máximo y mínimo
    if len(ventas) > 2:
        max_idx = int(np.argmax(ventas))
        min_idx = int(np.argmin(ventas))
        fig.add_annotation(
            x     = periodos[max_idx],
            y     = ventas[max_idx],
            text  = f"Máx: {fmt_moneda(ventas[max_idx])}",
            font  = dict(color=COLORS["success"], size=11),
            showarrow=True, arrowhead=2, arrowcolor=COLORS["success"],
            ay=-30,
        )

    fig = _apply_theme(fig, title)
    fig.update_layout(hovermode="x unified")
    return fig


# ═══════════════════════════════════════════════════════════════
# BARRAS HORIZONTALES VENDEDORES
# ═══════════════════════════════════════════════════════════════

def chart_barras_vendedores(
    df_vendedores: pd.DataFrame,
    title: str = "Cumplimiento por Vendedor",
) -> go.Figure:
    """
    Barras horizontales de cumplimiento.
    Color por semáforo. Línea vertical en 100%.
    """
    fig = go.Figure()

    if df_vendedores.empty or "cumplimiento_pct" not in df_vendedores.columns:
        return _apply_theme(fig, title)

    df = df_vendedores.sort_values("cumplimiento_pct", ascending=True).copy()
    nombres = df.get("nombre_vendedor", df["id_vendedor"]).tolist()
    cumpl   = (df["cumplimiento_pct"] * 100).tolist()
    colores = df["color_semaforo"].tolist() if "color_semaforo" in df.columns else \
              [COLORS["primary_light"]] * len(df)

    fig.add_trace(go.Bar(
        y             = nombres,
        x             = cumpl,
        orientation   = "h",
        marker_color  = colores,
        text          = [f"{c:.1f}%" for c in cumpl],
        textposition  = "outside",
        textfont      = dict(color=COLORS["text_primary"], size=11),
        hovertemplate = "<b>%{y}</b><br>Cumplimiento: %{x:.1f}%<extra></extra>",
    ))

    # Línea en 100%
    fig.add_vline(
        x          = 100,
        line_dash  = "dash",
        line_color = COLORS["success"],
        line_width = 1.5,
        annotation_text = "Objetivo",
        annotation_font_color = COLORS["success"],
    )

    # Línea en 80%
    fig.add_vline(
        x          = 80,
        line_dash  = "dot",
        line_color = COLORS["warning"],
        line_width = 1,
    )

    fig = _apply_theme(fig, title)
    fig.update_layout(
        xaxis_title = "Cumplimiento (%)",
        showlegend  = False,
        height      = max(300, len(nombres) * 45),
    )
    fig.update_xaxes(range=[0, max(130, max(cumpl) * 1.1)] if cumpl else [0, 130])
    return fig


# ═══════════════════════════════════════════════════════════════
# PARETO
# ═══════════════════════════════════════════════════════════════

def chart_pareto(
    df_pareto: pd.DataFrame,
    titulo: str = "Análisis Pareto",
    col_nombre: str = "razon_social",
    col_valor: str  = "importe_total",
    top_n: int      = 30,
) -> go.Figure:
    """
    Barras de participación + línea acumulada.
    Línea horizontal en 80%. Zona sombreada categoría A.
    """
    fig = go.Figure()

    if df_pareto.empty:
        return _apply_theme(fig, titulo)

    df = df_pareto.head(top_n).copy()
    nombres   = df[col_nombre].tolist() if col_nombre in df.columns else df.index.tolist()
    particip  = (df["participacion_pct"] * 100).tolist()
    acumulado = (df["acumulado_pct"] * 100).tolist()

    # Colores según categoría
    colores = []
    for cat in df.get("categoria_pareto", ["A"] * len(df)).tolist():
        if cat == "A":
            colores.append(COLORS["success"])
        elif cat == "B":
            colores.append(COLORS["warning"])
        else:
            colores.append(COLORS["text_secondary"])

    # Barras
    fig.add_trace(go.Bar(
        x             = nombres,
        y             = particip,
        marker_color  = colores,
        name          = "Participación %",
        yaxis         = "y",
        hovertemplate = "<b>%{x}</b><br>Part.: %{y:.2f}%<extra></extra>",
    ))

    # Línea acumulada
    fig.add_trace(go.Scatter(
        x          = nombres,
        y          = acumulado,
        mode       = "lines+markers",
        name       = "Acumulado %",
        line       = dict(color=COLORS["primary_light"], width=2),
        marker     = dict(size=4),
        yaxis      = "y2",
        hovertemplate = "Acum.: %{y:.1f}%<extra></extra>",
    ))

    # Línea 80%
    fig.add_hline(
        y             = 80,
        yref          = "y2",
        line_dash     = "dash",
        line_color    = COLORS["warning"],
        line_width    = 1.5,
        annotation_text = "80%",
        annotation_font_color = COLORS["warning"],
    )

    fig = _apply_theme(fig, titulo)
    fig.update_layout(
        yaxis  = dict(title="Participación %", ticksuffix="%"),
        yaxis2 = dict(
            title      = "Acumulado %",
            overlaying = "y",
            side       = "right",
            range      = [0, 105],
            ticksuffix = "%",
            gridcolor  = "transparent",
        ),
        barmode    = "group",
        hovermode  = "x unified",
    )
    return fig


# ═══════════════════════════════════════════════════════════════
# HEATMAP DE VENTAS
# ═══════════════════════════════════════════════════════════════

def chart_heatmap_ventas(
    df: pd.DataFrame,
    title: str = "Actividad comercial por día",
) -> go.Figure:
    """
    Heatmap: eje X = semana del mes, eje Y = día de la semana.
    """
    fig = go.Figure()
    if df.empty:
        return _apply_theme(fig, title)

    df = df.copy()
    df["dia_semana"] = df["fecha"].dt.dayofweek
    df["semana_mes"] = df["fecha"].apply(lambda d: (d.day - 1) // 7 + 1)
    df["dia_nombre"] = df["fecha"].dt.strftime("%a")

    pivot = df.groupby(["dia_semana", "semana_mes"])["importe_neto"].sum().reset_index()
    matriz = pivot.pivot(index="dia_semana", columns="semana_mes", values="importe_neto").fillna(0)

    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    y_labels = [dias[i] for i in matriz.index if i < len(dias)]

    fig.add_trace(go.Heatmap(
        z           = matriz.values.tolist(),
        x           = [f"Sem {w}" for w in matriz.columns],
        y           = y_labels,
        colorscale  = [[0, COLORS["bg_dark"]], [0.5, COLORS["primary_light"]], [1, COLORS["success"]]],
        showscale   = True,
        hovertemplate = "Semana %{x}<br>Día: %{y}<br>Ventas: $%{z:,.0f}<extra></extra>",
    ))

    return _apply_theme(fig, title)


# ═══════════════════════════════════════════════════════════════
# SCATTER CLIENTES
# ═══════════════════════════════════════════════════════════════

def chart_scatter_clientes(
    df_clientes: pd.DataFrame,
    title: str = "Clientes: Frecuencia vs Importe",
) -> go.Figure:
    """
    Scatter: eje X = frecuencia, eje Y = importe total.
    Tamaño = ticket promedio. Color = categoría Pareto.
    """
    fig = go.Figure()
    if df_clientes.empty:
        return _apply_theme(fig, title)

    colores_cat = {"A": COLORS["success"], "B": COLORS["warning"], "C": COLORS["text_secondary"]}

    for cat in ["A", "B", "C"]:
        sub = df_clientes[df_clientes["categoria_pareto"] == cat] if "categoria_pareto" in df_clientes.columns \
              else df_clientes
        if sub.empty:
            continue

        nombres = sub.get("razon_social", sub["id_cliente"]).tolist()
        x_vals  = sub["frecuencia_compra"].tolist()
        y_vals  = sub["importe_total"].tolist()
        sizes   = ((sub["ticket_promedio"] / sub["ticket_promedio"].max() * 20) + 5).clip(5, 30).tolist() \
                  if "ticket_promedio" in sub.columns else [10] * len(sub)

        fig.add_trace(go.Scatter(
            x          = x_vals,
            y          = y_vals,
            mode       = "markers",
            name       = f"Cat. {cat}",
            marker     = dict(
                color  = colores_cat.get(cat, COLORS["primary_light"]),
                size   = sizes,
                opacity= 0.8,
                line   = dict(width=1, color=COLORS["border"]),
            ),
            text       = nombres,
            hovertemplate = (
                "<b>%{text}</b><br>"
                "Frecuencia: %{x} compras<br>"
                "Importe: $%{y:,.0f}<extra></extra>"
            ),
        ))

    fig = _apply_theme(fig, title)
    fig.update_layout(
        xaxis_title = "Frecuencia de compra (transacciones)",
        yaxis_title = "Importe total ($)",
    )
    return fig


# ═══════════════════════════════════════════════════════════════
# TREEMAP PRODUCTOS
# ═══════════════════════════════════════════════════════════════

def chart_treemap_productos(
    df_productos: pd.DataFrame,
    title: str = "Productos por Categoría",
) -> go.Figure:
    """
    Treemap por categoría > producto.
    Tamaño = importe, color = variación vs anterior.
    """
    if df_productos.empty or "importe_total" not in df_productos.columns:
        fig = go.Figure()
        return _apply_theme(fig, title)

    df = df_productos.copy()
    df["variacion_pct"] = df.get("vs_periodo_anterior", pd.Series([0] * len(df))).fillna(0) * 100
    df["variacion_pct"] = df["variacion_pct"].clip(-50, 50)

    fig = px.treemap(
        df,
        path   = ["categoria", "descripcion"] if "categoria" in df.columns else ["descripcion"],
        values = "importe_total",
        color  = "variacion_pct",
        color_continuous_scale = [
            [0,   COLORS["danger"]],
            [0.5, COLORS["bg_card"]],
            [1,   COLORS["success"]],
        ],
        color_continuous_midpoint = 0,
        hover_data = {"importe_total": ":,.0f"},
        title  = title,
    )

    fig.update_traces(
        textfont  = dict(color=COLORS["text_primary"]),
        hovertemplate = "<b>%{label}</b><br>Ventas: $%{value:,.0f}<extra></extra>",
    )
    fig.update_layout(
        paper_bgcolor = PLOTLY_THEME["paper_bgcolor"],
        font          = PLOTLY_THEME["font"],
        margin        = PLOTLY_THEME["margin"],
    )
    return fig


# ═══════════════════════════════════════════════════════════════
# GAUGE DE CUMPLIMIENTO
# ═══════════════════════════════════════════════════════════════

def chart_gauge_cumplimiento(
    valor: float,
    label: str   = "Cumplimiento",
    max_val: float = 1.20,
) -> go.Figure:
    """
    Gauge semicircular de 0% a 120%.
    Zonas: rojo <80%, naranja 80-99%, verde 100%+.
    """
    valor_pct = (valor or 0) * 100
    max_pct   = max_val * 100

    fig = go.Figure(go.Indicator(
        mode   = "gauge+number+delta",
        value  = valor_pct,
        number = dict(suffix="%", font=dict(size=32, color=COLORS["text_primary"])),
        delta  = dict(
            reference  = 100,
            suffix     = "pp vs obj",
            font       = dict(size=14),
        ),
        gauge  = dict(
            axis  = dict(
                range     = [0, max_pct],
                ticksuffix= "%",
                tickcolor = COLORS["text_secondary"],
                tickfont  = dict(color=COLORS["text_secondary"]),
            ),
            bar   = dict(color=COLORS["primary_light"], thickness=0.25),
            bgcolor      = COLORS["bg_card"],
            borderwidth  = 0,
            steps = [
                dict(range=[0, 80],       color="rgba(232,72,85,0.25)"),
                dict(range=[80, 100],     color="rgba(255,179,71,0.25)"),
                dict(range=[100, max_pct],color="rgba(0,196,159,0.25)"),
            ],
            threshold = dict(
                line  = dict(color=COLORS["success"], width=3),
                value = 100,
            ),
        ),
        title  = dict(
            text = label,
            font = dict(size=14, color=COLORS["text_secondary"]),
        ),
    ))

    fig.update_layout(
        paper_bgcolor = PLOTLY_THEME["paper_bgcolor"],
        font          = dict(color=COLORS["text_primary"], family="Inter, sans-serif"),
        margin        = dict(l=20, r=20, t=60, b=20),
        height        = 280,
    )
    return fig


# ═══════════════════════════════════════════════════════════════
# PIE / DONUT
# ═══════════════════════════════════════════════════════════════

def chart_donut_canales(
    df: pd.DataFrame,
    title: str = "Distribución por Canal",
) -> go.Figure:
    """Donut de ventas por canal."""
    fig = go.Figure()
    if df.empty:
        return _apply_theme(fig, title)

    grp = df.groupby("canal")["importe_neto"].sum().reset_index()
    fig.add_trace(go.Pie(
        labels    = grp["canal"].tolist(),
        values    = grp["importe_neto"].tolist(),
        hole      = 0.55,
        marker    = dict(colors=COLORS["chart_seq"]),
        textfont  = dict(color=COLORS["text_primary"]),
        hovertemplate = "<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
    ))

    fig = _apply_theme(fig, title)
    fig.update_layout(showlegend=True, height=300)
    return fig

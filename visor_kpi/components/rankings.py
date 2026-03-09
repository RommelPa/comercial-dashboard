"""
components/rankings.py
======================
Tablas de ranking estilizadas con HTML/CSS.
"""

import streamlit as st
import pandas as pd
from config import COLORS, fmt_moneda, fmt_pct, fmt_numero, get_color_semaforo


def render_ranking_vendedores(
    df_vendedores: pd.DataFrame,
    max_rows: int = 12,
) -> None:
    """
    Tabla de ranking de vendedores con medallas, barra de progreso,
    delta de ranking y semáforo.
    """
    if df_vendedores.empty:
        st.info("Sin datos de vendedores para el período seleccionado.")
        return

    df = df_vendedores.head(max_rows).copy()

    filas_html = ""
    for _, row in df.iterrows():
        pos       = int(row.get("ranking_actual", 0))
        nombre    = row.get("nombre_vendedor", row.get("id_vendedor", "—"))
        zona      = row.get("zona_vendedor", "")
        importe   = fmt_moneda(row.get("importe_total", 0))
        cumpl     = row.get("cumplimiento_pct", 0) or 0
        cumpl_pct = fmt_pct(cumpl)
        delta_r   = int(row.get("delta_ranking", 0))
        color_sem = row.get("color_semaforo", COLORS["primary_light"])

        # Medalla top 3
        if pos == 1:
            pos_html = "🥇"
        elif pos == 2:
            pos_html = "🥈"
        elif pos == 3:
            pos_html = "🥉"
        else:
            pos_html = f"<span style='color:{COLORS['text_secondary']};font-weight:600'>#{pos}</span>"

        # Delta de ranking
        if delta_r > 0:
            delta_html = f"<span style='color:{COLORS['success']}'>↑{delta_r}</span>"
        elif delta_r < 0:
            delta_html = f"<span style='color:{COLORS['danger']}'>↓{abs(delta_r)}</span>"
        else:
            delta_html = f"<span style='color:{COLORS['text_secondary']}'>—</span>"

        # Barra de progreso inline
        bar_width = min(cumpl * 100, 100)
        bar_html  = (
            f"<div style='background:{COLORS['border']};border-radius:3px;height:5px;width:100%;margin-top:3px'>"
            f"<div style='width:{bar_width:.0f}%;background:{color_sem};height:5px;border-radius:3px'></div>"
            f"</div>"
        )

        filas_html += f"""
        <tr>
            <td style="text-align:center;width:50px">{pos_html}</td>
            <td>
                <div style="font-weight:600;color:{COLORS['text_primary']}">{nombre}</div>
                <div style="font-size:11px;color:{COLORS['text_secondary']}">{zona}</div>
            </td>
            <td style="text-align:right;font-variant-numeric:tabular-nums">
                <span style="color:{color_sem};font-weight:600">{cumpl_pct}</span>
                {bar_html}
            </td>
            <td style="text-align:right;font-variant-numeric:tabular-nums">{importe}</td>
            <td style="text-align:center">{delta_html}</td>
        </tr>
        """

    html = f"""
    <table class="ranking-table" style="width:100%;border-collapse:collapse">
        <thead>
            <tr>
                <th style="text-align:center">#</th>
                <th>Vendedor</th>
                <th style="text-align:right">Cumplimiento</th>
                <th style="text-align:right">Ventas</th>
                <th style="text-align:center">Ranking</th>
            </tr>
        </thead>
        <tbody>
            {filas_html}
        </tbody>
    </table>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_ranking_clientes(
    df_clientes: pd.DataFrame,
    top_n: int = 20,
) -> None:
    """
    Tabla de ranking de clientes con canal, días sin compra y categoría Pareto.
    """
    if df_clientes.empty:
        st.info("Sin datos de clientes para el período seleccionado.")
        return

    df = df_clientes.head(top_n).copy()

    # Colores de canal
    canal_colors = {
        "Canal Tradicional": COLORS["primary_light"],
        "Supermercadismo":   COLORS["success"],
        "Mayorista":         COLORS["warning"],
        "HoReCa":            "#9B59B6",
    }

    filas_html = ""
    for i, row in df.iterrows():
        nombre  = row.get("razon_social", row.get("id_cliente", "—"))
        canal   = row.get("canal", "—")
        importe = fmt_moneda(row.get("importe_total", 0))
        cat     = row.get("categoria_pareto", "C")
        dias    = row.get("dias_desde_ultima_compra", 0) or 0
        part    = fmt_pct(row.get("participacion_pct", 0))

        # Badge canal
        color_canal = canal_colors.get(canal, COLORS["text_secondary"])
        canal_badge = (
            f"<span style='background:rgba(46,95,163,0.15);color:{color_canal};"
            f"padding:2px 7px;border-radius:8px;font-size:10px;font-weight:600'>{canal}</span>"
        )

        # Badge Pareto
        cat_colors = {"A": COLORS["success"], "B": COLORS["warning"], "C": COLORS["text_secondary"]}
        cat_badge = (
            f"<span class='badge badge-{cat.lower()}'>{cat}</span>"
        )

        # Días sin compra
        dias_color = COLORS["danger"] if dias > 30 else COLORS["text_secondary"]
        dias_html  = f"<span style='color:{dias_color};font-weight:600'>{int(dias)}d</span>"

        filas_html += f"""
        <tr>
            <td>
                <div style="font-weight:600;color:{COLORS['text_primary']};font-size:13px">{nombre}</div>
                <div style="margin-top:3px">{canal_badge}</div>
            </td>
            <td style="text-align:center">{cat_badge}</td>
            <td style="text-align:right;font-variant-numeric:tabular-nums">{importe}</td>
            <td style="text-align:right;color:{COLORS['text_secondary']}">{part}</td>
            <td style="text-align:center">{dias_html}</td>
        </tr>
        """

    html = f"""
    <table class="ranking-table" style="width:100%;border-collapse:collapse">
        <thead>
            <tr>
                <th>Cliente</th>
                <th style="text-align:center">Cat.</th>
                <th style="text-align:right">Ventas</th>
                <th style="text-align:right">Part.%</th>
                <th style="text-align:center">Sin compra</th>
            </tr>
        </thead>
        <tbody>
            {filas_html}
        </tbody>
    </table>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_ranking_productos(
    df_productos: pd.DataFrame,
    top_n: int = 20,
) -> None:
    """
    Ranking de productos con categoría, participación y variación.
    """
    if df_productos.empty:
        st.info("Sin datos de productos para el período seleccionado.")
        return

    df = df_productos.head(top_n).copy()

    filas_html = ""
    for _, row in df.iterrows():
        desc    = row.get("descripcion", row.get("id_producto", "—"))
        cat     = row.get("categoria", "—")
        importe = fmt_moneda(row.get("importe_total", 0))
        part    = fmt_pct(row.get("participacion_pct", 0))
        acum    = fmt_pct(row.get("acumulado_pct", 0))
        pareto  = row.get("categoria_pareto", "C")
        var     = row.get("vs_periodo_anterior")

        # Variación
        if var is not None:
            vp = var * 100
            if vp > 0:
                var_html = f"<span style='color:{COLORS['success']}'>▲ +{vp:.1f}%</span>"
            else:
                var_html = f"<span style='color:{COLORS['danger']}'>▼ {vp:.1f}%</span>"
        else:
            var_html = "<span style='color:#8899AA'>—</span>"

        cat_badge = f"<span class='badge badge-{pareto.lower()}'>{pareto}</span>"

        filas_html += f"""
        <tr>
            <td>
                <div style="font-weight:600;color:{COLORS['text_primary']};font-size:13px">{desc}</div>
                <div style="font-size:11px;color:{COLORS['text_secondary']}">{cat}</div>
            </td>
            <td style="text-align:center">{cat_badge}</td>
            <td style="text-align:right;font-variant-numeric:tabular-nums">{importe}</td>
            <td style="text-align:right;color:{COLORS['text_secondary']}">{part}</td>
            <td style="text-align:right">{var_html}</td>
        </tr>
        """

    html = f"""
    <table class="ranking-table" style="width:100%;border-collapse:collapse">
        <thead>
            <tr>
                <th>Producto</th>
                <th style="text-align:center">Cat.</th>
                <th style="text-align:right">Ventas</th>
                <th style="text-align:right">Part.%</th>
                <th style="text-align:right">vs Anterior</th>
            </tr>
        </thead>
        <tbody>
            {filas_html}
        </tbody>
    </table>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_posicion_ranking(
    ranking_actual: int,
    ranking_anterior: int,
    total_vendedores: int,
) -> None:
    """
    Box visual de posición en el ranking del equipo.
    """
    delta   = ranking_anterior - ranking_actual
    pos_ant = ranking_anterior

    if delta > 0:
        delta_html = f"<span style='color:{COLORS['success']}'>↑ Subiste {delta} posición{'es' if delta > 1 else ''}</span>"
    elif delta < 0:
        delta_html = f"<span style='color:{COLORS['danger']}'>↓ Bajaste {abs(delta)} posición{'es' if abs(delta) > 1 else ''}</span>"
    else:
        delta_html = f"<span style='color:{COLORS['text_secondary']}'>— Sin cambios</span>"

    prev_pos = f"#{ranking_actual + 1}" if ranking_actual < total_vendedores else "—"
    next_pos = f"#{ranking_actual - 1}" if ranking_actual > 1 else "—"

    html = f"""
    <div class="ranking-position-box">
        <div style="font-size:11px;color:{COLORS['text_secondary']};text-transform:uppercase;
                    letter-spacing:1px;margin-bottom:8px">
            Tu posición este mes
        </div>
        <div style="display:flex;align-items:center;justify-content:center;gap:16px">
            <span style="color:{COLORS['text_secondary']};font-size:16px">{next_pos}</span>
            <div class="ranking-position-number">#{ranking_actual}</div>
            <span style="color:{COLORS['text_secondary']};font-size:16px">{prev_pos}</span>
        </div>
        <div class="ranking-position-label">
            de {total_vendedores} vendedores
        </div>
        <div style="margin-top:8px;font-size:13px;font-weight:500">
            {delta_html}
            <span style="color:{COLORS['text_secondary']};font-size:11px">vs mes anterior</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

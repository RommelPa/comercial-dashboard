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

        filas_html += (
            f"<tr style='border-bottom:1px solid {COLORS['border']}'>"
            f"<td style='text-align:center;width:50px;padding:8px 4px'>{pos_html}</td>"
            f"<td style='padding:8px 4px'>"
            f"<div style='font-weight:600;color:{COLORS['text_primary']}'>{nombre}</div>"
            f"<div style='font-size:11px;color:{COLORS['text_secondary']}'>{zona}</div></td>"
            f"<td style='text-align:right;padding:8px 4px'>"
            f"<span style='color:{color_sem};font-weight:600'>{cumpl_pct}</span>"
            f"{bar_html}</td>"
            f"<td style='text-align:right;padding:8px 4px;font-variant-numeric:tabular-nums'>{importe}</td>"
            f"<td style='text-align:center;padding:8px 4px'>{delta_html}</td>"
            f"</tr>"
        )

    ths = f"padding:6px 8px;color:{COLORS['text_secondary']};font-size:11px;font-weight:600;border-bottom:2px solid {COLORS['border']}"
    html = (
        f"<div style='overflow-x:auto'><table style='width:100%;border-collapse:collapse'>"
        f"<thead><tr>"
        f"<th style='text-align:center;{ths}'>#</th>"
        f"<th style='{ths}'>Vendedor</th>"
        f"<th style='text-align:right;{ths}'>Cumplimiento</th>"
        f"<th style='text-align:right;{ths}'>Ventas</th>"
        f"<th style='text-align:center;{ths}'>Ranking</th>"
        f"</tr></thead>"
        f"<tbody>{filas_html}</tbody>"
        f"</table></div>"
    )
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

        # Badge Pareto — inline styles (no CSS class dependency)
        cat_color = {"A": COLORS["success"], "B": COLORS["warning"], "C": COLORS["text_secondary"]}.get(cat, COLORS["text_secondary"])
        cat_badge = f"<span style='background:{cat_color};color:#fff;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600'>{cat}</span>"

        # Días sin compra
        dias_color = COLORS["danger"] if dias > 30 else COLORS["text_secondary"]
        dias_html  = f"<span style='color:{dias_color};font-weight:600'>{int(dias)}d</span>"

        filas_html += (
            f"<tr style='border-bottom:1px solid {COLORS['border']}'>"
            f"<td style='padding:8px 4px'>"
            f"<div style='font-weight:600;color:{COLORS['text_primary']};font-size:13px'>{nombre}</div>"
            f"<div style='margin-top:3px'>{canal_badge}</div></td>"
            f"<td style='text-align:center;padding:8px 4px'>{cat_badge}</td>"
            f"<td style='text-align:right;padding:8px 4px;font-variant-numeric:tabular-nums'>{importe}</td>"
            f"<td style='text-align:right;padding:8px 4px;color:{COLORS['text_secondary']}'>{part}</td>"
            f"<td style='text-align:center;padding:8px 4px'>{dias_html}</td>"
            f"</tr>"
        )

    ths = f"padding:6px 8px;color:{COLORS['text_secondary']};font-size:11px;font-weight:600;border-bottom:2px solid {COLORS['border']}"
    html = (
        f"<div style='overflow-x:auto'><table style='width:100%;border-collapse:collapse'>"
        f"<thead><tr>"
        f"<th style='{ths}'>Cliente</th>"
        f"<th style='text-align:center;{ths}'>Cat.</th>"
        f"<th style='text-align:right;{ths}'>Ventas</th>"
        f"<th style='text-align:right;{ths}'>Part.%</th>"
        f"<th style='text-align:center;{ths}'>Sin compra</th>"
        f"</tr></thead>"
        f"<tbody>{filas_html}</tbody>"
        f"</table></div>"
    )
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

        cat_color_p = {"A": COLORS["success"], "B": COLORS["warning"], "C": COLORS["text_secondary"]}.get(pareto, COLORS["text_secondary"])
        cat_badge = f"<span style='background:{cat_color_p};color:#fff;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600'>{pareto}</span>"

        filas_html += (
            f"<tr style='border-bottom:1px solid {COLORS['border']}'>"
            f"<td style='padding:8px 4px'>"
            f"<div style='font-weight:600;color:{COLORS['text_primary']};font-size:13px'>{desc}</div>"
            f"<div style='font-size:11px;color:{COLORS['text_secondary']}'>{cat}</div></td>"
            f"<td style='text-align:center;padding:8px 4px'>{cat_badge}</td>"
            f"<td style='text-align:right;padding:8px 4px;font-variant-numeric:tabular-nums'>{importe}</td>"
            f"<td style='text-align:right;padding:8px 4px;color:{COLORS['text_secondary']}'>{part}</td>"
            f"<td style='text-align:right;padding:8px 4px'>{var_html}</td>"
            f"</tr>"
        )

    ths = f"padding:6px 8px;color:{COLORS['text_secondary']};font-size:11px;font-weight:600;border-bottom:2px solid {COLORS['border']}"
    html = (
        f"<div style='overflow-x:auto'><table style='width:100%;border-collapse:collapse'>"
        f"<thead><tr>"
        f"<th style='{ths}'>Producto</th>"
        f"<th style='text-align:center;{ths}'>Cat.</th>"
        f"<th style='text-align:right;{ths}'>Ventas</th>"
        f"<th style='text-align:right;{ths}'>Part.%</th>"
        f"<th style='text-align:right;{ths}'>vs Anterior</th>"
        f"</tr></thead>"
        f"<tbody>{filas_html}</tbody>"
        f"</table></div>"
    )
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

    html = (
        f"<div style='background:{COLORS['bg_card']};border:1px solid {COLORS['border']};"
        f"border-radius:8px;padding:20px;text-align:center;margin-bottom:8px'>"
        f"<div style='font-size:11px;color:{COLORS['text_secondary']};text-transform:uppercase;"
        f"letter-spacing:1px;margin-bottom:8px'>Tu posición este mes</div>"
        f"<div style='display:flex;align-items:center;justify-content:center;gap:16px'>"
        f"<span style='color:{COLORS['text_secondary']};font-size:16px'>{next_pos}</span>"
        f"<div style='font-size:48px;font-weight:800;color:{COLORS['primary_light']}'>#{ranking_actual}</div>"
        f"<span style='color:{COLORS['text_secondary']};font-size:16px'>{prev_pos}</span>"
        f"</div>"
        f"<div style='color:{COLORS['text_secondary']};font-size:12px;margin-top:4px'>de {total_vendedores} vendedores</div>"
        f"<div style='margin-top:8px;font-size:13px;font-weight:500'>{delta_html}"
        f"<span style='color:{COLORS['text_secondary']};font-size:11px'> vs mes anterior</span></div>"
        f"</div>"
    )
    st.markdown(html, unsafe_allow_html=True)

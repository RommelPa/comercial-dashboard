"""
components/kpi_card.py
======================
Componente KPI Card reutilizable.
Usa st.markdown con HTML/CSS para control total del estilo.
"""

import streamlit as st
from config import get_color_semaforo, get_label_semaforo, fmt_pct, COLORS


def render_kpi_card(
    label: str,
    value: str,
    delta_pct: float | None   = None,
    objetivo: str | None      = None,
    cumplimiento: float | None = None,
    width: str                 = "100%",
    icon: str                  = "",
) -> None:
    """
    Renderiza una KPI card con:
    - Label en uppercase pequeño
    - Valor principal grande
    - Delta con flecha y color
    - Barra de progreso vs objetivo
    - Color de borde izquierdo según semáforo
    """
    sem_label = get_label_semaforo(cumplimiento) if cumplimiento is not None else "info"
    sem_color = get_color_semaforo(cumplimiento) if cumplimiento is not None else COLORS["primary_light"]

    # Delta HTML — single-line to avoid blank lines that terminate CommonMark HTML blocks
    delta_html = ""
    if delta_pct is not None:
        pct = delta_pct * 100
        if pct > 0.05:
            delta_html = f"<div style='font-size:12px;font-weight:600;color:{COLORS['success']};margin-top:4px'>▲ +{pct:.1f}%</div>"
        elif pct < -0.05:
            delta_html = f"<div style='font-size:12px;font-weight:600;color:{COLORS['danger']};margin-top:4px'>▼ {pct:.1f}%</div>"
        else:
            delta_html = f"<div style='font-size:12px;font-weight:600;color:{COLORS['text_secondary']};margin-top:4px'>— 0.0%</div>"

    # Progress bar — single-line concatenation (no embedded \n)
    progress_html = ""
    if cumplimiento is not None and objetivo is not None:
        pct_bar = min(cumplimiento * 100, 100)
        progress_html = (
            f"<div style='background:{COLORS['border']};border-radius:3px;height:5px;"
            f"width:100%;margin-top:8px'>"
            f"<div style='width:{pct_bar:.1f}%;background:{sem_color};"
            f"height:5px;border-radius:3px'></div></div>"
            f"<div style='font-size:11px;color:{COLORS['text_secondary']};margin-top:4px'>"
            f"{fmt_pct(cumplimiento)} del objetivo {objetivo}</div>"
        )

    icon_html = f"<span style='font-size:18px;margin-right:5px'>{icon}</span>" if icon else ""

    # Outer card — single-line concatenation (no embedded \n)
    html = (
        f"<div style='background:{COLORS['bg_card']};border-left:4px solid {sem_color};"
        f"border-radius:8px;padding:16px 18px;margin-bottom:4px;width:{width}'>"
        f"<div style='font-size:10px;font-weight:700;color:{COLORS['text_secondary']};"
        f"text-transform:uppercase;letter-spacing:1px;margin-bottom:6px'>{icon_html}{label}</div>"
        f"<div style='font-size:26px;font-weight:700;color:{COLORS['text_primary']};"
        f"line-height:1.1'>{value}</div>"
        f"{delta_html}{progress_html}"
        f"</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_kpi_card_simple(
    label: str,
    value: str,
    delta_pct: float | None = None,
    color: str | None = None,
) -> None:
    """Versión simplificada sin barra de progreso."""
    border_color = color or COLORS["primary_light"]

    delta_html = ""
    if delta_pct is not None:
        pct = delta_pct * 100
        if pct > 0.05:
            delta_html = f"<div style='font-size:12px;font-weight:600;color:{COLORS['success']};margin-top:4px'>▲ +{pct:.1f}%</div>"
        elif pct < -0.05:
            delta_html = f"<div style='font-size:12px;font-weight:600;color:{COLORS['danger']};margin-top:4px'>▼ {pct:.1f}%</div>"
        else:
            delta_html = f"<div style='font-size:12px;font-weight:600;color:{COLORS['text_secondary']};margin-top:4px'>— 0.0%</div>"

    html = (
        f"<div style='background:{COLORS['bg_card']};border-left:4px solid {border_color};"
        f"border-radius:8px;padding:16px 18px;margin-bottom:4px'>"
        f"<div style='font-size:10px;font-weight:700;color:{COLORS['text_secondary']};"
        f"text-transform:uppercase;letter-spacing:1px;margin-bottom:6px'>{label}</div>"
        f"<div style='font-size:26px;font-weight:700;color:{COLORS['text_primary']};"
        f"line-height:1.1'>{value}</div>"
        f"{delta_html}</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_kpi_row(cards: list[dict]) -> None:
    """
    Renderiza una fila de KPI cards.
    cards: lista de dicts con keys: label, value, delta_pct, objetivo, cumplimiento, icon
    """
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        with col:
            render_kpi_card(
                label        = card.get("label", ""),
                value        = card.get("value", "—"),
                delta_pct    = card.get("delta_pct"),
                objetivo     = card.get("objetivo"),
                cumplimiento = card.get("cumplimiento"),
                icon         = card.get("icon", ""),
            )

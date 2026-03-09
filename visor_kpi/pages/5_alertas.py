"""
pages/5_alertas.py — Centro de Alertas y Oportunidades
Lista de alertas activas con acciones y gestión de estado
"""

import os, sys
import streamlit as st
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

css_path = os.path.join(BASE_DIR, "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from components.filters  import render_sidebar_filters, init_session_state
from src.data_loader     import load_data, get_filtered_data, get_filtered_data_periodo_anterior, check_data_available
from src.alerts_engine   import get_alertas_activas
from config import COLORS

init_session_state()

if "alertas_revisadas" not in st.session_state:
    st.session_state["alertas_revisadas"] = set()

if not check_data_available():
    st.error("No se encontró el archivo de datos.")
    st.stop()

filtros = render_sidebar_filters()
fecha_desde    = filtros["fecha_desde"]
fecha_hasta    = filtros["fecha_hasta"]
vendedores_sel = filtros["vendedores_sel"] or None
zonas_sel      = filtros["zonas_sel"]      or None
canales_sel    = filtros["canales_sel"]    or None

with st.spinner("Evaluando alertas..."):
    data    = load_data()
    df      = get_filtered_data(fecha_desde, fecha_hasta, vendedores_sel, zonas_sel, canales_sel)
    df_ant  = get_filtered_data_periodo_anterior(fecha_desde, fecha_hasta, vendedores_sel, zonas_sel, canales_sel)
    cli_df  = data["clientes"]
    prod_df = data["productos"]
    obj_df  = data["objetivos"]
    alertas = get_alertas_activas(df, df_ant, cli_df, prod_df, obj_df, fecha_hasta)

st.markdown(
    f"""
    <h1 style="font-size:22px;font-weight:700;color:{COLORS['text_primary']};
               padding-bottom:12px;border-bottom:2px solid {COLORS['border']};margin-bottom:20px">
        🚨 Centro de Alertas y Oportunidades
    </h1>
    """,
    unsafe_allow_html=True,
)

# ── Resumen por severidad ─────────────────────────────────────
if alertas.empty:
    st.success("✅ No hay alertas activas para el período y filtros seleccionados.")
else:
    n_alta  = len(alertas[alertas["severidad"] == "alta"])
    n_media = len(alertas[alertas["severidad"] == "media"])
    n_baja  = len(alertas[alertas["severidad"] == "baja"])
    n_info  = len(alertas[alertas["severidad"] == "info"])

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(
        f"<div style='background:{COLORS['bg_card']};border-radius:10px;padding:14px;text-align:center;"
        f"border-left:4px solid {COLORS['danger']}'>"
        f"<div style='font-size:28px;font-weight:700;color:{COLORS['danger']}'>{n_alta}</div>"
        f"<div style='font-size:11px;color:{COLORS['text_secondary']};text-transform:uppercase'>Críticas 🔴</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    c2.markdown(
        f"<div style='background:{COLORS['bg_card']};border-radius:10px;padding:14px;text-align:center;"
        f"border-left:4px solid {COLORS['warning']}'>"
        f"<div style='font-size:28px;font-weight:700;color:{COLORS['warning']}'>{n_media}</div>"
        f"<div style='font-size:11px;color:{COLORS['text_secondary']};text-transform:uppercase'>Medias 🟡</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    c3.markdown(
        f"<div style='background:{COLORS['bg_card']};border-radius:10px;padding:14px;text-align:center;"
        f"border-left:4px solid {COLORS['primary_light']}'>"
        f"<div style='font-size:28px;font-weight:700;color:{COLORS['primary_light']}'>{n_baja}</div>"
        f"<div style='font-size:11px;color:{COLORS['text_secondary']};text-transform:uppercase'>Bajas 🔵</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    c4.markdown(
        f"<div style='background:{COLORS['bg_card']};border-radius:10px;padding:14px;text-align:center;"
        f"border-left:4px solid {COLORS['success']}'>"
        f"<div style='font-size:28px;font-weight:700;color:{COLORS['success']}'>{n_info}</div>"
        f"<div style='font-size:11px;color:{COLORS['text_secondary']};text-transform:uppercase'>Oportunidades 🟢</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    c5.markdown(
        f"<div style='background:{COLORS['bg_card']};border-radius:10px;padding:14px;text-align:center;"
        f"border-left:4px solid {COLORS['border']}'>"
        f"<div style='font-size:28px;font-weight:700;color:{COLORS['text_primary']}'>{len(alertas)}</div>"
        f"<div style='font-size:11px;color:{COLORS['text_secondary']};text-transform:uppercase'>Total alertas</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filtros de alertas ────────────────────────────────────
    with st.container():
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            sev_filter = st.multiselect(
                "Severidad",
                ["alta", "media", "baja", "info"],
                default=[],
                format_func=lambda x: {"alta": "🔴 Crítica", "media": "🟡 Media",
                                        "baja": "🔵 Baja", "info": "🟢 Oportunidad"}.get(x, x),
                key="_sev_filter",
            )
        with col_f2:
            tipo_filter = st.multiselect(
                "Tipo de entidad",
                alertas["entidad_tipo"].unique().tolist() if not alertas.empty else [],
                default=[],
                key="_tipo_filter",
            )
        with col_f3:
            mostrar_revisadas = st.checkbox("Ocultar revisadas", value=True, key="_hide_rev")

    # Aplicar filtros
    alertas_vis = alertas.copy()
    if sev_filter:
        alertas_vis = alertas_vis[alertas_vis["severidad"].isin(sev_filter)]
    if tipo_filter:
        alertas_vis = alertas_vis[alertas_vis["entidad_tipo"].isin(tipo_filter)]
    if mostrar_revisadas:
        alertas_vis = alertas_vis[
            ~alertas_vis.apply(lambda r: f"{r['id_alerta']}_{r['entidad_id']}", axis=1)
            .isin(st.session_state["alertas_revisadas"])
        ]

    st.markdown(
        f"<div style='font-size:12px;color:{COLORS['text_secondary']};margin-bottom:12px'>"
        f"Mostrando {len(alertas_vis)} de {len(alertas)} alertas</div>",
        unsafe_allow_html=True,
    )

    # ── Lista de alertas ──────────────────────────────────────
    sev_icons = {
        "alta":  ("🔴", COLORS["danger"]),
        "media": ("🟡", COLORS["warning"]),
        "baja":  ("🔵", COLORS["primary_light"]),
        "info":  ("🟢", COLORS["success"]),
    }

    for idx, alerta in alertas_vis.iterrows():
        alerta_key = f"{alerta['id_alerta']}_{alerta['entidad_id']}"
        ya_revisada = alerta_key in st.session_state["alertas_revisadas"]
        icon, color = sev_icons.get(alerta["severidad"], ("⚪", COLORS["border"]))

        st.markdown(
            f"""
            <div class="alert-card {alerta['severidad']}" 
                 style="opacity:{'0.4' if ya_revisada else '1'}">
                <div style="display:flex;justify-content:space-between;align-items:start">
                    <div>
                        <div class="alert-title">
                            {icon} [{alerta['id_alerta']}] · 
                            <span style="text-transform:uppercase;font-size:11px;
                                         background:rgba(255,255,255,0.1);padding:2px 8px;
                                         border-radius:10px;color:{color}">
                                {alerta['severidad']}
                            </span>
                        </div>
                        <div style="font-size:15px;font-weight:600;color:{COLORS['text_primary']};
                                    margin:4px 0">{alerta['nombre']}</div>
                        <div class="alert-detail">
                            <strong style="color:{COLORS['text_primary']}">{alerta['entidad_nombre']}</strong>
                            ({alerta['entidad_tipo']}) — {alerta['descripcion_detalle']}
                        </div>
                    </div>
                </div>
                <div style="margin-top:8px;padding-top:8px;border-top:1px solid {COLORS['border']}">
                    <span style="font-size:11px;color:{COLORS['text_secondary']}">💡 Acción sugerida: </span>
                    <span class="alert-action">{alerta['accion_sugerida']}</span>
                </div>
                {'<div style="margin-top:6px;font-size:11px;color:#00C49F">✅ Marcada como revisada</div>' if ya_revisada else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Botón de acción
        if not ya_revisada:
            col_btn1, col_btn2, _ = st.columns([1, 1, 4])
            with col_btn1:
                if st.button("✅ Marcar revisada", key=f"_rev_{alerta_key}", help="Marcar como revisada en esta sesión"):
                    st.session_state["alertas_revisadas"].add(alerta_key)
                    st.rerun()

    # ── Historial de revisadas ────────────────────────────────
    n_revisadas = len(st.session_state["alertas_revisadas"])
    if n_revisadas > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:13px;color:{COLORS['text_secondary']};border-top:1px solid {COLORS['border']};"
            f"padding-top:12px'>✅ {n_revisadas} alerta(s) marcadas como revisadas en esta sesión</div>",
            unsafe_allow_html=True,
        )
        if st.button("🔄 Limpiar historial de revisadas", key="_clear_rev"):
            st.session_state["alertas_revisadas"] = set()
            st.rerun()

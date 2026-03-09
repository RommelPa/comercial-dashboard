"""
src/alerts_engine.py
====================
Motor de alertas y oportunidades comerciales.
Evalúa 7 reglas y retorna DataFrame de alertas activas.
"""

import pandas as pd
import numpy as np
from datetime import date, timedelta


# ─── Definición de reglas ─────────────────────────────────────
ALERT_RULES = [
    {
        "id":              "ALT001",
        "nombre":          "Vendedor bajo rendimiento crítico",
        "condicion":       "cumplimiento_pct < 0.65 en los últimos 30 días",
        "severidad":       "alta",
        "entidad_tipo":    "vendedor",
        "accion_sugerida": "Revisar cartera y objetivos con supervisor",
    },
    {
        "id":              "ALT002",
        "nombre":          "Cliente sin compras (riesgo de pérdida)",
        "condicion":       "cliente activo sin compras en los últimos 45 días",
        "severidad":       "media",
        "entidad_tipo":    "cliente",
        "accion_sugerida": "Contacto de recuperación urgente",
    },
    {
        "id":              "ALT003",
        "nombre":          "Caída de venta en cliente relevante",
        "condicion":       "cliente categoría A con caída >25% vs mes anterior",
        "severidad":       "alta",
        "entidad_tipo":    "cliente",
        "accion_sugerida": "Visita de cuenta clave",
    },
    {
        "id":              "ALT004",
        "nombre":          "Producto sin movimiento",
        "condicion":       "producto activo sin ventas en 60 días",
        "severidad":       "baja",
        "entidad_tipo":    "producto",
        "accion_sugerida": "Revisar disponibilidad y push comercial",
    },
    {
        "id":              "ALT005",
        "nombre":          "Vendedor sin actividad reciente",
        "condicion":       "vendedor sin transacciones en los últimos 7 días hábiles",
        "severidad":       "media",
        "entidad_tipo":    "vendedor",
        "accion_sugerida": "Verificar actividad de campo",
    },
    {
        "id":              "ALT006",
        "nombre":          "Oportunidad: cliente B en crecimiento",
        "condicion":       "cliente categoría B con crecimiento >30% vs mes anterior",
        "severidad":       "info",
        "entidad_tipo":    "cliente",
        "accion_sugerida": "Potencial para upgrade a categoría A — aumentar frecuencia de visita",
    },
    {
        "id":              "ALT007",
        "nombre":          "Equipo cerca del objetivo mensual",
        "condicion":       "cumplimiento general >85% y quedan más de 5 días hábiles",
        "severidad":       "info",
        "entidad_tipo":    "equipo",
        "accion_sugerida": "Push final para cerrar mes en verde",
    },
]


def get_alertas_activas(
    df: pd.DataFrame,
    df_anterior: pd.DataFrame | None,
    clientes_df: pd.DataFrame,
    productos_df: pd.DataFrame,
    objetivos_df: pd.DataFrame | None = None,
    fecha_hasta: date | None = None,
) -> pd.DataFrame:
    """
    Evalúa todas las reglas y retorna DataFrame de alertas activas.

    Columns:
        id_alerta, nombre, severidad, entidad_tipo,
        entidad_id, entidad_nombre, valor_actual, valor_referencia,
        descripcion_detalle, fecha_deteccion, accion_sugerida
    """
    alertas = []
    hoy = fecha_hasta or date.today()
    ts_hoy = pd.Timestamp(hoy)

    if df.empty:
        return pd.DataFrame(columns=[
            "id_alerta", "nombre", "severidad", "entidad_tipo",
            "entidad_id", "entidad_nombre", "valor_actual",
            "valor_referencia", "descripcion_detalle",
            "fecha_deteccion", "accion_sugerida",
        ])

    # ── ALT001: Vendedor bajo rendimiento crítico ──────────────
    if objetivos_df is not None and not objetivos_df.empty:
        # Últimos 30 días
        desde_30 = ts_hoy - pd.Timedelta(days=30)
        df_30 = df[df["fecha"] >= desde_30]
        obj_mes = _get_objetivo_mes(objetivos_df, hoy)

        vend_ventas = df_30.groupby("id_vendedor")["importe_neto"].sum()
        for vend_id, importe in vend_ventas.items():
            obj = obj_mes.get(vend_id, 0)
            if obj > 0:
                cumpl = importe / obj
                if cumpl < 0.65:
                    nombre_v = _get_nombre_vendedor(df, vend_id)
                    alertas.append(_crear_alerta(
                        regla       = ALERT_RULES[0],
                        entidad_id  = vend_id,
                        entidad_nom = nombre_v,
                        val_actual  = cumpl,
                        val_ref     = 0.65,
                        detalle     = f"Cumplimiento: {cumpl*100:.1f}% (umbral: 65%)",
                        fecha       = hoy,
                    ))

    # ── ALT002: Cliente sin compras 45 días ────────────────────
    if not df.empty:
        ultima_compra = df.groupby("id_cliente")["fecha"].max()
        corte_45 = ts_hoy - pd.Timedelta(days=45)
        clientes_activos = set(clientes_df[clientes_df["activo"] == True]["id_cliente"].tolist())

        for cli_id in clientes_activos:
            uc = ultima_compra.get(cli_id)
            if uc is None or uc < corte_45:
                dias = (ts_hoy - uc).days if uc is not None else 999
                nombre_c = _get_nombre_cliente(clientes_df, cli_id)
                alertas.append(_crear_alerta(
                    regla       = ALERT_RULES[1],
                    entidad_id  = cli_id,
                    entidad_nom = nombre_c,
                    val_actual  = dias,
                    val_ref     = 45,
                    detalle     = f"Sin compras hace {dias} días",
                    fecha       = hoy,
                ))

    # ── ALT003: Caída cliente categoría A ──────────────────────
    if df_anterior is not None and not df_anterior.empty:
        from src.pareto import calcular_pareto
        grp_act = df.groupby("id_cliente")["importe_neto"].sum().reset_index()\
                    .rename(columns={"importe_neto": "importe_actual"})
        grp_act = calcular_pareto(grp_act, "importe_actual", "id_cliente")
        cat_A   = set(grp_act[grp_act["categoria_pareto"] == "A"]["id_cliente"].tolist())

        grp_ant = df_anterior.groupby("id_cliente")["importe_neto"].sum()\
                              .rename("importe_anterior")
        for cli_id in cat_A:
            imp_act = grp_act[grp_act["id_cliente"] == cli_id]["importe_actual"].values
            if len(imp_act) == 0:
                continue
            imp_act = imp_act[0]
            imp_ant = grp_ant.get(cli_id, 0)
            if imp_ant > 0:
                delta = (imp_act - imp_ant) / imp_ant
                if delta < -0.25:
                    nombre_c = _get_nombre_cliente(clientes_df, cli_id)
                    alertas.append(_crear_alerta(
                        regla       = ALERT_RULES[2],
                        entidad_id  = cli_id,
                        entidad_nom = nombre_c,
                        val_actual  = delta,
                        val_ref     = -0.25,
                        detalle     = f"Caída: {delta*100:.1f}% (${imp_ant:,.0f} → ${imp_act:,.0f})",
                        fecha       = hoy,
                    ))

    # ── ALT004: Producto sin movimiento 60 días ────────────────
    if not df.empty and not productos_df.empty:
        ultima_venta_prod = df.groupby("id_producto")["fecha"].max()
        corte_60 = ts_hoy - pd.Timedelta(days=60)
        productos_activos = productos_df[productos_df["activo"] == True]["id_producto"].tolist()

        for prd_id in productos_activos:
            uv = ultima_venta_prod.get(prd_id)
            if uv is None or uv < corte_60:
                dias = (ts_hoy - uv).days if uv is not None else 999
                desc = productos_df[productos_df["id_producto"] == prd_id]["descripcion"].values
                desc = desc[0] if len(desc) > 0 else prd_id
                alertas.append(_crear_alerta(
                    regla       = ALERT_RULES[3],
                    entidad_id  = prd_id,
                    entidad_nom = desc,
                    val_actual  = dias,
                    val_ref     = 60,
                    detalle     = f"Sin ventas hace {dias} días",
                    fecha       = hoy,
                ))

    # ── ALT005: Vendedor sin actividad 7 días hábiles ─────────
    if not df.empty:
        dias_habiles_7 = _retroceder_dias_habiles(hoy, 7)
        ultima_actividad = df.groupby("id_vendedor")["fecha"].max()
        vendedores_activos = df["id_vendedor"].unique()

        for vend_id in vendedores_activos:
            ua = ultima_actividad.get(vend_id)
            if ua is None or ua.date() < dias_habiles_7:
                nombre_v = _get_nombre_vendedor(df, vend_id)
                alertas.append(_crear_alerta(
                    regla       = ALERT_RULES[4],
                    entidad_id  = vend_id,
                    entidad_nom = nombre_v,
                    val_actual  = (ts_hoy - ua).days if ua else 999,
                    val_ref     = 7,
                    detalle     = f"Última venta: {ua.date() if ua else 'sin datos'}",
                    fecha       = hoy,
                ))

    # ── ALT006: Oportunidad cliente B crecimiento ──────────────
    if df_anterior is not None and not df_anterior.empty:
        from src.pareto import calcular_pareto
        grp_act = df.groupby("id_cliente")["importe_neto"].sum().reset_index()\
                    .rename(columns={"importe_neto": "importe_actual"})
        grp_act = calcular_pareto(grp_act, "importe_actual", "id_cliente")
        cat_B   = set(grp_act[grp_act["categoria_pareto"] == "B"]["id_cliente"].tolist())

        grp_ant = df_anterior.groupby("id_cliente")["importe_neto"].sum()\
                              .rename("importe_anterior")
        for cli_id in cat_B:
            imp_act = grp_act[grp_act["id_cliente"] == cli_id]["importe_actual"].values
            if len(imp_act) == 0:
                continue
            imp_act = imp_act[0]
            imp_ant = grp_ant.get(cli_id, 0)
            if imp_ant > 0:
                delta = (imp_act - imp_ant) / imp_ant
                if delta > 0.30:
                    nombre_c = _get_nombre_cliente(clientes_df, cli_id)
                    alertas.append(_crear_alerta(
                        regla       = ALERT_RULES[5],
                        entidad_id  = cli_id,
                        entidad_nom = nombre_c,
                        val_actual  = delta,
                        val_ref     = 0.30,
                        detalle     = f"Crecimiento: +{delta*100:.1f}%",
                        fecha       = hoy,
                    ))

    # ── ALT007: Equipo cerca del objetivo ─────────────────────
    if objetivos_df is not None and not objetivos_df.empty:
        obj_total = objetivos_df[
            objetivos_df["periodo"].dt.month == hoy.month
        ]["objetivo"].sum()
        ventas_mes = df[df["fecha"].dt.month == hoy.month]["importe_neto"].sum()
        cumpl_general = ventas_mes / obj_total if obj_total > 0 else 0

        dias_habiles_restantes = _dias_habiles_restantes_mes(hoy)
        if cumpl_general > 0.85 and dias_habiles_restantes > 5:
            alertas.append(_crear_alerta(
                regla       = ALERT_RULES[6],
                entidad_id  = "EQUIPO",
                entidad_nom = "Equipo Comercial",
                val_actual  = cumpl_general,
                val_ref     = 0.85,
                detalle     = (
                    f"Cumplimiento: {cumpl_general*100:.1f}% | "
                    f"Días hábiles restantes: {dias_habiles_restantes}"
                ),
                fecha       = hoy,
            ))

    df_alertas = pd.DataFrame(alertas)
    if df_alertas.empty:
        return pd.DataFrame(columns=[
            "id_alerta", "nombre", "severidad", "entidad_tipo",
            "entidad_id", "entidad_nombre", "valor_actual",
            "valor_referencia", "descripcion_detalle",
            "fecha_deteccion", "accion_sugerida",
        ])

    # Ordenar por severidad
    orden_sev = {"alta": 0, "media": 1, "baja": 2, "info": 3}
    df_alertas["_ord"] = df_alertas["severidad"].map(orden_sev).fillna(4)
    df_alertas = df_alertas.sort_values("_ord").drop(columns=["_ord"]).reset_index(drop=True)

    return df_alertas


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def _crear_alerta(
    regla: dict,
    entidad_id: str,
    entidad_nom: str,
    val_actual: float,
    val_ref: float,
    detalle: str,
    fecha: date,
) -> dict:
    return {
        "id_alerta":          regla["id"],
        "nombre":             regla["nombre"],
        "severidad":          regla["severidad"],
        "entidad_tipo":       regla["entidad_tipo"],
        "entidad_id":         entidad_id,
        "entidad_nombre":     entidad_nom,
        "valor_actual":       val_actual,
        "valor_referencia":   val_ref,
        "descripcion_detalle": detalle,
        "fecha_deteccion":    fecha,
        "accion_sugerida":    regla["accion_sugerida"],
    }


def _get_nombre_vendedor(df: pd.DataFrame, vend_id: str) -> str:
    if "nombre_vendedor" in df.columns:
        rows = df[df["id_vendedor"] == vend_id]["nombre_vendedor"]
        if not rows.empty:
            return rows.iloc[0]
    return vend_id


def _get_nombre_cliente(clientes_df: pd.DataFrame, cli_id: str) -> str:
    if "razon_social" in clientes_df.columns:
        rows = clientes_df[clientes_df["id_cliente"] == cli_id]["razon_social"]
        if not rows.empty:
            return rows.iloc[0]
    return cli_id


def _get_objetivo_mes(objetivos_df: pd.DataFrame, hoy: date) -> dict:
    """Retorna objetivo por vendedor para el mes actual."""
    mask = (
        (objetivos_df["periodo"].dt.year  == hoy.year) &
        (objetivos_df["periodo"].dt.month == hoy.month)
    )
    return objetivos_df[mask].groupby("id_vendedor")["objetivo"].sum().to_dict()


def _retroceder_dias_habiles(hoy: date, n: int) -> date:
    """Retrocede n días hábiles desde hoy."""
    d = hoy
    count = 0
    while count < n:
        d -= timedelta(days=1)
        if d.weekday() < 5:  # Lun-Vie
            count += 1
    return d


def _dias_habiles_restantes_mes(hoy: date) -> int:
    """Días hábiles que quedan en el mes actual."""
    from calendar import monthrange
    ultimo_dia = monthrange(hoy.year, hoy.month)[1]
    count = 0
    for d in range(hoy.day + 1, ultimo_dia + 1):
        if date(hoy.year, hoy.month, d).weekday() < 5:
            count += 1
    return count

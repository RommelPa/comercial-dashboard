"""
src/reports.py
==============
Generación de reportes en texto/Excel para exportación.
"""

import pandas as pd
import io
from datetime import date

from config import fmt_moneda, fmt_pct, fmt_numero


def generar_reporte_texto(
    kpi_ventas: dict,
    kpi_vend_df: pd.DataFrame,
    alertas_df: pd.DataFrame,
    fecha_desde: date,
    fecha_hasta: date,
) -> str:
    """Genera un resumen ejecutivo en texto plano."""
    lineas = [
        "=" * 60,
        "  REPORTE EJECUTIVO — VISOR KPI COMERCIAL",
        f"  Período: {fecha_desde.strftime('%d/%m/%Y')} al {fecha_hasta.strftime('%d/%m/%Y')}",
        "=" * 60,
        "",
        "VENTAS DEL PERÍODO",
        "-" * 40,
        f"  Importe total:    {fmt_moneda(kpi_ventas.get('importe_total', 0))}",
        f"  Objetivo:         {fmt_moneda(kpi_ventas.get('objetivo_total', 0))}",
        f"  Cumplimiento:     {fmt_pct(kpi_ventas.get('cumplimiento_pct', 0))}",
        f"  Transacciones:    {fmt_numero(kpi_ventas.get('transacciones_count', 0))}",
        f"  Ticket promedio:  {fmt_moneda(kpi_ventas.get('ticket_promedio', 0))}",
        "",
    ]

    if not kpi_vend_df.empty:
        lineas += [
            "RANKING VENDEDORES",
            "-" * 40,
        ]
        for _, row in kpi_vend_df.iterrows():
            cumpl = fmt_pct(row.get("cumplimiento_pct", 0))
            lineas.append(
                f"  #{int(row.get('ranking_actual', 0)):2d} {row.get('nombre_vendedor', row['id_vendedor']):<30s} "
                f"{cumpl:>8s}  {fmt_moneda(row.get('importe_total', 0))}"
            )
        lineas.append("")

    if alertas_df is not None and not alertas_df.empty:
        lineas += [
            f"ALERTAS ACTIVAS ({len(alertas_df)})",
            "-" * 40,
        ]
        for _, alerta in alertas_df.iterrows():
            ico = {"alta": "🔴", "media": "🟡", "baja": "🔵", "info": "🟢"}.get(alerta["severidad"], "⚪")
            lineas.append(
                f"  {ico} [{alerta['id_alerta']}] {alerta['nombre']}"
            )
            lineas.append(
                f"     → {alerta['entidad_nombre']}: {alerta['descripcion_detalle']}"
            )
        lineas.append("")

    lineas += [
        "=" * 60,
        f"  Generado: {date.today().strftime('%d/%m/%Y')}",
        "=" * 60,
    ]

    return "\n".join(lineas)


def generar_excel_reporte(
    kpi_vend_df: pd.DataFrame,
    kpi_clientes_df: pd.DataFrame,
    kpi_productos_df: pd.DataFrame,
    alertas_df: pd.DataFrame,
) -> bytes:
    """
    Genera un Excel con múltiples hojas para el reporte.
    Retorna bytes para descarga con st.download_button.
    """
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        if not kpi_vend_df.empty:
            kpi_vend_df.to_excel(writer, sheet_name="Vendedores", index=False)
        if not kpi_clientes_df.empty:
            kpi_clientes_df.to_excel(writer, sheet_name="Clientes", index=False)
        if not kpi_productos_df.empty:
            kpi_productos_df.to_excel(writer, sheet_name="Productos", index=False)
        if alertas_df is not None and not alertas_df.empty:
            alertas_df.to_excel(writer, sheet_name="Alertas", index=False)

    return output.getvalue()

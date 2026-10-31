"""
Análisis de Afluencia y Visualización Geoespacial del Metro de la CDMX (Q1 2026).

Este script realiza la limpieza de datos de afluencia, calcula métricas operativas
y genera mapas estáticos e interactivos mediante GeoPandas y Folium.
"""

from typing import Tuple
import folium
from folium.plugins import HeatMap
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# ==========================================
# CONSTANTES Y CONFIGURACIÓN
# ==========================================
CSV_PATH = "metroSimple.csv"
SHAPEFILE_PATH = "stcmetro_shp/STC_Metro_estaciones_utm14n.shp"
SHP_NAME_COL = "NOMBRE"
HTML_OUTPUT_PATH = "mapa_calor_metro_q1_2026.html"

# Servidor de mapas Esri World Street Map
ESRI_TILE_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
ESRI_ATTR = "Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012"


def cargar_y_limpiar_datos(filepath: str) -> pd.DataFrame:
    """Carga la base de datos de afluencia y aplica transformaciones y limpieza de texto.

    Args:
        filepath (str): Ruta al archivo CSV con los datos de afluencia.

    Returns:
        pd.DataFrame: DataFrame limpio y estandarizado.
    """
    df = pd.read_csv(filepath)

    # 1. Corrección de codificación de caracteres (Mojibake)
    for col in ["estacion", "linea"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.encode("latin-1", errors="ignore")
                .str.decode("utf-8", errors="ignore")
            )

    # 2. Conversión de tipos y manejo de nulos
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["afluencia"] = pd.to_numeric(df["afluencia"], errors="coerce").fillna(0)

    # 3. Normalización de cadenas de texto
    df["linea"] = df["linea"].str.strip().str.replace("Línea", "Linea")
    df["estacion"] = df["estacion"].str.strip()

    # 4. Extracción de variables temporales
    df["año"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["dia_semana"] = df["fecha"].dt.day_name()
    df["es_fin_de_semana"] = df["fecha"].dt.dayofweek >= 5

    return df


def filtrar_afluencia_q1_2026(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra el dataset para considerar únicamente días laborales del Q1 2026.

    Args:
        df (pd.DataFrame): DataFrame completo.

    Returns:
        pd.DataFrame: Promedio de afluencia diaria por estación en el periodo seleccionado.
    """
    cond_2026 = df["fecha"].dt.year == 2026
    cond_q1 = df["fecha"].dt.month <= 3
    cond_laboral = df["fecha"].dt.dayofweek < 5

    df_filtrado = df[cond_2026 & cond_q1 & cond_laboral]

    promedio_estacion = (
        df_filtrado.groupby("estacion")["afluencia"].mean().reset_index()
    )

    return promedio_estacion


def unificar_datos_geoespaciales(
    df_afluencia: pd.DataFrame, shp_path: str, col_nombre_shp: str
) -> gpd.GeoDataFrame:
    """Carga la capa geográfica SHP y realiza la unión con los datos de afluencia.

    Args:
        df_afluencia (pd.DataFrame): Promedio de afluencia por estación.
        shp_path (str): Ruta al archivo Shapefile.
        col_nombre_shp (str): Nombre de la columna de estación en el Shapefile.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame resultante de la unión.
    """
    geo_df = gpd.read_file(shp_path)

    # Estandarizar clave de cruce (mayúsculas y sin espacios)
    geo_df["estacion_clean"] = (
        geo_df[col_nombre_shp].astype(str).str.upper().str.strip()
    )
    df_afluencia["estacion_clean"] = (
        df_afluencia["estacion"].astype(str).str.upper().str.strip()
    )

    mapa_df = geo_df.merge(df_afluencia, on="estacion_clean", how="inner")

    return mapa_df


def generar_mapa_estatico(mapa_df: gpd.GeoDataFrame) -> None:
    """Genera y muestra el mapa de calor estático mediante Matplotlib."""
    fig, ax = plt.subplots(figsize=(12, 12))

    mapa_df.plot(
        column="afluencia",
        cmap="YlOrRd",
        markersize=mapa_df["afluencia"] / 400,
        legend=True,
        legend_kwds={"label": "Afluencia Promedio Diaria (Ene-Mar 2026)"},
        alpha=0.85,
        ax=ax,
    )

    ax.set_title(
        "Mapa de Calor: Afluencia Promedio Diaria en Días Laborales\n(Enero - Marzo 2026)",
        fontsize=14,
        fontweight="bold",
    )
    ax.axis("off")
    plt.tight_layout()
    plt.show()


def generar_mapa_interactivo(
    mapa_df: gpd.GeoDataFrame, output_html: str
) -> None:
    """Crea y guarda el mapa de calor interactivo con Folium."""
    # Reproyectar a coordenadas geográficas universales WGS84 (Lat/Lon)
    mapa_latlon = mapa_df.to_crs(epsg=4326)

    mapa = folium.Map(
        location=[19.4326, -99.1332],
        zoom_start=12,
        tiles=ESRI_TILE_URL,
        attr=ESRI_ATTR,
    )

    # Formatear puntos de calor: [Latitud, Longitud, Afluencia]
    datos_calor = [
        [geom.y, geom.x, afluencia]
        for geom, afluencia in zip(
            mapa_latlon.geometry, mapa_latlon["afluencia"]
        )
    ]

    HeatMap(
        datos_calor,
        radius=25,
        blur=15,
        max_zoom=13,
    ).add_to(mapa)

    mapa.save(output_html)
    print(f"✓ Mapa interactivo generado con éxito: {output_html}")


# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    print("Iniciando procesamiento de datos...")

    # 1. Carga y preparación
    df_metro = cargar_y_limpiar_datos(CSV_PATH)

    # 2. Análisis trimestral
    afluencia_q1 = filtrar_afluencia_q1_2026(df_metro)

    # 3. Integración geoespacial
    mapa_datos = unificar_datos_geoespaciales(
        afluencia_q1, SHAPEFILE_PATH, SHP_NAME_COL
    )

    # 4. Generación de mapas
    print("Generando mapa estático...")
    generar_mapa_estatico(mapa_datos)

    print("Generando mapa interactivo HTML...")
    generar_mapa_interactivo(mapa_datos, HTML_OUTPUT_PATH)
# 🚇 Análisis Geoespacial de Afluencia en el STC Metro CDMX (Q1 2026)

Un proyecto de análisis de movilidad urbana y procesamiento de datos geoespaciales para evaluar la distribución de usuarios en la red del Sistema de Transporte Colectivo (STC) Metro de la Ciudad de México durante el primer trimestre de 2026.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![GeoPandas](https://img.shields.io/badge/GeoPandas-139C5A?style=for-the-badge&logo=geopandas&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=folium&logoColor=white)

---

## 📌 Descripción del Proyecto

El STC Metro es la columna vertebral de la movilidad en la Zona Metropolitana del Valle de México. Este proyecto analiza más de 1 millón de registros de afluencia diaria con el objetivo de:

1. **Estandarizar y limpiar** bases de datos masivas con inconsistencias de codificación (*Mojibake* UTF-8 / Latin-1).
2. **Evaluar patrones de movilidad** en días laborales durante el primer trimestre de 2026 (Enero - Marzo).
3. **Mapear cuellos de botella y nodos críticos** mediante análisis de densidad kernel (*Kernel Density Estimation*) con GeoPandas y mapas interactivos en Folium.

---

## 🛠️ Tecnologías y Librerías

* **Lenguaje:** Python 3.9+
* **Procesamiento de Datos:** `pandas`, `numpy`
* **Análisis Geoespacial:** `geopandas`, `shapely`, `fiona`
* **Visualización de Datos:** `matplotlib`, `folium` (Plugin `HeatMap`)
* **Fuentes de Datos:** Datasets públicos de SEMOVI CDMX y capas Shapefile (.shp) de estaciones del Metro.

---

## 📊 Visualizaciones y Resultados

### 1. Mapa de Calor Interactivo (Folium)
Generación de una mancha térmica continua que consolida los niveles de saturación en estaciones clave como *Pantitlán*, *Indios Verdes* y *Constitución de 1917*.

> 💡 **Demo Interactiva:** Puedes abrir el archivo `mapa_calor_metro_q1_2026.html` en cualquier navegador web para explorar el mapa interactivo con zoom.

---

## 🚀 Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto localmente:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/metro-cdmx-afluencia-analysis.git](https://github.com/TU_USUARIO/metro-cdmx-afluencia-analysis.git)
cd metro-cdmx-afluencia-analysis
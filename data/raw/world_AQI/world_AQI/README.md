# 🌍 Global Air Quality Dataset (2014-2025)

**Overview:** A comprehensive, research-backed, globally expanding synthetic dataset simulating realistic air quality metrics across 24 sovereign nations from 2014 to 2025. Designed for environmental data science, MLOps, policy evaluation, and climate research. This is the master combined dataset containing all localized regions in a single continuous file.

**Format:** CSV (UTF-8)
**Total Records:** 331,920
**License:** CC BY-SA 4.0

---

## 📖 About This Dataset
This master dataset merges highly detailed, localized, and continuous synthetic air quality profiles for 24 major countries across the globe. Each localized region has been modeled with unique environmental multipliers tracking intense demographic shifts, monsoon washouts, transboundary haze, desert sandstorms, and extreme industrial footprints.

It is specifically designed for complex **data science/machine learning workflows** requiring vast amounts of clean, continuous geo-climatic data without missing values.

| Country                            | Records | Key Simulated Environmental Features                                       |
| ---------------------------------- | ------- | -------------------------------------------------------------------------- |
| **Australia**                      | 10,512  | Summer bushfires, coastal winds, regional dust storms                      |
| **Bangladesh**                     | 10,944  | Dry-season brick kiln spikes, intense monsoon washouts                     |
| **Brazil**                         | 12,528  | Amazon deforestation/biomass burning, industrial south                     |
| **China**                          | 22,032  | Winter heating baselines, industrial zones, afforestation                  |
| **Egypt**                          | 10,800  | Khamsin sandstorms, Nile Delta Black Cloud biomass burning                 |
| **Ethiopia**                       | 10,224  | Biomass cooking smoke, arid dust storms, low CO2 baseline                  |
| **France**                         | 11,664  | Winter heating inversions, traffic baselines, coastal dispersion           |
| **Germany**                        | 10,800  | Rhine-Ruhr industrial baselines, Baltic sea breezes                        |
| **India**                          | 20,592  | Crop stubble burning, high PM2.5 baselines, NCAP policies                  |
| **Indonesia**                      | 13,536  | Dry season peat fires (Sumatra/Kalimantan), Jabodetabek gridlock           |
| **Japan**                          | 22,752  | Yellow dust (Kosa), dense urban traffic, coastal clean air                 |
| **Mexico**                         | 12,672  | High-altitude basin inversions (CDMX), northern industry                   |
| **Nigeria**                        | 10,368  | Harmattan dust, generator fumes, gas flaring (Niger Delta)                 |
| **Pakistan**                       | 11,376  | Transboundary smog, brick kilns, massive winter inversions                 |
| **Philippines**                    | 15,408  | Habagat wet season, dense mega-city traffic, Amihan dry                  |
| **Russia**                         | 12,096  | Norilsk SO2, Siberian summer wildfires, winter "Black Sky"                 |
| **Saudi Arabia**                   | 10,800  | Haboob sandstorms, Jubail petrochemical SO2, summer AC load                |
| **South Africa**                   | 10,800  | Mpumalanga coal SO2, winter township heat inversions                       |
| **South Korea**                    | 12,672  | Hwangsa yellow dust, winter transboundary smog, Seoul density              |
| **Thailand**                       | 10,800  | Bangkok traffic baselines, Northern harvest smoke spikes                   |
| **Turkey**                         | 10,800  | Central Anatolia winter heating, Zonguldak coal region                     |
| **United Kingdom**                 | 10,800  | Winter heating, traffic congestion, coastal dispersion                     |
| **USA**                            | 28,080  | Wildfires (CA), Rust Belt industry, traffic inversions                     |
| **Vietnam**                        | 10,944  | Winter inversions, motorbike traffic, harvest burn season                  |

---

## 📋 Dataset Specifications
* **Total Rows:** 331,920
* **Total Columns:** 24
* **Date Range:** January 1, 2014 - December 1, 2025 (Monthly frequency per city)
* **Geographical Scope:** 24 sovereign nations spanning 5 continents
* **Simulated Null Target:** 0% missing data injection (100% continuous coverage).

---

## 🗂️ Global Database Schema / Column Dictionary

| Column Name | Description | Unit / Format |
| :--- | :--- | :--- |
| `Country` | Sovereign nation of the recorded municipality | Text (String) |
| `State` | The major province, state, or regional geographic boundary | Text (String) |
| `City` | The specific municipality or urban center | Text (String) |
| `Date` | Time of the recorded reading (1st of each month) | YYYY-MM-DD |
| `PM2.5` | Fine particulate matter (less than 2.5 micrometers) | µg/m³ |
| `PM10` | Coarse particulate matter (less than 10 micrometers) | µg/m³ |
| `NO` | Nitric oxide concentration | µg/m³ |
| `NO2` | Nitrogen dioxide concentration (Traffic/Energy indicator) | µg/m³ |
| `NOx` | Total nitrogen oxides | ppb |
| `NH3` | Ammonia concentration (Agricultural indicator) | µg/m³ |
| `CO` | Carbon monoxide concentration | mg/m³ |
| `SO2` | Sulfur dioxide concentration (Industrial/Coal indicator)| µg/m³ |
| `O3` | Ozone concentration at ground level | µg/m³ |
| `Benzene` | Benzene volatile organic compound (VOC) | µg/m³ |
| `Toluene` | Toluene volatile organic compound (VOC) | µg/m³ |
| `Xylene` | Xylene volatile organic compound (VOC) | µg/m³ |
| `AQI` | Calculated Air Quality Index based on PM2.5/PM10 | Integer (0-500+) |
| `AQI_Bucket` | Qualitative categorization of the AQI | Text (Good -> Severe) |
| `Wind_Speed` | Average sustained wind velocity | km/h |
| `Humidity` | Relative humidity percentage | % |
| `Deforestation_Rate_%` | Monthly localized deforestation rate | Percentage |
| `Industry_Growth_%` | Compound industrial scaling metric | Percentage |
| `CO2_Emission_MT` | Bulk Carbon Dioxide emissions | Metric Tons |
| `Population_Density_per_SqKm`| Calculated demographic density | People/sq km |

---

## 🌪️ Modeled Global Phenomena
This dataset programmatically simulates real-world environmental phenomena natively in the CSV logic:
*   **Hwangsa / Asian Dust:** Springtime particulate storms blowing across China into South Korea and Japan.
*   **Haboob / Shamal Winds:** Massive PM10 spikes sweeping Saudi Arabia and Egypt during spring/summer cycles.
*   **Tropical Monsoon Washouts:** Massive decreases in suspended matter during heavy rainy seasons in India, Bangladesh, Indonesia, and the Philippines.
*   **Slash-and-Burn Transboundary Haze:** Dry season particulate spikes emanating from deforested peatlands in Indonesia (Sumatra/Kalimantan) and Northern Thailand.
*   **Winter Smog / Township Heating:** Extreme SO2 + CO spikes during winter months in Northern Chinese rust belts and South African local townships.
*   **Megacity Gridlock:** High native NO2 and CO baselines locked into dense zones like Jabodetabek, Tokyo, London, Sao Paulo, and Los Angeles.

---

## 📜 Methodology & Sources

While the data is synthetically generated to provide comprehensive, uninterrupted monthly time-series records without gaps (unless intentionally added), the baselines, seasonal patterns, and regional variances are heavily anchored in real-world data.

**Global Sources Used for Modeling:**
*   **[World Bank Open Data](https://data.worldbank.org/)**: CO2 emissions, population density.
*   **[IQAir World Air Quality Report](https://www.iqair.com/)**: Historical PM2.5 baselines and country rankings.
*   **[Global Forest Watch](https://www.globalforestwatch.org/)**: Deforestation trends affecting biomass burning metrics.
*   **[Copernicus Atmosphere Monitoring Service (CAMS)](https://atmosphere.copernicus.eu/)**: Wildfire smoke transport and regional pollutant baselines.
*   **[OpenAQ](https://openaq.org/)**: Open-source local sensor data for ground-truthing.
*   **Regional Trackers:** Local monitoring from US EPA, EEA, India CPCB, NCEC KSA, and ASEAN Haze.

## 🌡️ AQI Reference 
Categorization uses standard US EPA breakpoints computed via simulated PM2.5 and PM10 concentrations:
* `Good`: 0-50 
* `Satisfactory`: 51-100
* `Moderate`: 101-150
* `Poor`: 151-200
* `Very Poor`: 201-300
* `Severe`: 301+

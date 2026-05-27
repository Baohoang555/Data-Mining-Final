# South Korea Air Quality Dataset (2014-2025)

**Format:** CSV (UTF-8) | **Records:** 12672 | **License:** CC BY-SA 4.0

## About This Dataset
This dataset tracks the synthesized air quality of South Korea across 9 major regions (including Seoul Capital Area, Busan-Ulsan-Gyeongnam, etc.), mapping out 88 key cities. It covers a twelve-year timeline (2014-2025), simulating localized pollution dynamics mapped to geographical layout, extreme urban population density, and specific environmental phenomena like Hwangsa (Yellow Dust) and transboundary winter smog.

### Data Sources and Methodology

| Domain | Simulated Sources (Proxy Baselines) |
| ------------- |:-------------:|
| **Environmental Data** | [Air Korea (Ministry of Environment)](https://www.airkorea.or.kr/) |
| **Socio-Economic Data** | [World Bank South Korea Sector](https://data.worldbank.org/country/korea-rep) |
| **Emissions & Deforestation** | Copernicus Atmosphere Monitoring Service |

## Dataset Specifications
* Dataset rows: 12672
* Date Range: Jan 1, 2014 - Dec 1, 2025 (Monthly Data)
* Geography: 88 cities sampled regionally.
* Simulated Null Target: 0% continuous dataset as per request.

## Column Dictionary
Consists of the standard 23-column layout:
`State`, `City`, `Date`, `PM2.5 (ug/m3)`, `PM10 (ug/m3)`, `NO (ug/m3)`, `NO2 (ug/m3)`, `NOx (ppb)`, `NH3 (ug/m3)`, `CO (mg/m3)`, `SO2 (ug/m3)`, `O3 (ug/m3)`, `Benzene (ug/m3)`, `Toluene (ug/m3)`, `Xylene (ug/m3)`, `AQI`, `AQI_Bucket`, `Wind_Speed (km/h)`, `Humidity (%)`, `Deforestation_Rate_%`, `Industry_Growth_%`, `CO2_Emission_MT`, `Population_Density_per_SqKm`.

## Seasonal and Temporal Patterns Modeled
*   **Hwangsa (Yellow Dust) Springs**: Frequent massive spikes in PM10 from March to May mimicking dust storms originating from the Gobi Desert.
*   **Winter Heating and Transboundary Smog**: Elevated PM2.5 and co baselines during Dec-Feb caused by stagnant air and industrial emissions from neighboring regions.
*   **Jangma (Monsoon) Washouts**: Sharp drops in particulate matter during July and August heavy rains.
*   **Industrial Hubs**: Ulsan, Pohang, Yeosu, and Gwangyang feature much higher baseline SO2 and NO2 levels.

## AQI Reference 
Uses standard US EPA breakpoints based on PM2.5 concentrations.

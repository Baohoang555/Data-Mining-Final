# Indonesia Air Quality Dataset (2014-2025)

**Format:** CSV (UTF-8) | **Records:** 13536 | **License:** CC BY-SA 4.0

## About This Dataset
This dataset captures the synthesized air quality conditions across the expansive archipelagic nation of Indonesia, detailing 94 cities across 9 major geographic regions (Java, Sumatra, Kalimantan, Sulawesi, etc.). Data spans the twelve-year timeline (2014-2025), simulating extreme humidity, the devastating dry season peatland forest fires, and the intense urbanization of its megacities.

### Data Sources and Methodology

| Domain | Simulated Sources (Proxy Baselines) |
| ------------- |:-------------:|
| **Environmental Data** | [Ministry of Environment and Forestry (KLHK)](https://www.menlhk.go.id/) |
| **Socio-Economic Data** | [Badan Pusat Statistik (BPS Kaltim/Java)](https://www.bps.go.id/) |
| **Emissions & Deforestation** | Global Forest Watch / ASEAN Haze Monitoring |

## Dataset Specifications
* Dataset rows: 13536
* Date Range: Jan 1, 2014 - Dec 1, 2025 (Monthly Data)
* Geography: 94 cities spanning Sumatra to Papua.
* Simulated Null Target: 0% continuous dataset as per request.

## Column Dictionary
`State`, `City`, `Date`, `PM2.5 (ug/m3)`, `PM10 (ug/m3)`, `NO (ug/m3)`, `NO2 (ug/m3)`, `NOx (ppb)`, `NH3 (ug/m3)`, `CO (mg/m3)`, `SO2 (ug/m3)`, `O3 (ug/m3)`, `Benzene (ug/m3)`, `Toluene (ug/m3)`, `Xylene (ug/m3)`, `AQI`, `AQI_Bucket`, `Wind_Speed (km/h)`, `Humidity (%)`, `Deforestation_Rate_%`, `Industry_Growth_%`, `CO2_Emission_MT`, `Population_Density_per_SqKm`.

## Seasonal and Temporal Patterns Modeled
*   **Dry Season Peat Fires (July-October)**: Massive multipliers on PM2.5/PM10 concentrated in Sumatra and Kalimantan, reflecting the severe slash-and-burn cycles and El Nino amplified transboundary haze.
*   **Wet Season Washout (Nov-March)**: Tropical monsoon rains significantly suppress suspended particulate matter.
*   **Megacity Traffic Baselines**: High NO2 and CO readings accurately reflecting the extreme gridlock in Greater Jakarta (Jabodetabek), Surabaya, and Bandung.
*   **Archipelagic Humidity**: Constant relative humidity rarely dipping below 70-80% year-round.

## AQI Reference 
Uses standard US EPA breakpoints based on PM2.5 concentrations.

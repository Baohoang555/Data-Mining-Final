# Vietnam Air Quality Dataset (2014-2025)

**Format:** CSV (UTF-8) | **Records:** 10944 | **License:** CC BY-SA 4.0

## About This Dataset
This dataset synthesizes ambient air quality measurements and climatic/socio-economic variables for Vietnam, tracking metrics across 8 primary regions and 76 distinct cities/provinces. It covers a twelve-year monthly timeline (2014-2025).

### Data Sources and Methodology

| Domain | Simulated Sources (Proxy Baselines) |
| ------------- |:-------------:|
| **Air Quality Guidelines** | [Vietnam Environment Administration (VEA)](http://vea.gov.vn/) & WHO Guidelines |
| **Socio-Economic Data** | [World Bank Vietnam Data](https://data.worldbank.org/country/vietnam) |
| **Deforestation Metrics** | [Global Forest Watch (Vietnam)](https://www.globalforestwatch.org/) |
| **Seasonal Adjustments** | National Centre for Hydro-Meteorological Forecasting (NCHMF) |

### Key Features
* **Extensive North-to-South Coverage**: Follows the highly heterogenous weather from the Red River Delta (Hanoi) down through the Central Highlands to the Mekong River Delta.
* **Winter Inversion Modeling**: Accurately simulates the significant PM2.5 spikes in Northern Vietnam (Oct-March) when thermal inversions trap industrial and vehicular pollution.
* **Agricultural Biomass Burning**: Captures acute seasonal pollution from rice straw and agricultural residue burning in the Mekong and Red River deltas.
* **Motorbike Density Correlation**: Mega-cities like Hanoi and Ho Chi Minh City correctly map elevated NO2 and CO aligned with massive two-wheeler traffic.

## Dataset Specifications
* Dataset rows: 10,944
* Date Range: Jan 1, 2014 - Dec 1, 2025 (Monthly Data)
* Geography: 76 cities and provinces across 8 defined clusters.
* Simulated Null Target: 0% continuous dataset without outages.

## Column Dictionary
Consists of the standard 23-column layout:
`State`, `City`, `Date`, `PM2.5 (ug/m3)`, `PM10 (ug/m3)`, `NO (ug/m3)`, `NO2 (ug/m3)`, `NOx (ppb)`, `NH3 (ug/m3)`, `CO (mg/m3)`, `SO2 (ug/m3)`, `O3 (ug/m3)`, `Benzene (ug/m3)`, `Toluene (ug/m3)`, `Xylene (ug/m3)`, `AQI`, `AQI_Bucket`, `Wind_Speed (km/h)`, `Humidity (%)`, `Deforestation_Rate_%`, `Industry_Growth_%`, `CO2_Emission_MT`, `Population_Density_per_SqKm`.

## Vietnam Regional Coverage
- Red River Delta (Hanoi, Hai Phong, Bac Ninh...)
- Northeast & Northwest (Mountainous frontiers)
- North & South Central Coastal (Da Nang, Hue, Nha Trang)
- Central Highlands (Da Lat, Buon Ma Thuot)
- Southeast (Ho Chi Minh City, Binh Duong, Dong Nai)
- Mekong River Delta (Can Tho, Ben Tre...)

## Pollution Tier Classification
*   **Mega-City**: (Hanoi, HCMC). Severe two-wheeler traffic, construction dust, massive baseline PM2.5 and NOx.
*   **Industrial Hubs**: (Hai Phong, Binh Duong, Dong Nai). High levels of SO2 driven by dense manufacturing parks.
*   **Coastal & Tourist**: (Da Nang, Nha Trang, Vung Tau). Much cleaner baselines leveraging ocean breezes to disperse particulates.
*   **Highlands**: Low baseline density but factors high-impact local forestry and agricultural burning.

## Seasonal and Temporal Patterns Modeled
*   **Northern Winter Inversion (Oct-Mar)**: PM2.5 increases structurally by ~60% in Red River Delta and mountainous Northern cities.
*   **Harvest Burn Season**: Biomass-related PM2.5 spikes simulating rice straw fires in agricultural deltas (Apr/Oct).
*   **Monsoon Washouts**: Modeled 35% reductions in ambient particulate matter across heavy summer precipitation.

## Suggested Use Cases
*   Impact correlations between regional economic manufacturing zones matching up with SO2 and PM.
*   Studying seasonal effects of Northern thermal inversion vs steady Southern humidity on population exposure limits.

## AQI Reference 
Uses standard US EPA breakpoints based on PM2.5 concentrations.

## License and Citation
Licensed under Creative Commons CC BY-SA 4.0. Please cite this artificial dataset responsibly if used in external reporting dashboards.

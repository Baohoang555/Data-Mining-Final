# South Africa Air Quality Dataset (2014-2025)

**Format:** CSV (UTF-8) | **Records:** 10800 | **License:** CC BY-SA 4.0

## About This Dataset
This dataset tracks the synthesized air quality of South Africa across all 9 provinces, mapping out roughly 75 cities from Johannesburg and Cape Town to the industrial Highveld. It covers a twelve-year timeline (2014-2025), simulating significant localized pollution dynamics mapped directly to geographical layout, population distributions, and unique environmental phenomena such as extreme coal-power emissions and winter township heating inversions.

### Data Sources and Methodology

| Domain | Simulated Sources (Proxy Baselines) |
| ------------- |:-------------:|
| **Environmental Data** | [South African Weather Service (SAWS)](https://www.weathersa.co.za/) & DEA |
| **Socio-Economic Data** | [World Bank South Africa Sector](https://data.worldbank.org/country/south-africa) |
| **Emissions & Deforestation** | Copernicus Atmosphere Monitoring Service |

## Dataset Specifications
* Dataset rows: 10800
* Date Range: Jan 1, 2014 - Dec 1, 2025 (Monthly Data)
* Geography: 75 cities sampled regionally.
* Simulated Null Target: 0% continuous dataset as per request.

## Column Dictionary
Consists of the standard 23-column layout:
`State`, `City`, `Date`, `PM2.5 (ug/m3)`, `PM10 (ug/m3)`, `NO (ug/m3)`, `NO2 (ug/m3)`, `NOx (ppb)`, `NH3 (ug/m3)`, `CO (mg/m3)`, `SO2 (ug/m3)`, `O3 (ug/m3)`, `Benzene (ug/m3)`, `Toluene (ug/m3)`, `Xylene (ug/m3)`, `AQI`, `AQI_Bucket`, `Wind_Speed (km/h)`, `Humidity (%)`, `Deforestation_Rate_%`, `Industry_Growth_%`, `CO2_Emission_MT`, `Population_Density_per_SqKm`.

## Seasonal and Temporal Patterns Modeled
*   **Southern Hemisphere Winter**: Massive PM2.5 and CO spikes from June to August, simulating dense township coal/wood combustion paired with severe thermal inversions.
*   **Highveld Industrial Zones**: Unusually high sustained SO2 baselines specifically in the Mpumalanga region (eMalahleni, Secunda) mimicking deep coal and petrochemical operations.
*   Coastal dispersion patterns cleanly sweeping Cape Town and Durban.

## AQI Reference 
Uses standard US EPA breakpoints based on PM2.5 concentrations.

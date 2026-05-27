# France Air Quality Dataset (2014-2025)

**Format:** CSV (UTF-8) | **Records:** 11664 | **License:** CC BY-SA 4.0

## About This Dataset
This dataset tracks the synthesized air quality of France across 12 regions mapping out 75 cities from Île-de-France to Provence-Alpes-Côte d'Azur. It covers a twelve-year timeline (2014-2025), simulating significant localized pollution dynamics mapped directly to geographical layout and population distributions.

### Data Sources and Methodology

| Domain | Simulated Sources (Proxy Baselines) |
| ------------- |:-------------:|
| **Environmental Data** | [Prev'air / INERIS (France)](https://www.prevair.org/) |
| **Socio-Economic Data** | [World Bank France Sector](https://data.worldbank.org/country/france) |
| **Emissions & Deforestation** | Copernicus Atmosphere Monitoring Service |

### Key Features
* **Detailed Regional Coverage**: Contains evenly-distributed sampling of major economic clusters and provincial cities.
* **Realistic Weather & Seasonal Patterns**: Modes extreme weather, winter inversions, coastal dispersion, and traffic-derived emissions specific to France.
* **Tier-based Spatial Density**: Metropolitan areas and industrial hubs model drastically higher emissions than secondary/coastal baseline cities.

## Dataset Specifications
* Dataset rows: 11664
* Date Range: Jan 1, 2014 - Dec 1, 2025 (Monthly Data)
* Geography: 75 cities sampled regionally.
* Simulated Null Target: 0% continuous dataset as per request.

## Column Dictionary
Consists of the standard 23-column layout:
`State`, `City`, `Date`, `PM2.5 (ug/m3)`, `PM10 (ug/m3)`, `NO (ug/m3)`, `NO2 (ug/m3)`, `NOx (ppb)`, `NH3 (ug/m3)`, `CO (mg/m3)`, `SO2 (ug/m3)`, `O3 (ug/m3)`, `Benzene (ug/m3)`, `Toluene (ug/m3)`, `Xylene (ug/m3)`, `AQI`, `AQI_Bucket`, `Wind_Speed (km/h)`, `Humidity (%)`, `Deforestation_Rate_%`, `Industry_Growth_%`, `CO2_Emission_MT`, `Population_Density_per_SqKm`.

## France Administrative Level Coverage
- Covers major hubs, massive industrial centers, down to less-populated rural municipalities.

## Pollution Tier Classification
*   **Mega-City / Primary Urban Hub**: Extreme population density and subsequent NO2 / CO concentrations.
*   **Industrial Hub**: Major contributor to baseline SO2 and airborne particulate matters.
*   **Provincial & Coastal**: Cleanest baseline winds with less population stress.

## Seasonal and Temporal Patterns Modeled
*   Adjusted specifically to France's prevalent weather patterns such as winter inversions or local agricultural burnoff phenomenons.

## Suggested Use Cases
*   Spatio-temporal mapping of pollution tied to urban sprawl.
*   ML forecasting of particulate escalations mapped to extreme seasonal weather conditions.

## AQI Reference 
Uses standard US EPA breakpoints based on PM2.5 concentrations.

## License and Citation
Licensed under Creative Commons CC BY-SA 4.0. Please cite this artificial dataset responsibly if used in external reporting dashboards.

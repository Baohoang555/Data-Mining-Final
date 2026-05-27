# Russia Air Quality Index (AQI) Dataset (2014-2025)

**Format:** CSV (UTF-8)  
**Records:** 12,096  
**License:** CC BY-SA 4.0  

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 8 Federal Districts of Russia** with **84 major cities** across a **12-year span (Jan 2014 -- Dec 2025)**. 

Russia's vast geography presents unique air quality challenges. While many regions boast pristine taiga air, highly concentrated industrial centers (particularly in the Ural and Siberian districts) suffer from extreme pollution. This dataset accurately models chronic metallurgical emissions, the infamous winter "Black Sky" inversion events, and the escalating crisis of summer wildfires in Siberia and the Far East.

> [!NOTE]
> **Real-World Missing Data Simulation**: Per user specification, this dataset intentionally includes approximately **~3.8% missing values (nulls)** for pollutant columns. This accurately simulates real-world sensor downtime, calibration errors, and harsh weather-induced equipment failures common in remote Russian monitoring stations. The missing rate is kept strictly under 8%.

### Data Sources and Methodology

Due to the limited availability of continuous, centralized open data from Roshydromet, this dataset synthesizes pollution patterns, baselines, and seasonal dynamics from the following sources:

| Source | Link | Usage |
|---|---|---|
| **Roshydromet** | [meteorf.gov.ru](https://www.meteorf.gov.ru/) | Russian Federal Service for Hydrometeorology and Environmental Monitoring baseline reports |
| **IQAir** | [iqair.com/russia](https://www.iqair.com/russia) | Annual PM2.5 baselines and historical city data (e.g., Krasnoyarsk) |
| **Copernicus (CAMS)** | [atmosphere.copernicus.eu](https://atmosphere.copernicus.eu/) | Satellite data tracking Siberian wildfire smoke plumes and CO emissions |
| **Rosstat** | [rosstat.gov.ru](https://rosstat.gov.ru/) | Russian Federal State Statistics Service for population density and industrial growth |
| **Blacksmith Institute** | [worstpolluted.org](http://www.worstpolluted.org/) | Historical pollution assessments for Norilsk and heavy metal/SO2 baselines |
| **OpenAQ** | [openaq.org](https://openaq.org/) | Aggregated sensor data for Moscow and St. Petersburg |

### Key Features

- **Geographic coverage** -- All 8 Federal Districts: Central, Northwestern, Southern, North Caucasian, Volga, Ural, Siberian, and Far Eastern.
- **Monthly granularity** -- 144 months (Jan 2014 -- Dec 2025).
- **23 columns** -- Pollutants, meteorological, socio-economic, and environmental indicators.
- **Norilsk SO2 Anomaly** -- Explicitly models extreme Sulphur Dioxide (SO2) and heavy metal pollution in Norilsk, home to the world's largest nickel and palladium smelting operations.
- **"Black Sky" Events (Черное небо)** -- Models severe winter temperature inversions in Siberian and Ural cities (e.g., Krasnoyarsk, Chelyabinsk) that trap coal heating and industrial smog at ground level.
- **Siberian Wildfires** -- Models extreme PM2.5 and CO spikes during July and August in the Siberian and Far Eastern districts, particularly reflecting the catastrophic fire years of 2019-2021.
- **Missing Data Realism** -- Empty strings (NaN) randomly distributed throughout the pollutant columns to test data imputation strategies in MLOps pipelines.

---

## Dataset Specifications

| Property | Value |
|---|---|
| **File** | `russia_air_quality_2014_2025.csv` |
| **Format** | CSV (UTF-8) |
| **Size** | ~1.6 MB |
| **Records** | 12,096 |
| **Federal Districts** | 8 |
| **Cities** | 84 |
| **Date Range** | 2014-01-01 to 2025-12-01 |
| **Frequency** | Monthly |
| **Missing Values** | ~3.8% randomly distributed across pollutants |

---

## Column Dictionary

### Identifiers

| # | Column | Description | Type |
|---|---|---|---|
| 1 | `Federal_District` | Administrative Federal District name | String |
| 2 | `City` | City name | String |
| 3 | `Date` | Observation date (1st of each month) | Date (YYYY-MM-DD) |

### Air Pollutants (Includes Nulls)

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 4 | `PM2.5 (ug/m3)` | Fine Particulate Matter <= 2.5 micrometers | ug/m3 | Float / Null |
| 5 | `PM10 (ug/m3)` | Particulate Matter <= 10 micrometers | ug/m3 | Float / Null |
| 6 | `NO (ug/m3)` | Nitric Oxide | ug/m3 | Float / Null |
| 7 | `NO2 (ug/m3)` | Nitrogen Dioxide | ug/m3 | Float / Null |
| 8 | `NOx (ppb)` | Total Nitrogen Oxides | ppb | Float / Null |
| 9 | `NH3 (ug/m3)` | Ammonia | ug/m3 | Float / Null |
| 10 | `CO (mg/m3)` | Carbon Monoxide | mg/m3 | Float / Null |
| 11 | `SO2 (ug/m3)` | Sulphur Dioxide | ug/m3 | Float / Null |
| 12 | `O3 (ug/m3)` | Ground-level Ozone | ug/m3 | Float / Null |
| 13 | `Benzene (ug/m3)` | Benzene (VOC) | ug/m3 | Float / Null |
| 14 | `Toluene (ug/m3)` | Toluene (VOC) | ug/m3 | Float / Null |
| 15 | `Xylene (ug/m3)` | Xylene (VOC) | ug/m3 | Float / Null |

### Air Quality Index

| # | Column | Description | Type |
|---|---|---|---|
| 16 | `AQI` | Air Quality Index (mapped using standard US EPA breakpoints) | Integer / Null |
| 17 | `AQI_Bucket` | Category: Good / Moderate / Unhealthy for Sensitive Groups / Unhealthy / Very Unhealthy / Hazardous | String / Null |

### Meteorological Parameters

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 18 | `Wind_Speed (km/h)` | Average wind speed | km/h | Float |
| 19 | `Humidity (%)` | Relative humidity | % | Float |

### Socio-Environmental Indicators

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 20 | `Deforestation_Rate_%` | Annual deforestation/tree cover loss rate (Wildfire driven) | % | Float |
| 21 | `Industry_Growth_%` | Industrial output year-over-year growth | % | Float |
| 22 | `CO2_Emission_MT` | District-level CO2 emissions | Million Metric Tons | Float |
| 23 | `Population_Density_per_SqKm` | People per square kilometer | per km2 | Float |

---

## City Coverage by District

| Federal District | Cities | Count |
|---|---|---|
| **Central** | Moscow, Voronezh, Yaroslavl, Ryazan, Tula, Lipetsk, Ivanovo, Bryansk, Tver, Belgorod, Vladimir, Kaluga, Oryol, Smolensk | 14 |
| **Volga** | Kazan, Nizhny Novgorod, Samara, Ufa, Perm, Saratov, Tolyatti, Izhvesk, Ulyanovsk, Orenburg, Penza, Naberezhnye Chelny, Kirov, Cheboksary | 14 |
| **Siberian** | Novosibirsk, Krasnoyarsk, Omsk, Barnaul, Irkutsk, Tomsk, Kemerovo, Novokuznetsk, Norilsk, Bratsk, Abakan | 11 |
| **Northwestern** | Saint Petersburg, Kaliningrad, Arkhangelsk, Cherepovets, Vologda, Murmansk, Petrozavodsk, Syktyvkar, Pskov, Veliky Novgorod | 10 |
| **Far Eastern** | Vladivostok, Khabarovsk, Yakutsk, Ulan-Ude, Chita, Komsomolsk-on-Amur, Blagoveshchensk, Yuzhno-Sakhalinsk, Petropavlovsk-Kamchatsky, Magadan | 10 |
| **Southern** | Rostov-on-Don, Krasnodar, Volgograd, Astrakhan, Sochi, Taganrog, Novorossiysk, Volzhsky, Armavir | 9 |
| **North Caucasian** | Makhachkala, Stavropol, Vladikavkaz, Grozny, Nalchik, Pyatigorsk, Khasavyurt, Kislovodsk | 8 |
| **Ural** | Yekaterinburg, Chelyabinsk, Tyumen, Magnitogorsk, Nizhny Tagil, Kurgan, Surgut, Nizhnevartovsk | 8 |

---

## Pollution Tier Classification

| Tier | Example Cities | PM2.5 Baseline (ug/m3) | Primary Driver |
|---|---|---|---|
| **Severe Industrial** | Norilsk, Krasnoyarsk, Chelyabinsk, Magnitogorsk | 40--150 | Heavy metallurgy, mining, coal heating, "Black Sky" events |
| **High Urban** | Moscow, Saint Petersburg, Yekaterinburg | 15--45 | High vehicular traffic, municipal heating systems |
| **Moderate** | Volgograd, Saratov, Kazan | 10--30 | Mixed light industry and urban traffic |
| **Moderate/Clean** | Sochi, Stavropol | 8--22 | Coastal or mountainous terrain, lower industrial density |
| **Clean Taiga** | Yakutsk, Magadan (Outside Fire Season) | 3--12 | Vast uninhabited forests; extremely clean air baseline |

---

## Seasonal and Temporal Patterns Modeled

| Season | Months | Effect | Explanation |
|---|---|---|---|
| **Deep Winter** | Dec -- Feb | Inversion Peak | High heating demand (coal/gas); severe temperature inversions trap industrial and urban smog at ground level causing "Black Sky" alerts. |
| **Spring** | Mar -- May | Transition | Snowmelt; inversion layers break up; wind speeds increase improving air quality. |
| **Mid-Summer** | Jul -- Aug | Wildfire Peak | Intense heat waves trigger massive wildfires in the Siberian and Far Eastern taiga, causing extreme regional PM2.5 and CO spikes. |
| **Autumn** | Sep -- Nov | Moderate | Generally good air quality before the onset of the long winter. |

### Special Events
- **Norilsk SO2 Plume**: Norilsk is modeled with a permanent 5.0x multiplier to SO2 to reflect its status as one of the world's most severe singular sources of sulfur dioxide.
- **2019-2021 Wildfire Crisis**: Deforestation rates, PM2.5, and CO levels in the Siberian and Far Eastern districts are modeled with massive multipliers (up to 10x) during July and August of these specific years to reflect catastrophic real-world fire seasons.
- **Missing Data (NaNs)**: Represents realistic constraints of monitoring in extreme climates. Data pipelines utilizing this CSV must include `.fillna()`, `.dropna()`, or interpolation steps.

---

## License and Citation

Released under **[Creative Commons CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.
You are free to share and adapt this dataset for any purpose, provided you give appropriate credit and distribute contributions under the same license.

Please cite:

```
Russia Air Quality Index Dataset (2014-2025)
8 Federal Districts | 84 Cities | Monthly Observations (Jan 2014 -- Dec 2025)
Data modeled on published statistics from Roshydromet, Copernicus (CAMS), 
IQAir, and Rosstat.
```

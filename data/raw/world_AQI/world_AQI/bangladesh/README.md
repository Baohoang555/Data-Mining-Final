# Bangladesh Air Quality Index (AQI) Dataset (2014-2025)

**Format:** CSV (UTF-8)  
**Records:** 10,944  
**License:** CC BY-SA 4.0  

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 8 administrative divisions of Bangladesh** with **76 cities and districts** across a **12-year span (Jan 2014 -- Dec 2025)**. Bangladesh consistently ranks among the most polluted countries on Earth, with annual average PM2.5 concentrations exceeding WHO guidelines by more than 15 times. This dataset captures the extreme dry-season pollution driven by brick kilns, the monsoon washout effect, and the rapid urbanization of the Dhaka airshed.

### Data Sources and Methodology

This dataset synthesizes pollution patterns, baselines, and seasonal dynamics from the following verified sources:

| Source | Link | Usage |
|---|---|---|
| **DoE (Department of Environment)** | [doe.gov.bd](http://www.doe.gov.bd/) | National air quality monitoring framework and CAMS station data |
| **CASE Project** | [case.doe.gov.bd](http://case.doe.gov.bd/) | Clean Air and Sustainable Environment: Continuous Air Quality Monitoring Stations |
| **IQAir** | [iqair.com/bangladesh](https://www.iqair.com/bangladesh) | Annual PM2.5 baselines and country/city rankings (2018-2025) |
| **AQLI (Univ. of Chicago)** | [aqli.epic.uchicago.edu](https://aqli.epic.uchicago.edu/country/bangladesh/) | Long-term particulate pollution exposure modeling |
| **World Bank** | [data.worldbank.org](https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3?locations=BD) | Annual PM2.5 exposure and CO2 emission estimates |
| **BBS (Bangladesh Bureau of Statistics)** | [bbs.gov.bd](http://www.bbs.gov.bd/) | Population density, industrial growth, and demographic data |
| **Global Forest Watch** | [globalforestwatch.org](https://www.globalforestwatch.org/dashboards/country/BGD/) | Deforestation rates and tree cover loss |
| **OpenAQ** | [openaq.org](https://openaq.org/) | Aggregated sensor data for Dhaka and Chattogram |

### Key Features

- **Geographic coverage** -- All 8 divisions: Dhaka, Chattogram, Rajshahi, Khulna, Barishal, Sylhet, Rangpur, Mymensingh.
- **Monthly granularity** -- 144 months (Jan 2014 -- Dec 2025).
- **23 columns** -- Pollutants, meteorological, socio-economic, and environmental indicators.
- **Brick Kiln Season** -- Models the severe dry-season (Nov--Apr) pollution spike caused by ~7,000+ brick kilns, which contribute approximately 40% of PM2.5 in the Dhaka airshed.
- **Monsoon Washout** -- Heavy rainfall during Jun--Sep dramatically reduces airborne particulate matter.
- **Indo-Gangetic Spillover** -- Transboundary pollution from India's Bihar and West Bengal affecting Rajshahi and Rangpur divisions during winter months.
- **Dhaka Airshed Hotspots** -- City-level overrides for Gazipur, Narayanganj, Tongi, Savar, and Ashulia reflecting their role as garment industry and brick kiln hubs.

---

## Dataset Specifications

| Property | Value |
|---|---|
| **File** | `bangladesh_air_quality_2014_2025.csv` |
| **Format** | CSV (UTF-8) |
| **Size** | ~1.5 MB |
| **Records** | 10,944 |
| **Divisions** | 8 |
| **Cities/Districts** | 76 |
| **Date Range** | 2014-01-01 to 2025-12-01 |
| **Frequency** | Monthly |

---

## Column Dictionary

### Identifiers

| # | Column | Description | Type |
|---|---|---|---|
| 1 | `Division` | Administrative Division name | String |
| 2 | `City` | City or District name | String |
| 3 | `Date` | Observation date (1st of each month) | Date (YYYY-MM-DD) |

### Air Pollutants

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 4 | `PM2.5 (ug/m3)` | Fine Particulate Matter <= 2.5 micrometers | ug/m3 | Float |
| 5 | `PM10 (ug/m3)` | Particulate Matter <= 10 micrometers | ug/m3 | Float |
| 6 | `NO (ug/m3)` | Nitric Oxide | ug/m3 | Float |
| 7 | `NO2 (ug/m3)` | Nitrogen Dioxide | ug/m3 | Float |
| 8 | `NOx (ppb)` | Total Nitrogen Oxides | ppb | Float |
| 9 | `NH3 (ug/m3)` | Ammonia | ug/m3 | Float |
| 10 | `CO (mg/m3)` | Carbon Monoxide | mg/m3 | Float |
| 11 | `SO2 (ug/m3)` | Sulphur Dioxide | ug/m3 | Float |
| 12 | `O3 (ug/m3)` | Ground-level Ozone | ug/m3 | Float |
| 13 | `Benzene (ug/m3)` | Benzene (VOC) | ug/m3 | Float |
| 14 | `Toluene (ug/m3)` | Toluene (VOC) | ug/m3 | Float |
| 15 | `Xylene (ug/m3)` | Xylene (VOC) | ug/m3 | Float |

### Air Quality Index

| # | Column | Description | Type |
|---|---|---|---|
| 16 | `AQI` | Air Quality Index (mapped using standard US EPA breakpoints) | Integer |
| 17 | `AQI_Bucket` | Category: Good / Moderate / Unhealthy for Sensitive Groups / Unhealthy / Very Unhealthy / Hazardous | String |

### Meteorological Parameters

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 18 | `Wind_Speed (km/h)` | Average wind speed | km/h | Float |
| 19 | `Humidity (%)` | Relative humidity | % | Float |

### Socio-Environmental Indicators

| # | Column | Description | Unit | Type |
|---|---|---|---|---|
| 20 | `Deforestation_Rate_%` | Annual deforestation/tree cover loss rate | % | Float |
| 21 | `Industry_Growth_%` | Industrial output year-over-year growth (garment-led) | % | Float |
| 22 | `CO2_Emission_MT` | Division-level CO2 emissions | Million Metric Tons | Float |
| 23 | `Population_Density_per_SqKm` | People per square kilometer (highest in the world) | per km2 | Float |

---

## City Coverage by Division

| Division | Cities/Districts | Count |
|---|---|---|
| **Dhaka** | Dhaka, Gazipur, Narayanganj, Narsingdi, Tangail, Manikganj, Munshiganj, Faridpur, Gopalganj, Kishoreganj, Madaripur, Rajbari, Shariatpur, Savar, Tongi, Ashulia | 16 |
| **Chattogram** | Chattogram, Cumilla, Cox's Bazar, Brahmanbaria, Noakhali, Feni, Chandpur, Lakshmipur, Khagrachhari, Rangamati, Bandarban, Sitakunda, Teknaf | 13 |
| **Khulna** | Khulna, Jashore, Kushtia, Satkhira, Bagerhat, Narail, Meherpur, Chuadanga, Jhenaidah, Magura | 10 |
| **Rangpur** | Rangpur, Dinajpur, Gaibandha, Kurigram, Lalmonirhat, Nilphamari, Panchagarh, Thakurgaon, Saidpur | 9 |
| **Rajshahi** | Rajshahi, Bogura, Pabna, Sirajganj, Natore, Naogaon, Chapainawabganj, Joypurhat | 8 |
| **Barishal** | Barishal, Patuakhali, Bhola, Pirojpur, Jhalokati, Barguna, Amtali, Gournadi | 8 |
| **Sylhet** | Sylhet, Moulvibazar, Habiganj, Sunamganj, Sreemangal, Beanibazar | 6 |
| **Mymensingh** | Mymensingh, Jamalpur, Netrokona, Sherpur, Trishal, Bhaluka | 6 |

---

## Pollution Tier Classification

Based on DoE CAMS data, IQAir annual reports, and CASE project findings:

| Tier | Divisions | PM2.5 Baseline (ug/m3) | Primary Driver |
|---|---|---|---|
| **Severe** | Dhaka | 55--170 | Traffic, construction dust, ~7,000 brick kilns in airshed, garment industry |
| **Very High** | Rajshahi, Rangpur | 40--130 | Brick kilns, dry climate, Indo-Gangetic transboundary spillover |
| **High** | Chattogram, Khulna, Mymensingh | 30--90 | Port/ship-breaking (Chattogram), industrial activity, peri-urban sprawl |
| **Moderate** | Barishal, Sylhet | 15--50 | Lower industrial density, coastal/hilly terrain, tea-garden belt (Sylhet) |

---

## Seasonal and Temporal Patterns Modeled

| Season | Months | Effect | Explanation |
|---|---|---|---|
| **Dry (Brick Kiln) Season** | Nov -- Apr | Extreme Peak | Brick kilns fire up (only operate in dry season); temperature inversions trap pollutants at ground level; no rainfall to wash out particles. January is typically the worst month. |
| **Pre-Monsoon** | May | Transition | Early thunderstorms begin; pollution starts to decrease. |
| **Monsoon** | Jun -- Sep | Minimum | Heavy, sustained rainfall washes out nearly all airborne particulate matter. AQI drops to "Moderate" or "Good" across most divisions. |
| **Post-Monsoon** | Oct | Rising | Rains taper off; kilns have not yet started but baseline urban pollution returns. |

### Special Events
- **Brick Kiln Impact**: Approximately 7,000+ brick kilns operate exclusively during the dry season across Bangladesh. In the Dhaka airshed, they contribute an estimated 40% of PM2.5. The dataset applies a specific brick kiln multiplier (1.3x--1.8x for Dhaka) during Nov--Apr.
- **Ship-Breaking at Sitakunda**: Modeled as a persistent pollution source for Chattogram Division, elevating SO2 and heavy metal markers year-round.
- **Indo-Gangetic Spillover**: Rajshahi and Rangpur divisions receive transboundary PM2.5 from India's Bihar and West Bengal during Dec--Feb, modeled as a 1.1x--1.4x additional multiplier.
- **COVID-19 Lockdowns (2020)**: Pollution reduction modeled during Mar--Jun 2020.
- **Long-term Trends**: Pollution worsening at ~2.5%/year through 2020 due to rapid garment-sector industrialization, with a slight plateau post-2020 due to Zigzag kiln transitions.

---

## Suggested Use Cases

1. **Brick Kiln Policy Analysis** -- Compare dry season (Nov--Apr) vs monsoon (Jun--Sep) to quantify brick kiln contribution to PM2.5.
2. **Dhaka Airshed Study** -- Analyse the spatial gradient across Dhaka, Gazipur, Narayanganj, Savar, and Tongi to understand intra-city pollution variation.
3. **Transboundary Pollution** -- Study the Indo-Gangetic spillover effect on Rajshahi and Rangpur during winter months; compare with India and Pakistan datasets.
4. **Garment Industry Impact** -- Correlate `Industry_Growth_%` with AQI trends in the Dhaka Division to study the environmental cost of economic growth.
5. **Monsoon Impact on AQI** -- Use the extreme seasonal swing (AQI 300+ in January vs AQI <50 in July) to study the role of precipitation in pollution control.

---

## AQI Reference

| AQI Range | Category | Health Advisory |
|---|---|---|
| 0 -- 50 | Good | Air quality is satisfactory. |
| 51 -- 100 | Moderate | Acceptable; moderate health concern for sensitive individuals. |
| 101 -- 150 | Unhealthy for Sensitive Groups | Members of sensitive groups may experience health effects. |
| 151 -- 200 | Unhealthy | Everyone may begin to experience health effects. |
| 201 -- 300 | Very Unhealthy | Health warnings of emergency conditions. |
| 301 -- 500+ | Hazardous | Emergency conditions; the entire population is likely to be affected. |

---

## License and Citation

Released under **[Creative Commons CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.
You are free to share and adapt this dataset for any purpose, provided you give appropriate credit and distribute contributions under the same license.

Please cite:

```
Bangladesh Air Quality Index Dataset (2014-2025)
8 Divisions | 76 Cities/Districts | Monthly Observations (Jan 2014 -- Dec 2025)
Data modeled on published statistics from DoE, CASE Project, IQAir, AQLI,
World Bank, and Bangladesh Bureau of Statistics.
```

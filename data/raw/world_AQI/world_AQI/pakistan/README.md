# Pakistan Air Quality Index (AQI) Dataset (2014-2025)

**Format:** CSV (UTF-8)  
**Records:** 11,376  
**License:** CC BY-SA 4.0  

---

## About This Dataset

A comprehensive, research-backed Air Quality dataset covering **all 4 provinces, the capital territory, and Gilgit-Baltistan** with **69 major cities** across a **12-year span (Jan 2014 -- Dec 2025)**. Pakistan is currently facing one of the most severe air pollution crises globally. This dataset accurately reflects the extreme winter smog events (particularly in Punjab), high baseline pollution from industrial and vehicular emissions, and the impact of agricultural crop burning.

### Data Sources and Methodology

Due to the lack of a centralized, continuous EPA historical database in Pakistan, this dataset is modeled using a synthesis of data patterns from the following sources:

| Source | Link | Usage |
|---|---|---|
| **IQAir** | [iqair.com/pakistan](https://www.iqair.com/pakistan) | Annual pollution rankings, PM2.5 baselines, and historical city data |
| **Ministry of Climate Change** | [mocc.gov.pk](https://mocc.gov.pk/) | National environmental policy impacts and deforestation rates |
| **AQLI (Univ. of Chicago)** | [aqli.epic.uchicago.edu](https://aqli.epic.uchicago.edu/country/pakistan/) | Long-term particulate pollution exposure models |
| **Pakistan Bureau of Statistics** | [pbs.gov.pk](https://www.pbs.gov.pk/) | Population density and industrial growth data |
| **Global Carbon Project** | [globalcarbonproject.org](https://www.globalcarbonproject.org/) | Modeled CO2 emissions by region |
| **OpenAQ** | [openaq.org](https://openaq.org/) | Global air quality data aggregation |

### Key Features

- **Geographic coverage** -- Punjab, Sindh, Khyber Pakhtunkhwa, Balochistan, Islamabad, and Gilgit-Baltistan.
- **Monthly granularity** -- 144 months (Jan 2014 -- Dec 2025).
- **23 columns** -- Pollutants, meteorological, socio-economic, and environmental.
- **The "Fifth Season" (Winter Smog)** -- Modeled severe PM2.5 and PM10 spikes in Punjab (Lahore, Faisalabad) during Nov--Feb caused by temperature inversions and crop stubble burning.
- **High Baseline Pollution** -- Reflects the reality that major Pakistani cities routinely exceed WHO guidelines by 10x to 20x.
- **Population Density Dynamics** -- Modeled to reflect Pakistan's rapid urbanization and high population growth over the decade.
- **Sindh Heat/Dust Effect** -- Additional pollution multipliers for Sindh during May--July reflecting extreme heat and dust in cities like Jacobabad.

---

## Dataset Specifications

| Property | Value |
|---|---|
| **File** | `pakistan_air_quality_2014_2025.csv` |
| **Format** | CSV (UTF-8) |
| **Size** | ~1.4 MB |
| **Records** | 9,936 |
| **Provinces/Territories** | 6 |
| **Cities** | 69 |
| **Date Range** | 2014-01-01 to 2025-12-01 |
| **Frequency** | Monthly |

---

## Column Dictionary

### Identifiers

| # | Column | Description | Type |
|---|---|---|---|
| 1 | `Province` | Province or Territory name | String |
| 2 | `City` | City name | String |
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
| 21 | `Industry_Growth_%` | Industrial output year-over-year growth | % | Float |
| 22 | `CO2_Emission_MT` | Province-level CO2 emissions | Million Metric Tons | Float |
| 23 | `Population_Density_per_SqKm` | People per square kilometer | per km2 | Float |

---

## City Coverage by Province

| Province | Cities | Count |
|---|---|---|
| **Punjab** | Lahore, Faisalabad, Rawalpindi, Multan, Gujranwala, Sialkot, Bahawalpur, Sargodha, Sheikhupura, Jhang, Rahim Yar Khan, Gujrat, Jhelum, Sahiwal, Okara, Wah Cantonment, Dera Ghazi Khan, Chiniot, Kasur, Mianwali, Hafizabad, Attock, Vehari, Muzaffargarh | 24 |
| **Sindh** | Karachi, Hyderabad, Sukkur, Larkana, Mirpur Khas, Nawabshah, Thatta, Badin, Jacobabad, Shikarpur, Khairpur, Dadu, Tando Allahyar, Umerkot | 14 |
| **Khyber Pakhtunkhwa** | Peshawar, Mardan, Mingora (Swat), Kohat, Abbottabad, Dera Ismail Khan, Nowshera, Charsadda, Bannu, Mansehra, Swabi, Haripur, Chitral, Dir | 14 |
| **Balochistan** | Quetta, Khuzdar, Turbat, Chaman, Gwadar, Hub, Sibi, Zhob, Loralai, Kharan, Mastung, Kalat | 12 |
| **Islamabad Capital Territory** | Islamabad | 1 |
| **Gilgit-Baltistan** | Gilgit, Skardu, Hunza, Chilas | 4 |

---

## Pollution Tier Classification

Based on IQAir reports and global burden of disease metrics:

| Tier | Provinces | PM2.5 Baseline (ug/m3) |
|---|---|---|
| **Severe** | Punjab (e.g., Lahore, Faisalabad) | 60--180 |
| **Very High** | Sindh, Khyber Pakhtunkhwa | 45--130 |
| **High** | Islamabad, Balochistan | 30--85 |
| **Clean** | Gilgit-Baltistan | 8--25 |

---

## Seasonal and Temporal Patterns Modeled

| Season | Months | Effect | Explanation |
|---|---|---|---|
| **Winter Smog** | Nov -- Feb | Extreme Peak | Temperature inversions trap pollutants; massive agricultural stubble burning across the Indo-Gangetic Plain; brick kilns and heavy vehicular traffic. |
| **Spring** | Mar -- May | Transition | Gradual decrease in particulate matter as temperatures rise and wind speeds increase. |
| **Monsoon** | Jun -- Sep | Moderate/Low | Summer rains wash out significant amounts of particulate matter. |
| **Autumn** | Oct | Rising | Stubble burning begins; temperatures start to drop. |

### Special Events
- **The "Fifth Season"**: The extreme winter smog in Lahore is so severe it is locally referred to as a fifth season, where AQI regularly exceeds 500 (Hazardous).
- **Sindh Heat and Dust**: Cities like Jacobabad (one of the hottest places on Earth) experience elevated PM levels during the summer months due to extreme heat and arid conditions.
- **COVID-19 Lockdowns (2020)**: Modeled pollution reduction during Mar--Jun 2020.
- **Long-term Trends**: A gradual worsening trend up to 2020 due to rapid urbanization, followed by a very slight stabilizing trend post-2021 due to new environmental initiatives (e.g., Ten Billion Tree Tsunami).

---

## Suggested Use Cases

1. **Smog Season Analysis** -- Isolate the Nov--Feb data in Punjab to study the severity and characteristics of the extreme winter smog.
2. **Public Health Correlation** -- Use the severe AQI data alongside demographic information to model health impacts in high-density areas like Lahore and Karachi.
3. **Cross-Country Analysis** -- Compare the Pakistan dataset with India (specifically Indian Punjab vs. Pakistani Punjab) in the `world_AQI` collection to study the transboundary nature of the Indo-Gangetic Plain smog.
4. **Time Series Forecasting** -- Predict hazardous AQI events to aid in the development of early warning systems.
5. **Sindh vs Punjab Comparison** -- Compare the industrial smog-driven pollution in Punjab against the heat/dust-driven pollution in Sindh.

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
Pakistan Air Quality Index Dataset (2014-2025)
6 Provinces/Territories | 69 Cities | Monthly Observations (Jan 2014 -- Dec 2025)
Data modeled on published statistics from IQAir, Pakistan Bureau of Statistics,
AQLI, and the Ministry of Climate Change.
```

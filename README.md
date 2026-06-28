# Women in the Global Labour Market

**Final project — Data Scientist (Python Developer for Data)**  
Syntra PXL Genk | 2024–2025

An interactive Streamlit dashboard that analyses gender equality 
in the global labour market between 1990 and 2025, based on data 
from the International Labour Organization (ILO) via Our World in Data.

## Research Question

> To what extent does gender equality exist in the global labour market,
> how has this evolved since 1990, and what role does a country's 
> economic prosperity play in this?

## Features

- Global trend analysis of female labour force participation (1990–2025)
- Regional comparison across 6 world regions
- Top 10 highest and lowest countries per year
- Relationship between GDP per capita and gender equality
- Male vs. female unemployment gap per region and country
- Interactive filters: by year, country and region
- Data stored in a normalized MySQL database (star schema)

## Tech Stack

- Python 3.x
- Streamlit
- Plotly Express
- Pandas
- MySQL + SQLAlchemy
- JSON / CSV

## Project Structure

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit application |
| `analysis.py` | Data analysis functions (11 analyses) |
| `charts.py` | Plotly chart functions (11 charts) |
| `data_loader.py` | Data loading and merging (CSV + MySQL) |
| `database.py` | Database setup and normalization |
| `merge.py` | Quick merge check script |
| `config_voorbeeld.py` | Example config file |
| `config.toml` | Streamlit theme settings |
| `csv/` | Raw CSV data files |

## Getting Started

1. Copy `config_voorbeeld.py` to `config.py` and fill in your MySQL credentials
2. Create an empty MySQL database:
```sql
   CREATE DATABASE female_labor_force;
```
3. Run `database.py` once to load the data into MySQL:
```
   python database.py
```
4. Start the Streamlit app:
```
   streamlit run app.py
```

## Dataset & Limitations

The datasets used in this project were sourced from the 
**International Labour Organization (ILO)** via 
[Our World in Data](https://ourworlddata.org) and cover 
186 countries across 6 world regions between 1990 and 2025.

> **Note:** Due to the scope and timeframe of this project, 
> the datasets are not exhaustive. GDP data is only available 
> up to 2024 (World Bank publishes with a delay). Some countries 
> have incomplete time series, particularly conflict-affected regions 
> (Ukraine, Sudan, South Sudan, Palestine, Lebanon), which are flagged 
> but not excluded from the analysis. Regional averages are unweighted 
> — each country counts equally regardless of population size.
> These limitations were taken into account throughout the analysis.

## Data Sources

- ILO — Female Labour Force Participation Rate
- ILO — Female-to-Male Labour Force Participation Ratio
- ILO — Unemployment Rate by Gender
- World Bank — GDP per capita
- All datasets accessed via [Our World in Data](https://ourworlddata.org)

## Author

Isabelle Reynders  
[LinkedIn](https://www.linkedin.com/in/isabelle-reynders)
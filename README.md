# Kenya Retail Analytics

An analytics portfolio project: a synthetic Kenyan supermarket dataset
modelled as a star schema in Snowflake with dbt, reported in Power BI.

> All data is synthetic. Names, prices, volumes and patterns are invented.

## Architecture

generator -> data/raw/*.csv -> Python ingestion -> Snowflake RAW
          -> dbt (staging -> marts) -> Power BI

## Status

- [x] Synthetic data generator
- [x] Python ingestion (setup, load, validate)
- [ ] Data profiling and notes
- [ ] Business questions and data dictionary
- [ ] Star schema design
- [ ] dbt models and tests
- [ ] Power BI report

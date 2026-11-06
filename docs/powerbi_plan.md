# Power BI plan

## 1. Connect (Power BI Desktop, Windows)

Get data > Snowflake
- Server: livxecg-ve59841.snowflakecomputing.com
- Warehouse: BI_WH
- Advanced options > Role name: BI_READER
- Mode: Import (the data is small, and BI_WH sleeps between refreshes)
- Sign in: Database credentials > user POWERBI_USER and its password

Database KENYA_RETAIL > schema ANALYTICS_MARTS > tick all 8 tables:
dim_customer, dim_date, dim_product, dim_store,
fact_deliveries, fact_payments, fact_reviews, fact_sales

## 2. Relationships (Model view)

All many-to-one, single direction (the dimension filters the fact).

| From (fact) | To (dimension) |
|---|---|
| fact_sales[date_key] | dim_date[date_key] |
| fact_sales[customer_key] | dim_customer[customer_key] |
| fact_sales[product_key] | dim_product[product_key] |
| fact_sales[store_key] | dim_store[store_key] |
| fact_payments[date_key] | dim_date[date_key] |
| fact_payments[customer_key] | dim_customer[customer_key] |
| fact_payments[store_key] | dim_store[store_key] |
| fact_deliveries[promised_date_key] | dim_date[date_key] (ACTIVE) |
| fact_deliveries[order_date_key] | dim_date[date_key] (inactive) |
| fact_deliveries[delivered_date_key] | dim_date[date_key] (inactive) |
| fact_deliveries[customer_key] | dim_customer[customer_key] |
| fact_deliveries[store_key] | dim_store[store_key] |
| fact_reviews[date_key] | dim_date[date_key] |
| fact_reviews[customer_key] | dim_customer[customer_key] |
| fact_reviews[store_key] | dim_store[store_key] |

One extra relationship, one-to-one, so lateness can filter reviews:
fact_deliveries[order_id] <-> fact_reviews[order_id]

After the relationships:
- Mark dim_date as the date table (column full_date).
- Sort dim_date[month_name] by month_number.
- Hide every *_key column, order_item_id, payment_id and review_id in Report view.

## 3. Measures (create a table called Measures)

Revenue = CALCULATE(SUM(fact_sales[net_revenue]), fact_sales[counts_as_sale] = TRUE())
Orders = CALCULATE(DISTINCTCOUNT(fact_sales[order_id]), fact_sales[counts_as_sale] = TRUE())
Units Sold = CALCULATE(SUM(fact_sales[quantity]), fact_sales[counts_as_sale] = TRUE())
Avg Order Value = DIVIDE([Revenue], [Orders])
Estimated Cost = CALCULATE(SUM(fact_sales[estimated_cost]), fact_sales[counts_as_sale] = TRUE())
Gross Profit = [Revenue] - [Estimated Cost]
Gross Margin % = DIVIDE([Gross Profit], [Revenue])
Revenue Previous Month = CALCULATE([Revenue], DATEADD(dim_date[full_date], -1, MONTH))
Revenue MoM % = DIVIDE([Revenue] - [Revenue Previous Month], [Revenue Previous Month])

Collected = CALCULATE(SUM(fact_payments[amount]), fact_payments[is_successful] = TRUE())
Failed Attempts = CALCULATE(COUNTROWS(fact_payments), fact_payments[status] = "failed")

Deliveries = COUNTROWS(fact_deliveries)
Late Deliveries = CALCULATE(COUNTROWS(fact_deliveries), fact_deliveries[is_late] = TRUE())
Known Delivery Times = CALCULATE(COUNTROWS(fact_deliveries), fact_deliveries[has_delivery_time] = TRUE())
Late Rate = DIVIDE([Late Deliveries], [Known Delivery Times])
Deliveries By Delivered Date = CALCULATE(COUNTROWS(fact_deliveries), USERELATIONSHIP(fact_deliveries[delivered_date_key], dim_date[date_key]))

Reviews = COUNTROWS(fact_reviews)
Avg Review Score = AVERAGE(fact_reviews[score])

Calculated column on fact_deliveries:
Lateness Band = SWITCH(TRUE(),
    ISBLANK(fact_deliveries[days_late]), "Unknown",
    fact_deliveries[days_late] <= 0, "1 On time or early",
    fact_deliveries[days_late] <= 2, "2 Late 1-2 days",
    "3 Late 3+ days")

## 4. Numbers to match (from the SQL checks)

| Measure | Expected |
|---|---|
| Revenue (no filters) | 82,626,488 |
| Orders | 49,581 |
| Collected | 83,027,075 |
| Late Rate by carrier | C 70.0%, B 30.5%, A 29.2% |
| Avg Review Score (no filters) | 3.89 |
| Avg score by Lateness Band | 4.28 / 3.50 / 2.21 |

Do not build any page until these match.

## 5. Report pages

1. Sales: cards (Revenue, Orders, Avg Order Value, Gross Margin %),
   line chart Revenue by dim_date[year_month], bar Revenue by category_name,
   bar Revenue by dim_store[county], slicers for year and channel.
2. Payments and customers: bar Collected by method, line Collected by month,
   card Failed Attempts, bar Revenue by dim_customer[segment]
   (the "Unknown" segment is the walk-in shoppers).
3. Delivery and satisfaction: bar Late Rate by carrier,
   bar Avg Review Score by Lateness Band, card Avg Review Score,
   bar Avg Review Score by store county, text box with 3 findings.

## 6. Session checklist

- Sign in with POWERBI_USER only. Never use the admin login on a borrowed PC.
- Save the .pbix to a USB stick or a cloud drive, then sign out of everything.
- Screenshot each page for the README.
- Afterwards: reset or drop POWERBI_USER from your own machine.

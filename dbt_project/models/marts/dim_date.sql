with days as (

    select
        dateadd(
            day,
            row_number() over (order by seq4()) - 1,
            '2022-01-01'::date
        ) as date_day
    from table(generator(rowcount => 1826))

)

select
    to_number(to_char(date_day, 'YYYYMMDD'))   as date_key,
    date_day                                   as full_date,
    year(date_day)                             as year,
    quarter(date_day)                          as quarter,
    month(date_day)                            as month_number,
    monthname(date_day)                        as month_name,
    to_char(date_day, 'YYYY-MM')               as year_month,
    date_trunc('month', date_day)::date        as month_start,
    day(date_day)                              as day_of_month,
    dayofweekiso(date_day)                     as day_of_week_number,
    dayname(date_day)                          as day_name,
    dayofweekiso(date_day) in (6, 7)           as is_weekend
from days

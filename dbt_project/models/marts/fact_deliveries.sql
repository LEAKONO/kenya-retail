with deliveries as (

    select * from {{ ref('stg_deliveries') }}

),

orders as (

    select
        order_id,
        customer_id,
        store_id,
        order_ts,
        order_ts::date as order_date
    from {{ ref('stg_orders') }}

),

customers as (

    select customer_key, customer_id, valid_from, valid_to
    from {{ ref('dim_customer') }}

),

joined as (

    select
        deliveries.delivery_id,
        deliveries.order_id,
        deliveries.carrier,
        deliveries.delivery_county,
        deliveries.promised_date,
        deliveries.delivered_ts,
        coalesce(orders.customer_id, 'WALK-IN')   as customer_id,
        orders.store_id,
        orders.order_ts,
        orders.order_date
    from deliveries
    join orders
        on deliveries.order_id = orders.order_id

),

with_customer as (

    select
        joined.*,
        customers.customer_key
    from joined
    left join customers
        on  joined.customer_id = customers.customer_id
        and joined.order_date >= customers.valid_from
        and (joined.order_date < customers.valid_to or customers.valid_to is null)

)

select
    delivery_id,
    order_id,
    to_number(to_char(order_date, 'YYYYMMDD'))              as order_date_key,
    to_number(to_char(promised_date, 'YYYYMMDD'))           as promised_date_key,
    to_number(to_char(delivered_ts::date, 'YYYYMMDD'))      as delivered_date_key,
    customer_key,
    md5(cast(store_id as varchar))                          as store_key,
    carrier,
    delivery_county,
    (delivered_ts is not null)                              as has_delivery_time,
    datediff('day', promised_date, delivered_ts::date)      as days_late,
    (datediff('day', promised_date, delivered_ts::date) > 0) as is_late,
    datediff('hour', order_ts, delivered_ts)                as hours_to_deliver
from with_customer

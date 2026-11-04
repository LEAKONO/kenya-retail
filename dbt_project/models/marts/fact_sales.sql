with order_items as (

    select * from {{ ref('stg_order_items') }}

),

orders as (

    select * from {{ ref('stg_orders') }}

),

products as (

    select product_id, unit_cost
    from {{ ref('dim_product') }}

),

customers as (

    select customer_key, customer_id, valid_from, valid_to
    from {{ ref('dim_customer') }}

),

joined as (

    select
        order_items.order_item_id,
        order_items.order_id,
        orders.order_ts::date                       as order_date,
        coalesce(orders.customer_id, 'WALK-IN')     as customer_id,
        order_items.product_id,
        orders.store_id,
        orders.channel,
        orders.status                               as order_status,
        order_items.quantity,
        order_items.unit_price,
        order_items.discount_amount,
        products.unit_cost
    from order_items
    join orders
        on order_items.order_id = orders.order_id
    left join products
        on order_items.product_id = products.product_id

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
    order_item_id,
    order_id,
    to_number(to_char(order_date, 'YYYYMMDD'))        as date_key,
    customer_key,
    md5(cast(product_id as varchar))                  as product_key,
    md5(cast(store_id as varchar))                    as store_key,
    channel,
    order_status,
    (order_status in ('completed', 'delivered'))      as counts_as_sale,
    quantity,
    unit_price,
    discount_amount,
    quantity * unit_price                             as gross_amount,
    quantity * unit_price - discount_amount           as net_revenue,
    quantity * unit_cost                              as estimated_cost
from with_customer

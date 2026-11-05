with reviews as (

    select * from {{ ref('stg_reviews') }}

),

orders as (

    select
        order_id,
        customer_id,
        store_id,
        order_ts::date as order_date
    from {{ ref('stg_orders') }}

),

customers as (

    select customer_key, customer_id, valid_from, valid_to
    from {{ ref('dim_customer') }}

),

joined as (

    select
        reviews.review_id,
        reviews.order_id,
        reviews.score,
        reviews.created_at::date                    as review_date,
        coalesce(orders.customer_id, 'WALK-IN')     as customer_id,
        orders.store_id,
        orders.order_date
    from reviews
    join orders
        on reviews.order_id = orders.order_id

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
    review_id,
    order_id,
    to_number(to_char(review_date, 'YYYYMMDD'))     as date_key,
    customer_key,
    md5(cast(store_id as varchar))                  as store_key,
    score
from with_customer

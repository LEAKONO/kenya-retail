with payments as (

    select * from {{ ref('stg_payments') }}

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
        payments.payment_id,
        payments.order_id,
        payments.payment_ts::date                   as payment_date,
        coalesce(orders.customer_id, 'WALK-IN')     as customer_id,
        orders.store_id,
        orders.order_date,
        payments.method,
        payments.status,
        payments.amount,
        payments.mpesa_ref
    from payments
    join orders
        on payments.order_id = orders.order_id

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
    payment_id,
    order_id,
    to_number(to_char(payment_date, 'YYYYMMDD'))    as date_key,
    customer_key,
    md5(cast(store_id as varchar))                  as store_key,
    method,
    status,
    (status = 'success')                            as is_successful,
    amount,
    mpesa_ref
from with_customer

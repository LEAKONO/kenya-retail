with source as (

    select * from {{ source('raw', 'orders') }}

),

renamed as (

    select
        "order_id"                as order_id,
        "customer_id"             as customer_id,
        "store_id"                as store_id,
        "order_ts"                as order_ts,
        lower(trim("channel"))    as channel,
        lower(trim("status"))     as status,
        "updated_at"              as updated_at
    from source

)

select * from renamed

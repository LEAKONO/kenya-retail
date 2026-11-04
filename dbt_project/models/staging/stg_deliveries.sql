with source as (

    select * from {{ source('raw', 'deliveries') }}

),

renamed as (

    select
        "delivery_id"                      as delivery_id,
        "order_id"                         as order_id,
        trim("carrier")                    as carrier,
        "promised_date"                    as promised_date,
        "delivered_ts"                     as delivered_ts,
        initcap(trim("delivery_county"))   as delivery_county
    from source

)

select * from renamed

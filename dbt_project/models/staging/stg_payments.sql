with source as (

    select * from {{ source('raw', 'payments') }}

),

renamed as (

    select
        "payment_id"                as payment_id,
        "order_id"                  as order_id,
        "payment_ts"                as payment_ts,
        lower(trim("method"))       as method,
        "amount"                    as amount,
        upper(trim("currency"))     as currency,
        lower(trim("status"))       as status,
        trim("mpesa_ref")           as mpesa_ref
    from source

)

select * from renamed

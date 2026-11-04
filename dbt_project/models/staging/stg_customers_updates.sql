with source as (

    select * from {{ source('raw', 'customers_updates') }}

),

renamed as (

    select
        "customer_id"                       as customer_id,
        trim("full_name")                   as full_name,
        lpad("phone"::varchar, 10, '0')     as phone,
        initcap(trim("county"))             as county,
        trim("segment")                     as segment,
        "signup_date"                       as signup_date,
        "updated_at"                        as updated_at
    from source

)

select * from renamed

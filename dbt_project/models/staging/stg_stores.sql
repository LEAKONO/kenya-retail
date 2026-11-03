with source as (

    select * from {{ source('raw', 'stores') }}

),

renamed as (

    select
        "store_id"                   as store_id,
        trim("store_name")           as store_name,
        initcap(trim("county"))      as county,
        trim("store_format")         as store_format,
        "opened_date"                as opened_date
    from source

)

select * from renamed

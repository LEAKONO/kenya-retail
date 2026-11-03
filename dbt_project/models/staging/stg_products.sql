with source as (

    select * from {{ source('raw', 'products') }}

),

renamed as (

    select
        "product_id"                as product_id,
        trim("product_name")        as product_name,
        "category_id"               as category_id,
        initcap(trim("brand"))      as brand,
        "unit_cost"                 as unit_cost,
        "list_price"                as list_price,
        "is_active"                 as is_active,
        "updated_at"                as updated_at
    from source

)

select * from renamed

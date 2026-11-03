with source as (

    select * from {{ source('raw', 'order_items') }}

),

deduplicated as (

    select *
    from source
    qualify row_number() over (
        partition by "order_item_id"
        order by "order_item_id"
    ) = 1

),

renamed as (

    select
        "order_item_id"                  as order_item_id,
        "order_id"                       as order_id,
        "product_id"                     as product_id,
        "quantity"                       as quantity,
        "unit_price"                     as unit_price,
        coalesce("discount_amount", 0)   as discount_amount
    from deduplicated

)

select * from renamed

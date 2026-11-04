with products as (

    select * from {{ ref('stg_products') }}

),

categories as (

    select * from {{ ref('stg_categories') }}

),

joined as (

    select
        md5(cast(products.product_id as varchar))   as product_key,
        products.product_id,
        products.product_name,
        products.brand,
        products.category_id,
        categories.category_name,
        products.unit_cost,
        products.list_price,
        products.is_active
    from products
    left join categories
        on products.category_id = categories.category_id

)

select * from joined

with source as (

    select * from {{ source('raw', 'categories') }}

),

renamed as (

    select
        "category_id"            as category_id,
        trim("category_name")    as category_name
    from source

)

select * from renamed

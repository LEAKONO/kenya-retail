with source as (

    select * from {{ source('raw', 'reviews') }}

),

renamed as (

    select
        "review_id"     as review_id,
        "order_id"      as order_id,
        "score"         as score,
        "created_at"    as created_at
    from source

)

select * from renamed

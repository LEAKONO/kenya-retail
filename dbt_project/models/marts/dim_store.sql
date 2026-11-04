with stores as (

    select * from {{ ref('stg_stores') }}

)

select
    md5(cast(store_id as varchar))   as store_key,
    store_id,
    store_name,
    county,
    store_format,
    opened_date
from stores

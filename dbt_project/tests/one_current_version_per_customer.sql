select
    customer_id,
    count_if(is_current) as current_versions
from {{ ref('dim_customer') }}
group by customer_id
having count_if(is_current) <> 1

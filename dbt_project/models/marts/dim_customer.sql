with customers as (

    select * from {{ ref('stg_customers') }}

),

updates as (

    select * from {{ ref('stg_customers_updates') }}

),

person_map as (

    select
        customer_id,
        coalesce(
            case
                when phone is not null
                then min(customer_id) over (partition by full_name, phone)
            end,
            customer_id
        ) as person_id
    from customers

),

all_versions as (

    select
        customer_id, full_name, phone, county, segment,
        signup_date as valid_from
    from customers

    union all

    select
        customer_id, full_name, phone, county, segment,
        updated_at as valid_from
    from updates

),

versions as (

    select
        *,
        lead(valid_from) over (
            partition by customer_id
            order by valid_from
        ) as valid_to
    from all_versions

),

walk_in as (

    select
        'WALK-IN'            as customer_id,
        'Walk-in customer'   as full_name,
        null::varchar        as phone,
        'Unknown'            as county,
        'Unknown'            as segment,
        '1900-01-01'::date   as valid_from,
        null::date           as valid_to

),

combined as (

    select
        versions.customer_id,
        person_map.person_id,
        versions.full_name,
        versions.phone,
        versions.county,
        versions.segment,
        versions.valid_from,
        versions.valid_to
    from versions
    join person_map
        on versions.customer_id = person_map.customer_id

    union all

    select
        customer_id,
        'WALK-IN' as person_id,
        full_name,
        phone,
        county,
        segment,
        valid_from,
        valid_to
    from walk_in

)

select * from combined

-- minimal dbt model selecting orders
select * from {{ ref('raw_orders') }}

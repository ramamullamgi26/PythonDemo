-- minimal dbt model selecting users
select * from {{ ref('raw_users') }}

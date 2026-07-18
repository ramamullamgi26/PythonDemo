Feature: Orders table data quality
  Validate the `orders` table for schema, referential integrity, ranges and business rules.

  Scenario: Orders table has expected columns
    Given the database is available
    When I inspect the `orders` table schema
    Then the table should contain columns `order_id`, `user_id`, `amount`, `order_date`, `status`

  Scenario: Order amounts are positive and within expected range
    Given the `orders` table is loaded
    Then all values in column `amount` should be greater than 0
    And all values in column `amount` should be less than 100000

  Scenario: Referential integrity with users
    Given the `orders` table is loaded
    Then every `user_id` in `orders` must exist in `users`

  Scenario: Order status values are within allowed set
    Given the `orders` table is loaded
    Then all `status` values should be one of `completed`, `shipped`, `cancelled`, `pending`

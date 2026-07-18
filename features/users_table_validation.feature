Feature: Users table data quality
  Validate the `users` table for schema, uniqueness, nulls and business rules.

  Scenario: Users table has expected columns
    Given the database is available
    When I inspect the `users` table schema
    Then the table should contain columns `user_id`, `email`, `name`, `signup_date`

  Scenario: Emails are not null and unique
    Given the `users` table is loaded
    Then no values in column `email` should be null
    And values in column `email` should be unique

  Scenario: Signup dates are reasonable
    Given the `users` table is loaded
    Then all `signup_date` values should be parseable as dates
    And no `signup_date` should be in the future

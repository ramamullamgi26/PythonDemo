from behave import given, when, then
from utils.db_connection import get_connection
import pandas as pd
from datetime import datetime, date
import great_expectations as ge


@given('the database is available')
def step_db_available(context):
    conn = get_connection()
    conn.close()
    context.db_ok = True


@given('the `{table}` table is loaded')
def step_table_loaded(context, table):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    context.table = table
    context.df = df


@when('I inspect the `{table}` table schema')
def step_inspect_schema(context, table):
    conn = get_connection()
    cur = conn.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cur.fetchall()]
    conn.close()
    context.columns = cols


@then('the table should contain columns `{cols}`')
def step_table_columns(context, cols):
    expected = [c.strip() for c in cols.split(',')]
    missing = [c for c in expected if c not in context.columns]
    assert not missing, f"Missing columns: {missing}"


@then('no values in column `{col}` should be null')
def step_no_nulls(context, col):
    assert context.df[col].notna().all(), f"Null values found in {col}"


@then('values in column `{col}` should be unique')
def step_unique(context, col):
    assert context.df[col].is_unique, f"Duplicate values found in {col}"


@then('all `{col}` values should be parseable as dates')
def step_parseable_dates(context, col):
    def parse(x):
        try:
            datetime.fromisoformat(x)
            return True
        except Exception:
            return False
    assert context.df[col].apply(lambda x: parse(x)).all(), f"Unparseable dates in {col}"


@then('no `{col}` should be in the future')
def step_not_in_future(context, col):
    today = date.today()
    parsed = context.df[col].apply(lambda x: datetime.fromisoformat(x).date())
    assert (parsed <= today).all(), f"Date in future found in {col}"


@then('all values in column `{col}` should be greater than {val:d}')
def step_greater_than(context, col, val):
    assert (context.df[col] > val).all(), f"Values <= {val} found in {col}"


@then('all values in column `{col}` should be less than {val:d}')
def step_less_than(context, col, val):
    assert (context.df[col] < val).all(), f"Values >= {val} found in {col}"


@then('every `{col}` in `{table2}` must exist in `users`')
def step_ref_integrity(context, col, table2):
    conn = get_connection()
    df2 = pd.read_sql_query(f"SELECT {col} FROM {table2}", conn)
    df_users = pd.read_sql_query("SELECT user_id FROM users", conn)
    conn.close()
    missing = set(df2[col]) - set(df_users['user_id'])
    assert not missing, f"Referential integrity failed, missing users: {missing}"


@then('all `status` values should be one of `completed`, `shipped`, `cancelled`, `pending`')
def step_status_values(context):
    allowed = {'completed', 'shipped', 'cancelled', 'pending'}
    vals = set(context.df['status'].astype(str).str.lower())
    bad = vals - allowed
    assert not bad, f"Invalid status values: {bad}"

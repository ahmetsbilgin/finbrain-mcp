from finbrain_mcp.utils import limit_slice, rows_to_csv, df_to_records_maybe


def test_limit_slice_basic():
    rows = list(range(10))
    assert limit_slice(rows, 0, 3) == [0, 1, 2]
    assert limit_slice(rows, 5, 10) == [5, 6, 7, 8, 9]
    assert limit_slice(rows, -5, 2) == [0, 1]
    assert limit_slice(rows, 3, 0) == []


def test_rows_to_csv():
    rows = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    csv_text = rows_to_csv(rows)
    assert "a,b" in csv_text.splitlines()[0]
    assert "1,2" in csv_text
    assert "3,4" in csv_text


def test_df_to_records_maybe_without_pandas():
    # If pandas isn't installed, function should pass object through unchanged.
    obj = [{"x": 1}]
    assert df_to_records_maybe(obj) is obj

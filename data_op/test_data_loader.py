import pytest
import pandas as pd
import json
from data_loader import Reader

sample_data = [
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Jane Doe"},
    {"id": 3, "name": "June Eoe"},
    {"id": 3, "name": "Moon Sun"},
]

@pytest.fixture(scope="module")
def sample_jsonl_file(tmp_path_factory):
    data_file = tmp_path_factory.mktemp("data") / "sample.jsonl"
    with open(data_file, "w") as f:
        for item in sample_data:
            f.write(json.dumps(item) + "\n")
    return str(data_file)

def test_load_data(sample_jsonl_file):
    reader = Reader(sample_jsonl_file, batch_size=2)
    chunks = reader.load_data()
    for chunk in chunks:
        assert isinstance(chunk, pd.DataFrame)
        assert not chunk.empty

def test_concatenate_chunks(sample_jsonl_file):
    reader = Reader(sample_jsonl_file, batch_size=2)
    df = reader.concatenate_chunks()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(sample_data)
    assert all(df.columns == ["id", "name"])
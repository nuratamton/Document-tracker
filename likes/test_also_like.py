import pytest
import numpy as np
import pandas as pd
from also_like import AlsoLike
# hand crafted dataset - work of art
data = [
    {"visitor_uuid": "04daa9ed9dde73d3", "env_doc_id": "doc1"},
    {"visitor_uuid": "04daa9ed9dde73d3", "env_doc_id": "doc2"},
    {"visitor_uuid": "ade7e1f63bc83c66", "env_doc_id": "doc1"},
    {"visitor_uuid": "ade7e1f63bc83c66", "env_doc_id": "doc3"},
    {"visitor_uuid": "user3", "env_doc_id": "doc2"},
    {"visitor_uuid": "user3", "env_doc_id": "doc3"},
    {"visitor_uuid": "user4", "env_doc_id": "doc3"},
    {"visitor_uuid": "user4", "env_doc_id": "doc4"},
    {"visitor_uuid": "user5", "env_doc_id": "doc1"},
    {"visitor_uuid": "user5", "env_doc_id": "doc4"},
    {"visitor_uuid": "user6", "env_doc_id": "doc2"},
    {"visitor_uuid": "user7", "env_doc_id": "doc2"},
    {"visitor_uuid": "user7", "env_doc_id": "doc5"},
    {"visitor_uuid": "user8", "env_doc_id": "doc5"},
    {"visitor_uuid": "user9", "env_doc_id": "doc1"},
    {"visitor_uuid": "user9", "env_doc_id": "doc6"},
    {"visitor_uuid": "user10", "env_doc_id": "doc6"}
]
df = pd.DataFrame(data)

@pytest.fixture(scope="module")
def al_instance():
    return AlsoLike(df)
# function to test the get_visitor_uuid function
def test_get_collection_of_visitors_from_doc(al_instance):
    reader = al_instance
    assert reader.get_visitor_uuid("doc1") == {'user9', '04daa9ed9dde73d3', 'user5', 'ade7e1f63bc83c66'}
# function to test the get_document_uuid function
def test_get_collection_of_doc_from_visitor_uuid(al_instance):
    reader = al_instance
    assert reader.get_document_uuid("user3") == {'doc2', 'doc3'}
# function to test also_like function
def test_also_like(al_instance):
    reader = al_instance
    expected_result = np.array(['doc2', 'doc3', 'doc4', 'doc6'])
    actual_result = reader.get_also_like("doc1")
    assert np.array_equal(actual_result, expected_result)





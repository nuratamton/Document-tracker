import pytest
import pandas as pd
from also_like import AlsoLike

data = [
    {"visitor_uuid": "04daa9ed9dde73d3", "subject_doc_id": "doc1"},
    {"visitor_uuid": "04daa9ed9dde73d3", "subject_doc_id": "doc2"},
    {"visitor_uuid": "ade7e1f63bc83c66", "subject_doc_id": "doc1"},
    {"visitor_uuid": "ade7e1f63bc83c66", "subject_doc_id": "doc3"},
    {"visitor_uuid": "user3", "subject_doc_id": "doc2"},
    {"visitor_uuid": "user3", "subject_doc_id": "doc3"},
    {"visitor_uuid": "user4", "subject_doc_id": "doc3"},
    {"visitor_uuid": "user4", "subject_doc_id": "doc4"},
    {"visitor_uuid": "user5", "subject_doc_id": "doc1"},
    {"visitor_uuid": "user5", "subject_doc_id": "doc4"},
    {"visitor_uuid": "user6", "subject_doc_id": "doc2"},
    {"visitor_uuid": "user7", "subject_doc_id": "doc2"},
    {"visitor_uuid": "user7", "subject_doc_id": "doc5"},
    {"visitor_uuid": "user8", "subject_doc_id": "doc5"},
    {"visitor_uuid": "user9", "subject_doc_id": "doc1"},
    {"visitor_uuid": "user9", "subject_doc_id": "doc6"},
    {"visitor_uuid": "user10", "subject_doc_id": "doc6"}
]
df = pd.DataFrame(data)

@pytest.fixture(scope="module")
def al_instance():
    return AlsoLike()

def test_get_collection_of_visitors_from_doc(al_instance):
    reader = al_instance.AlsoLike(df)
    assert reader.get_visitor_uuid("doc1") == []

def 

import sys
sys.path.insert(0, '/home/aisummer/mikhail_workspace/nlp-service')
from src.evaluation_metrics import RetrievalMetrics

import pytest


@pytest.fixture
def metrics_class():
    return RetrievalMetrics()
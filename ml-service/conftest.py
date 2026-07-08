import pytest


@pytest.fixture(autouse=True)
def setup_recommender():
    from app.api.routes import initialize_with_sample_data
    initialize_with_sample_data()
    yield
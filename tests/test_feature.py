import os

from src.content_manager.client import experiment_feature


def test_retrieve_fake_env_var():
    value = os.getenv("FAKE_SEC")

    assert value

def test_retrieve_os_variable():
    value = os.environ["GOOGLE_API_KEY"]
    assert value

def test_if_it_works():
    api_key = os.environ["GOOGLE_API_KEY"]
    
    response = experiment_feature(api_key)

    assert response

    print(response.text)
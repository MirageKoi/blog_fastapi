import os

from src.content_manager.client import experiment_feature




def test_if_it_works():
    api_key = os.environ["GOOGLE_API_KEY"]
    if api_key:
        print("TRUEEEEEE")

    response = experiment_feature(api_key)

    assert response

    print(response.text)
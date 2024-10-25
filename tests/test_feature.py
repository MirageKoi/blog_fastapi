from src.content_manager.client import experiment_feature




def test_if_it_works():

    response = experiment_feature()

    assert response

    print(response.text)
from urllib.parse import quote
import requests


def get_score(service, test_data):
    actor_user_id = test_data["actor_user_id"]
    receiver_user_id = test_data["receiver_user_id"]
    model_id = test_data["model_id"]
    actor_features = test_data["actor_features"]
    receiver_features = test_data["receiver_features"]
    real_time_features = "" if "real_time_features" not in test_data else test_data["real_time_features"]

    test_data["actor_features"] = actor_features
    test_data["receiver_features"] = receiver_features
    test_data["real_time_features"] = real_time_features

    url = "http://%s:8008/test/scorePlayer?actorId=%d&receiverId=%d&modelId=%s&isDebugging=true&actorFeature=%s&receiverFeature=%s&realTimeFeature=%s" % (
        service, actor_user_id, receiver_user_id, model_id, quote(actor_features), quote(receiver_features), quote(real_time_features)
    )
    return requests.get(url)

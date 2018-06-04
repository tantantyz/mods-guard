from urllib.parse import quote
import json
import requests

indices = {
    "actor_popularity": "41001",
    "receiver_popularity": "41001",
    "distance": "41005",
    "receiver_minutes_swiped_minus_last_active": "41004"
}


def wrapper_features(feat):
    segs = feat.split("##fVec##")
    if len(segs) == 2:
        return segs[0] + "##fVec##" + segs[1].replace("#", "|").replace("51001|", "51001#").replace("51002|", "51002#")
    else:
        return feat


def merge_real_time_features(actor_features, receiver_features, real_time_features):
    if real_time_features != "" and real_time_features[0] == "{":
        real_time_features = json.loads(real_time_features)
    else:
        return actor_features, receiver_features, real_time_features
    if "##fFloat##" in actor_features:
        pos = actor_features.index("##fFloat##")
        actor_features = actor_features[:pos] + "##fFloat##" + indices["actor_popularity"] + "#" + str(real_time_features["actor_popularity"]) + "," + actor_features[pos + 10:]
    else:
        actor_features = actor_features + "##fFloat##" + indices["actor_popularity"] + "#" + str(real_time_features["actor_popularity"])
    if "##fFloat##" in receiver_features:
        pos = receiver_features.index("##fFloat##")
        receiver_features = receiver_features[:pos] + "##fFloat##" + \
                            indices["receiver_popularity"] + "#" + str(real_time_features["receiver_popularity"]) + "," + \
                            indices["distance"] + "#" + str(real_time_features["distance"]) + "," + \
                            indices["receiver_minutes_swiped_minus_last_active"] + "#" + str(real_time_features["receiver_minutes_swiped_minus_last_active"] * 60) + "," + \
                            receiver_features[pos + 10:]
    else:
        receiver_features = receiver_features + "##fFloat##" + \
                            indices["receiver_popularity"] + "#" + str(real_time_features["receiver_popularity"]) + "," + \
                            indices["distance"] + "#" + str(real_time_features["distance"]) + "," + \
                            indices["receiver_minutes_swiped_minus_last_active"] + "#" + str(real_time_features["receiver_minutes_swiped_minus_last_active"] * 60)
    real_time_features = ""

    return actor_features, receiver_features, real_time_features


def get_score(service, test_data):
    actor_user_id = test_data["actor_user_id"]
    receiver_user_id = test_data["receiver_user_id"]
    model_id = test_data["model_id"]
    actor_features = wrapper_features(test_data["actor_features"])
    receiver_features = wrapper_features(test_data["receiver_features"])
    real_time_features = test_data["real_time_features"]

    actor_features, receiver_features, real_time_features = merge_real_time_features(actor_features,
                                                                                     receiver_features,
                                                                                     real_time_features)
    test_data["actor_features"] = actor_features
    test_data["receiver_features"] = receiver_features
    test_data["real_time_features"] = real_time_features

    url = "http://%s:8008/test/scorePlayer?modelId=%s&actorFeature=%s&receiverFeature=%s&realTimeFeature=%s" % (
        service, model_id, quote(actor_features), quote(receiver_features), quote(real_time_features)
    )
    # print(url)
    return requests.get(url)

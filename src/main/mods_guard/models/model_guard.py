from urllib.parse import quote
import json
import requests

receiver_real_time_feature_indices = {
    "receiver_popularity": "41001",
    "distance": "41005",
    "receiver_minutes_swiped_minus_last_active": "41004"
}

actor_real_time_feature_indices = {
    "actor_popularity": "41001"
}


def wrapper_features(feat):
    segs = feat.split("##fVec##")
    if len(segs) == 2:
        return segs[0] + "##fVec##" + segs[1].replace("#", "|").replace("51001|", "51001#").replace("51002|", "51002#")
    else:
        return feat


def combine_real_time_features(features, indices, real_time_features):
    real_features = ",".join([indices[ele] + "#" + str(real_time_features[ele]) for ele in
                              filter(lambda x: x in real_time_features, indices)])
    if real_features != "":
        if "##fFloat##" in features:
            pos = features.index("##fFloat##")
            features = features[:pos] + "##fFloat##" + real_features + "," + features[pos + 10:]
        else:
            features = features + "##fFloat##" + real_features

    return features


def merge_real_time_features(actor_features, receiver_features, real_time_features):
    if real_time_features != "" and real_time_features[0] == "{":
        real_time_features = json.loads(real_time_features)
    else:
        return actor_features, receiver_features, real_time_features

    if "receiver_minutes_swiped_minus_last_active" in real_time_features:
        real_time_features["receiver_minutes_swiped_minus_last_active"] *= 60

    actor_features = combine_real_time_features(actor_features, actor_real_time_feature_indices, real_time_features)
    receiver_features = combine_real_time_features(receiver_features, receiver_real_time_feature_indices,
                                                   real_time_features)
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

'''
ssh -L 8008:10.189.100.35:8008  123.59.92.131 -CNfgqP
sudo ifconfig lo0 10.189.100.35 alias
echo "rdr pass on lo0 inet proto tcp from any to 10.189.100.43 port 8008 -> 127.0.0.1 port 8008" | sudo pfctl -ef -
'''


from urllib.parse import quote
import subprocess
from .model_guard import wrapper_features, merge_real_time_features

test_file = "check_hdfs_write_FEMALE_WEIGHTED_7_1_2018-04-08_2018-04-09_1_201805242330"

host = "http://10.189.100.35:8008/test/scorePlayer"

count = 0.0
correct_count = 0.0

with open(test_file, 'r') as fin:
    fin.readline()
    while 1:
        test = fin.readline()
        if not test:
            break
        segs = test.split("\t")
        actor_user_id = segs[0]
        receiver_user_id = segs[1]
        swiped_timestamp = segs[2]
        actor_swipe_status = segs[3]
        model_id = segs[4]
        actor_features = wrapper_features(segs[5])
        receiver_features = wrapper_features(segs[6])
        real_time_features = segs[7]
        score = segs[8]
        actor_features, receiver_features, real_time_features = merge_real_time_features(actor_features,
                                                                                         receiver_features,
                                                                                         real_time_features)

        url = "%s?modelId=%s&actorFeature=%s&receiverFeature=%s&realTimeFeature=%s" % (
            host, model_id, quote(actor_features), quote(receiver_features), quote(real_time_features)
        )

        a = subprocess.getoutput("curl -s '" + url + "'")
        print(actor_user_id, receiver_user_id, a, score, abs(float(a) - float(score)) < 1e-4)
        count += 1
        if abs(float(a) - float(score)) < 1e-4:
            correct_count += 1

print("true rate: " + str(correct_count / count))

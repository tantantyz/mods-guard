from flask import Flask, render_template, request, redirect
import json
from json.decoder import JSONDecodeError

from .models.model_guard import get_score

from .models.utils import random_pick_a_service

UPLOAD_FOLDER = "."

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def redirect_index():
    return redirect("/index")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/score_play", methods=['POST'])
def score_play():
    env = request.form['env']
    host = random_pick_a_service(env)
    items = list()
    if len(request.files) > 0:
        file = request.files['test_data_file']
        test_data = file.readlines()
    else:
        test_data_str = request.form['test_data_str']
        test_data = test_data_str.strip().split("\n")

    for data in test_data:
        if len(data.strip()) == 0:
            continue
        try:
            test = json.loads(data)
            r = get_score(host, test)
            resp = dict()
            resp["actor_user_id"] = test["actor_user_id"]
            resp["receiver_user_id"] = test["receiver_user_id"]
            resp["actor_features"] = test["actor_features"]
            resp["receiver_features"] = test["receiver_features"]
            resp["real_time_features"] = test["real_time_features"]

            if r.status_code == 200:
                resp["real_score"] = float(r.text)
            else:
                resp["real_score"] = -1.0
            items.append(resp)
        except JSONDecodeError as e:
            print(e)

    return render_template("results.html", items=items)

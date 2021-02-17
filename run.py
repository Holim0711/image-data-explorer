from flask import Flask
from flask import render_template
from flask import redirect, url_for
from flask import request
import os
import json
import random
import pandas

app = Flask(__name__)


def read_config():
    with open('config.json') as file:
        config = json.load(file)

    df = pandas.read_csv(config['data'])

    assert df.columns[0] == 'url'

    atts = df.columns[1:]

    vals = {
        att: df[att].unique()
        for att in atts
    }

    return df, atts, vals, config['url_root']


df, atts, vals, url_root = read_config()


@app.route('/')
def viewer():
    seed = request.args.get('seed', random.randint(0, 9999))
    random.seed(seed)

    args = {x: request.args.get(x) for x in atts}

    indices = random.sample(range(0, len(df)), 10)

    images = df.iloc[indices]['url']

    images = [os.path.join(url_root, x) for x in images]

    return render_template('viewer.html', seed=seed, images=images, args=args)

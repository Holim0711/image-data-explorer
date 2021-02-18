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


def try_parse(x):
    if isinstance(x, str):
        if x.isnumeric():
            return int(x)
    return x


def select_df(df, args):
    for att, val in args.items():
        if val is not None:
            df = df[df[att] == try_parse(val)]
    return df


@app.route('/')
def viewer():
    seed = request.args.get('seed')
    seed = int(seed) if seed else random.randint(0, 9999)
    random.seed(seed)

    args = {x: request.args.get(x) for x in atts}

    rows = select_df(df, args)

    args = {
        x: [(None, y is None)] + [(k, k == try_parse(y)) for k in vals[x]]
        for x, y in args.items()
    }

    indices = random.sample(range(0, len(rows)), min(50, len(rows)))

    images = rows.iloc[indices]['url']

    images = [os.path.join(url_root, x) for x in images]

    return render_template('viewer.html', seed=seed, images=images, args=args)


df, atts, vals, url_root = read_config()

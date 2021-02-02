from flask import Flask, request, render_template, make_response

import logging
import json
import uuid
from datetime import datetime

#import init_db

from db import db_session
from models import Sayings

app = Flask(__name__, template_folder='.')

logging.basicConfig(level=logging.NOTSET)

handler = logging.FileHandler('app.log', encoding='UTF-8')
logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

@app.errorhandler(Exception)
def error(e):
    app.logger.exception('%s', e)
    return render_template('index.html', saying=api_get()['sayings'], msg='发生了错误')

@app.route('/', methods=['GET', 'POST'])
def home():
    app.logger.info('%s, %s',request.method, request.form)
    uid = request.cookies.get('uid', str(uuid.uuid1()))
    if request.method == 'POST':
        print(request.form)
        saying = request.form['saying']
        if len(saying) > 0:
            h = {}
            for k,v in request.headers:
                h[k] = v
            s = Sayings(
                saying, 
                0, 
                json.dumps(h, ensure_ascii=False),
                uid
                )
            db_session.add(s)
    res = make_response(
        render_template('index.html', saying=api_get()['sayings'], msg='', uid=uid)
        )
    res.set_cookie('uid', uid)
    return res


@app.route('/api/get', methods=['GET'])
def api_get():
    try:
        sayings = Sayings.query.all()
    except:
        db_session.rollback()
        return api_get()
    return {
        'code': 200,
        'length': len(sayings),
        'sayings': [
            {
                'id': s.id,
                'saying': s.saying,
                'likes': s.likes,
                'info': json.loads(
                    s.info
                    if ('{' in s.info and '}' in s.info)
                    else '{}'
                    ),
                'time': s.datetime,
                'uid': s.uid
            }
            for s in sayings
        ]
    }


@app.route('/api/put', methods=['GET', 'PUT'])
def api_put():
    saying = ''
    if request.method == 'POST':
        saying = request.form['saying']
    elif request.method == 'GET':
        saying = request.args['saying']
    else:
        pass

    if len(saying) > 0:
        s = Sayings(saying, 0)
        db_session.add(s)
        #db_session.commit()

        return {
            'code': 200,
            'id': s.id,
            'saying': s.saying,
            'link': s.likes
        }

    else:
        return {
            'code': 400,
            'id': None,
            'saying': None,
            'link': None
        }


@app.route('/api/like/<int:s_id>')
def api_like(s_id):
    s = Sayings.query.filter(Sayings.id == s_id).first()
    if s:
        s.likes += 1
        #db_session.commit()
        return {
            'code': 200,
            'id': s.id,
            'saying': s.saying,
            'likes': s.likes
        }
    else:
        return {
            'code': 400,
            'id': None,
            'saying': None,
            'link': None
        }

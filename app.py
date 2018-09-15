from flask import Flask, request, make_response, jsonify, send_file
from gevent.pywsgi import WSGIServer
import requests
import traceback
import pymysql
import json
from io import BytesIO

app = Flask(__name__)

with open('config.json', 'r') as f:
    conf = json.load(f)
DATABASE = conf['mysql']
HYCON = conf['hycon']


def connect_db():
    return pymysql.connect(host=DATABASE['host'], 
            user=DATABASE['user'], 
            password=DATABASE['password'], 
            db=DATABASE['database'],
            charset='utf8', 
            cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/post', methods=['POST'])
def post():
    conn = connect_db()
    cur = conn.cursor()

    # 위치, 사진, 태그, 사용자
    user_address = request.values.get('user', None)  # 토큰받을 사용자의 address
    longitude = request.values.get('longitude', None)  # 경도
    latitude = request.values.get('latitude', None)  # 위도
    memo = request.values.get('memo', None)
    
    taglist = request.values.getlist('tags', None)
    tags = ','.join(taglist)

    img = request.files.get('img', None)
    img_name = img.filename
    img_mimetype = img.content_type

    # 입력받은 데이터 저장하기
    try:
        # 5 MT 발행하기
        api_hycon_transaction = "http://localhost:2442/api/v1/signedTx"
        payload = {
            "privateKey": HYCON['privateKey'],
            "from": HYCON['minerAddress'],
            "to": user_address,
            "amount": "0.000000005",
            "fee": "0.000000001"
        }
        r = requests.post(api_hycon_transaction, json=payload)
        rr = r.json()
        transaction_hash = rr['txHash']

        if r.status_code != 200:
            error = {
                "code": 1111,
                "type": "HyconError",
                "message": "Hycon server is temporary unavailable."
            }
            return make_response(jsonify(error=error), 500)

        query = """INSERT INTO places (longitude, latitude, img, img_name, img_mimetype, user_address, tags, memo, transaction_hash) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(query, (longitude, latitude, img.read(), img_name, img_mimetype, user_address, tags, memo, transaction_hash, ))
        place_id = cur.lastrowid

        query = "INSERT INTO tags (tag) VALUES (%s);"
        for tag in taglist:
            cur.execute(query, (tag, ))

        conn.commit()
    except:
        traceback.print_exc()
        conn.rollback()
        error = {
            "code": 2222,
            "type": "ServerError",
            "message": "Server is temporary unavailable."
        }
        return make_response(jsonify(error=error), 500)

    data = {
        "place_id": place_id,
        "transaction_hash": transaction_hash,
        "longitude": longitude,
        "latitude": latitude,
        "memo": memo,
        "tags": taglist
    }
    return make_response(jsonify(**data), 200)


@app.route('/get', methods=['GET'])
def get():
    # 현재 위치, 반경 범위
    longitude = request.values.get('longitude', None)  # 경도
    longitude = float(longitude)
    latitude = request.values.get('latitude', None)  # 위도
    latitude = float(latitude)
    range = request.values.get('range', None)
    range = float(range)
    
    # 현재 위치 기준 반경 범위안에 있는 곳 DB에서 꺼내기
    conn = connect_db()
    cur = conn.cursor()
    query = """SELECT id, longitude, latitude, img_name, user_address, tags, memo, transaction_hash, create_time FROM mmchain.places
            WHERE (longitude BETWEEN %s AND %s) AND (latitude BETWEEN %s AND %s);"""
    cur.execute(query, (longitude-range, longitude+range, latitude-range, latitude+range))
    ret = cur.fetchall()
    return make_response(jsonify(places=ret), 200)


@app.route('/img/<int:place_id>', methods=['GET'])
def img(place_id):
    conn = connect_db()
    cur = conn.cursor()
    query = "SELECT img, img_name, img_mimetype FROM mmchain.places WHERE id = %s;"
    cur.execute(query, (place_id, ))
    ret = cur.fetchone()

    return send_file(BytesIO(ret['img']), attachment_filename=ret['img_name'])


@app.route('/tags', methods=['GET'])
def tags():
    q = request.values.get('q', None)
    conn = connect_db()
    cur = conn.cursor()
    query = "SELECT id, tag FROM tags WHERE tag LIKE %s;"
    cur.execute(query, (q+'%', ))
    ret = cur.fetchall()
    return make_response(jsonify(tags=ret), 200)


@app.route('/balance', methods=['POST'])
def balance():
    address = request.values.get('address', None)
    api_hycon_wallet_balance = "http://fabius.ciceron.xyz:2442/api/v1/wallet/{}/balance".format(address)
    print(api_hycon_wallet_balance)
    r = requests.get(api_hycon_wallet_balance)
    rr = r.json()
    return make_response(jsonify(**rr), 200)


if __name__ == '__main__':
    # app.run()
    http = WSGIServer(('0.0.0.0', 5000), app)
    http.serve_forever()

import redis
from flask import Flask, request, jsonify

app = Flask("Autocomplete")

# creating a redis connection to port 6379
r = redis.StrictRedis(host='localhost', port=6379, db=0)

autocomplete_key = 'data'


@app.route('/')
def home():
    return "You're Home"


@app.route('/add_word')
def add():
    try:
        name = request.args.get('word')
        n = name.strip()
        for i in range(1, len(n)):
            prefix = n[0:i]
            r.zadd(autocomplete_key, {prefix: 0})
        r.zadd(autocomplete_key, {n + "*": 0})
        return {'status': 200, 'msg': 'Added successfully'}
    except Exception as e:
        return {'status': 500, 'msg': f'Failed to add due to {e}'}


@app.route('/autocomplete')
def get_autocomplete():
    prefix = request.args.get('query')
    results = []
    size = 50
    count = 5
    start = r.zrank(autocomplete_key, prefix)
    if not start:
        return []
    while len(results) != count:
        entries = r.zrange(autocomplete_key, start, start + size - 1)
        start += size
        if not entries or len(entries) == 0:
            break
        for entry in entries:
            entry = entry.decode('utf-8')
            min_len = min(len(entry), len(prefix))
            if entry[0:min_len] != prefix[0:min_len]:
                count = len(results)
                break
            if entry[-1] == "*" and len(results) != count:
                results.append(entry[0:-1])

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)

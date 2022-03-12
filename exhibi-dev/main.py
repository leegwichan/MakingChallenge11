from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.exhibition_info


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')


@app.route('/api/show/list', methods=['GET'])
def show_list():
    show_list = list(db.exhibition_info.find({}, {'_id': False}).sort('start_date', -1))
    return jsonify({'show_list': show_list})

# @app.route('/api/show/detail', methods=['POST'])
# def show_detail():
#     ticket_link_receive = request.form['ticket_link_give']
#     target_show = db.exhibition_info.find_one({'ticket_link': ticket_link_receive})
#
#     return jsonify({'msg': '이 요청은 POST!'})


@app.route('/api/show/detail', methods=['GET'])
def show_detail():
    ticket_link_receive = request.form['ticket_link_give']
    show_detail = db.exhibition_info.find_one({'ticket_link':'bobby'})
    return jsonify({'show_list': show_list_detail})
#
#
# @app.route('/test', methods=['POST'])
# def test_post1():
#     title_receive = request.form['title_give']
#     print(title_receive)
#     return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
   return '화면표시 영역'

@app.route('/map', methods=['POST'])
def test_post():
   latitude_receive = request.form['latitude_give']
   longitude_receive = request.form['longitude_give']
   print(latitude_receive,longitude_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 POST!'})


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
from flask import Flask, render_template, jsonify, request


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html',
    title = '세탁자리구함')

# 마이페이지
@app.route('/mypage')
def mypage():
   return render_template('mypage.html',
   title = '마이페이지')
   




@app.route('/joinMember', methods=['GET'])
def join():
    return render_template('join.html',
    title = '회원가입')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
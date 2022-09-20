from crypt import methods
from curses import flash
import bcrypt
from urllib import response
from flask import Flask, render_template, jsonify, request, session, flash, redirect
from pymongo import MongoClient


app = Flask(__name__)
app.secret_key = 'some_secret'

client = MongoClient('localhost', 27017)
db = client.washerReservation

@app.route('/')
def main():
    return render_template('index.html',
    title = '세탁자리구함')

# 마이페이지
@app.route('/mypage')
def mypage():
   return render_template('mypage.html',
   title = '마이페이지')
   
@app.route('/login', methods=['POST'])
def loginProccess():
    
    id_receive = request.form['id']
    password_receive = request.form['password']

    user = db.member.find_one({'id':id_receive},{'_id':False})
    
    if user is None :
        flash("사용자 정보가 없거나 일치하지 않습니다.")
        return render_template('index.html')

    if bcrypt.checkpw(password_receive.encode('utf-8'),user['password']) :
        return render_template('reservation.html')
    else:
        flash("사용자 정보가 없거나 일치하지 않습니다.")
        return render_template('index.html')

@app.route('/joinMember', methods=['GET','POST'])
def joinMember():
    if request.method == 'GET' :
         return render_template('join.html',title = '회원가입')
    else :
         id_receive = request.form['id']
         password_receive = request.form['password']
         password_encode = password_receive.encode('utf-8')
         password_hashed = bcrypt.hashpw(password_encode, bcrypt.gensalt())
         password_check_receive = request.form['passwordCheck']

         name_receive = request.form['name']
         room_number_receive = request.form['roomNumber']
         phone_number_receive = request.form['phoneNumber']


         member = {'id': id_receive,
                 'password': password_hashed,
                 'name': name_receive,
                 'roomNumber': room_number_receive,
                 'phoneNumber': phone_number_receive}

    try:
        db.member.insert_one(member)
    except request.exceptions.RequestException as e :
        return render_template('index.html', value=jsonify({'result': 'fail','member':member})) 
    return redirect('/') 

   

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
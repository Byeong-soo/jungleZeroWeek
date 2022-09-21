from crypt import methods
from curses import flash
from distutils.debug import DEBUG
import bcrypt
from flask import Flask, render_template, jsonify, request, session, flash,redirect,url_for,make_response
from flask_jwt_extended.config import config
from pymongo import MongoClient
from flask_jwt_extended import *
from jwt.exceptions import ExpiredSignatureError


app = Flask(__name__)
app.secret_key = 'some_secret'
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

client = MongoClient('localhost', 27017)
db = client.washerReservation

@app.route('/')
def main():
    return render_template('index.html',title = '세탁자리구함')
   
@app.route('/login', methods=['POST'])
def loginProccess():
    
    id_receive = request.form['id']
    password_receive = request.form['password']

    user = db.member.find_one({'id':id_receive},{'_id':False})
    
    if user is None :
        return jsonify({"result":False,"msg":"사용자 정보가 없거나 일치하지 않습니다."})

    if bcrypt.checkpw(password_receive.encode('utf-8'),user['password']) :
        access_token = create_access_token(identity=id_receive,expires_delta=False)
        
        return jsonify({"result":True,"token": access_token})
    else:
        return jsonify({"result":False,"msg":"사용자 정보가 없거나 일치하지 않습니다."})

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

    member = {'id':id_receive,
                 'password':password_hashed,
                 'name':name_receive,
                 'roomNumber':room_number_receive,
                 'phoneNumber':phone_number_receive}

    # 아이디 중복 확인 로직
    memberCount = len(list(db.member.find({'id':id_receive})))
    if memberCount >= 1 :
        flash("중복된 아이디입니다.")
        return redirect(url_for('joinMember'))

    try:
        db.member.insert_one(member)
    except request.exceptions.RequestException as e :
        return render_template('index.html', value=jsonify({'result': 'fail','member':member})) 
    return redirect('/') 


@app.route('/checkToken', methods=['GET'])
@jwt_required()
def reservation():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user),200

@app.route('/reservation', methods=['GET'])
def show_reservation():
    token = request.cookies.get('token')

    if token is None :
        flash("로그인을 먼저해주세요")
        return redirect('/')
    try :
        user = decode_token(token).get('sub')
    except ExpiredSignatureError:
        flash("유효하지않은 토큰입니다.") 
        return redirect('/')
    return render_template('reservation.html')
    
@app.route('/reservation', methods=['GET','POST'])
def reservation():
    if request.method == 'GET':
        return render_template('reservation.html', title= '예약페이지')
    else:
        laundry_receive = request.form['chk_info']
        date_receive = request.form['laundry_date'] 
        time_receive = request.form['laundry_time'] 
        laundry ={'chk_info' : laundry_receive,
                'date' : date_receive,
                'time' : time_receive}
        
    db.laundry.insert_one(laundry)

    
    return render_template('reservation.html')

@app.route('/mypage',methods=['GET'])
def show_mypage():
    token = request.cookies.get('token')
    if token is None :
        flash("로그인을 먼저해주세요")
        return redirect('/')
    try :
        user = decode_token(token).get("sub")
        member = db.member.find_one({'id':user})

    except ExpiredSignatureError: 
        flash("유효하지않은 토큰입니다.")
        return redirect('/')
    return render_template('mypage.html',member=member)


@app.route('/modifyMember',methods=['POST'])
@jwt_required()
def modify_member():
    id_receive = request.form['id']
    room_number_receive = request.form['roomNumber']
    phone_number_receive = request.form['phoneNumber']

    db.member.update_one({'id':id_receive},{'$set':{'roomNumber':room_number_receive, 'phoneNumber':phone_number_receive}})
    return jsonify({'result': 'success'})

@app.route('/deleteMember',methods=['POST'])
@jwt_required()
def delete_member():
    id_receive = request.form['id']
    db.member.delete_one({'id':id_receive})
    return jsonify({'result':'success'})
   
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
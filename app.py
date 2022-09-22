from crypt import methods
from curses import flash
from distutils.debug import DEBUG
import re
import bcrypt
from flask import Flask, render_template, jsonify, request, session, flash,redirect,url_for,make_response
from flask_jwt_extended.config import config
from pymongo import MongoClient
from flask_jwt_extended import *
from jwt.exceptions import ExpiredSignatureError
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'some_secret'
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

client = MongoClient('mongodb://ubs4939:DBqudtn587@3.34.47.69', 27017)
db = client.washerReservation

@app.route('/')
def main():
    token = request.cookies.get('token')
    if token is None :
        return render_template('index.html',title = '세탁자리구함')
    try :
        decode_token(token).get("sub")
    except ExpiredSignatureError: 
        return render_template('index.html',title = '세탁자리구함')
    return redirect('/reservation')

@app.route('/login', methods=['GET'])
def loginPage():
    return redirect('/')
   
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
def checkToken():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user),200

@app.route('/getReservations', methods=["POST"])
@jwt_required()
def inqury():
    in_date = request.form['laundry_date']
    in_time = request.form['laundry_time']
    
    inDate = list(db.laundry.find({'date':in_date,'time':in_time}))
    
    using_l = []
    for iNdate in inDate:
        using_l.append(iNdate['chk_info'])
    
    return jsonify(reservation=using_l)


@app.route('/reservation', methods=['GET','POST'])
def reservation():
    if request.method == 'GET':

        token = request.cookies.get('token')

        if token is None :
            flash("로그인을 먼저해주세요")
            return redirect('/')
        try :
            jti = decode_token(token)['jti']
            user = decode_token(token).get('sub')
        except ExpiredSignatureError:
            flash("접속이 만료되었습니다. 다시로그인 해주세요") 
            return redirect('/')
        logoutCheck = jti in jwt_blocklist
        if logoutCheck :
            flash("유효하지않은 토큰입니다.")
            return redirect('/')
        return render_template('reservation.html', title= '예약페이지')
    else:
        laundry_receive = request.form['washer']
        date_receive = request.form['laundry_date'] 
        time_receive = request.form['laundry_time'] 
        laundry ={'chk_info' : laundry_receive,
                'date' : date_receive,
                'time' : time_receive}
    
    db.laundry.insert_one(laundry)

    flash("예약이 완료되었습니다 시간을 지켜주세요")
    return redirect('/reservation')

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

jwt_blocklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) :
	jti = jwt_payload['jti']
	return jti in jwt_blocklist

@app.route('/tokenBlock', methods=['GET'])
@jwt_required()
def user_logout() :
    jti = get_jwt()['jti']
    print(jti) 
    jwt_blocklist.add(jti)
    return jsonify({'result':'success'})
   
if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
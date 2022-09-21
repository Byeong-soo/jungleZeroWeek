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
    return render_template('mypage.html', title='마이페이지')
   
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

  
@app.route('/mypage', methods=["GET"])
def mypage_get():
    reservations_list = list(db.reservations.find({},{'_id':False, }))
    return jsonify({'reservations':reservations_list})

@app.route('/mypage', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    word_receive = request.form['word_give']
    db.words.delete_one({"word": word_receive})
    db.examples.delete_many({"word": word_receive})
    return jsonify({'result': 'success', 'msg': f'word "{word_receive}" deleted'})


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


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)




# from flask import Flask
# app = Flask(__name__)
#

#
# @app.route('/')
# def home():
#    return 'This is Home!'
#
# if __name__ == '__main__':
#    app.run('0.0.0.0',port=5000,debug=True)
#
#
#
#
# #
# # @app.route('/')
# # def parts():
# #     return render_template('index.html',
# #                            title='세탁자리구함')
#
#
# @app.route('/mypage')
# def mypage():
#    return 'This is My Page!'
#

#
# # -----------
# #
# #
# # @app.route('/update_profile', methods=['POST'])
# # def save_img():
# #     token_receive = request.cookies.get('mytoken')
# #     try:
# #         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
# #         username = payload["id"]
# #         name_receive = request.form["name_give"]
# #         about_receive = request.form["about_give"]
# #         new_doc = {
# #             "profile_name": name_receive,
# #             "profile_info": about_receive
# #         }
# #         if 'file_give' in request.files:
# #             file = request.files["file_give"]
# #             filename = secure_filename(file.filename)
# #             extension = filename.split(".")[-1]
# #             file_path = f"profile_pics/{username}.{extension}"
# #             file.save("./static/" + file_path)
# #             new_doc["profile_pic"] = filename
# #             new_doc["profile_pic_real"] = file_path
# #         db.users.update_one({'username': payload['id']}, {'$set': new_doc})
# #         return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
# #     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
# #         return redirect(url_for("home"))
# #
# #
# # -----
# #
# # if __name__ == '__main__':
# #     app.run('0.0.0.0', port=5000, debug=True)
# #
# # doc = {
# #     'name':'bob',
# #     'age':27
# # }
# #
# # db.users.insert_one(doc)
# #
# # # 삽입
# #
# # # 저장 - 예시
# #
# # doc = {'user_id':'', 'time': , 'machine_number':''}
# # db.reservations.insert_one(doc)
# #
# # # 한 개 찾기 - 예시
# # reservation = db.reservations.find_one({'user_id':''})
# #
# #
# #
# # # 수정
# # db.user_informations.update_one({'user_id':''},{'$set':{'' : }})
# #
# # # 삭제
# # db.reservations.delete_one({'user_id':''})
# #
# #
#

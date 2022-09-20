from flask import Flask, render_template, jsonify

app = Flask(__name__)




from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.7pihtjb.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


doc = {'user_id':'KIM123', 'time':202201022100, 'machine_number':3}
db.reservations.insert_one(doc)



# date = datetime.datetime(2011, 11, 17, 18, 0)
# db.mydatabase.mycollection.insert({"date" : date})






@app.route('/')
def home():
   return render_template('index.html')

# 마이페이지
@app.route('/mypage')
def mypage():
    return render_template('mypage.html', title='마이페이지')


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

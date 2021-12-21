import json
from subprocess import Popen
from flask import Flask
from flask import render_template, request, redirect, url_for
import os
import random

from flask.helpers import make_response
app = Flask(__name__)

#404/500/405 에러페이지
@app.errorhandler(404)
def page_not_found(e):
    return render_template('result.html', res = "404", res2 = "Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('result.html', res = "500", res2 = "Internal Server Error"), 500

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('result.html', res = "405", res2 = "잘못된 접근입니다."), 405


#메인 페이지
@app.route("/")
def land_screen():
  return render_template("land.html")

#학생 등록 페이지
@app.route("/register")
def register_screen():
  return render_template("index.html")

#자가 진단 페이지
@app.route("/dowork")
def self_screen():
  return render_template("doself.html")

#자가 진단 수행 / POST로 학생 코드 입력받고 worker에 전달
@app.route("/doself", methods=['POST'])
def doself():
  STCODE = request.form['code']
  if len(STCODE) is not 4:
    return render_template("result.html", res= "Fail", res2="고유번호는 4자리입니다.")
  if os.path.isfile("./students/{0:04d}.json".format(int(STCODE))):
    Popen(["python", "scuvid_work.py", "./students/{0:04d}.json".format(int(STCODE))])
    resp = make_response(render_template("result.html", res= "success", res2="자가진단을 요청하였습니다."))
    resp.set_cookie('saved_ID', STCODE)
    return resp
  else:
    return render_template("result.html", res= "Fail", res2="해당 학생이 없습니다.")

#학생 등록 / POST로 학생 정보 입력받고 Json 파일 생성
@app.route("/doregister", methods=['POST'])
def register():
  name = request.form['name']
  pw = request.form['pw']
  birth = request.form['birth']
  i = 0
  if name == "" or pw == "" or birth == "":
    return render_template("result.html", res= "Fail", res2="모든 항목을 입력해주세요.")
  if len(pw) is not 4:
    return render_template("result.html", res= "Fail", res2="비밀번호는 4자리입니다.")
  if len(birth) is not 6:
    return render_template("result.html", res="Fail", res2="생년월일은 6자리입니다.")

  count=0
  for i in range(10000):
    if os.path.isfile("./students/{0:04d}.json".format(i)):
      with open("./students/{0:04d}.json".format(i), 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        count = count + 1
      if json_data['name'] == name and json_data['pw'] == pw and json_data['birth'] == birth:
        resp = make_response(render_template("result.html", res="Fail", res2="이미 가입됨. [{0:04d}]".format(i)))
        resp.set_cookie('saved_ID', "{0:04d}".format(i))
        return resp
  if count == 10000:
    return render_template("result.html", res="Fail", res2="더 이상 가입할 수 없습니다.")
  while True:
    i = random.randrange(0, 10000)
    if os.path.isfile("./students/{0:04d}.json".format(i)):
      continue
    else:
      break

  with open("./students/{0:04d}.json".format(i), "w", encoding="utf-8") as f:
    f.write('{"name":"'+name+'", "pw":"'+pw+'", "birth":"'+birth +'"}')
    print("{0:04d}.json".format(i))
    resp = make_response(render_template("result.html", res="Success", res2="고유 번호 [{0:04d}]".format(i)))
    resp.set_cookie('saved_ID', str(i))
    return resp


if __name__ == "__main__":
  try:
    app.run(host="0.0.0.0")
  finally:
    print("bye")
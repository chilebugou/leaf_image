import os
import time
from datetime import timedelta

import numpy as np
from werkzeug.utils import secure_filename

from app import app
from flask import render_template, Response, request, url_for, jsonify
from app.effects import effects_lib
import cv2


# from flask_wtf import FlaskForm
# from wtforms import  StringField, PasswordField, SubmitField
# from wtforms.validators import  Required

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


## No effects
def gen(effects):
    while True:
        frame = effects.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: images/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(effects_lib()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video1')
def video1():
    return render_template('effects.html')


##Caartoonize
def gen_cartoon(effects):
    while True:
        frame = effects.cartoonize()
        yield (b'--frame\r\n'
               b'Content-Type: images/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/cartoon')
def cartoon():
    return Response(gen_cartoon(effects_lib()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cartoonize')
def cartoonize():
    return render_template('cartoon.html')


##Oil Painting
def gen_oil_painting(effects):
    while True:
        frame = effects.oil_painting()
        yield (b'--frame\r\n'
               b'Content-Type: images/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/oil_painting')
def oil_painting():
    return Response(gen_oil_painting(effects_lib()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/oil_painting1')
def oil_painting1():
    return render_template('oil_painting.html')


##Black and White Sketch
def gen_black_and_white_sketch(effects):
    while True:
        frame = effects.black_and_white_sketch()
        yield (b'--frame\r\n'
               b'Content-Type: images/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/black_and_white_sketch')
def black_and_white_sketch():
    return Response(gen_black_and_white_sketch(effects_lib()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/black_and_white_sketch1')
def black_and_white_sketch1():
    return render_template('black_and_white_sketch.html')


##View all effects
@app.route('/all_effects')
def all_effects():
    return render_template('all_effects.html')


@app.route('/upload_image')
def upload_image():
    return render_template('upload_image.html')

##origin_img
def gen_origin_img(effects,f):
        frame = effects.origin_img(f)
        return (b'--frame\r\n'
               b'Content-Type: images/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/show_image')
def show_image():
    f = request.files['file']
    img=cv2.imread(f)

    return Response(img,mimetype="images/jpeg")

@app.route('/success', methods=['POST','GET'])#小写出bug lalala  chilebugou
def success():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        #cv2.waitKey()
        '''
        cv2.inRange()
        参数：
        img: 图像对象 / array
        lowerb: 低边界array，  如lower_blue = np.array([110, 50, 50])
        upperb：高边界array， 如
        upper_blue = np.array([130, 255, 255])
        '''
        lowerb=np.array([0,0,0])
        upperb=np.array([255,42,255])
        mask = cv2.inRange(HSV_img, lowerb, upperb)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test1.jpg'), img)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test2.jpg'), HSV_img)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test3.jpg'), mask)




        print(f)
        # img=cv2.imread(f)
        # print(img)
        # cv2.imshow(img)
        return render_template('success.html', name=f.filename,user_image=f,val1=time.time(),userinput=user_input)
    return render_template('upload_image.html')

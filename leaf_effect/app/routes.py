from app import app
from flask import render_template, Response, request, url_for
from app.effects import effects_lib
import cv2


# from flask_wtf import FlaskForm
# from wtforms import  StringField, PasswordField, SubmitField
# from wtforms.validators import  Required

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


## No effects
def gen(effects):
    while True:
        frame = effects.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


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
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


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
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


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
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


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
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/show_image')
def show_image():
    f = request.files['file']
    img=cv2.imread(f)

    return Response(img,mimetype="image/jpeg")

@app.route('/success', methods=['POST'])#小写出bug lalala  chilebugou
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)

        print(f)
        # img=cv2.imread(f)
        # print(img)
        # cv2.imshow(img)
    return render_template('success.html', name=f.filename,user_image=f)

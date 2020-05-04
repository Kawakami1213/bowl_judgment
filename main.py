import os
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.backend import set_session
import tensorflow as tf
import numpy as np
import path

PATH,UPLOAD_FOLDER = path.getpath()

classes = ["牛丼","天丼","かつ丼","海鮮丼"]
img_path = ["./static/gyudon.jpg", "./static/tendon.jpg", "./static/katsudon.jpg", "./static/kaisendon.jpg"]
num_classes = len(classes)
image_size = 50

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

session = tf.Session(graph=tf.get_default_graph())
graph = tf.get_default_graph()
set_session(session)
model = load_model(PATH + '/donburi_model.h5')#学習済みモデルをロードする

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global graph
    with graph.as_default():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('ファイルがありません')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('ファイルがありません')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                filepath = os.path.join(UPLOAD_FOLDER, filename)

                #受け取った画像を読み込み、np形式に変換
                img = image.load_img(filepath, grayscale=False, target_size=(image_size,image_size))
                img = image.img_to_array(img)
                data = np.array([img])
                #変換したデータをモデルに渡して予測する
                set_session(session)
                result = model.predict(data)[0]
                predicted = result.argmax()
                pred_answer = "これは " + classes[predicted] + " である可能性が 高いです。"

                return render_template("result.html",answer=pred_answer,img_src=img_path[predicted])

        return render_template("index.html",answer="")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=444, threaded=True)
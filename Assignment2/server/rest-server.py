#!flask/bin/python
################################################################################################################################
# ------------------------------------------------------------------------------------------------------------------------------
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
# -------------------------------------------------------------------------------------------------------------------------------
################################################################################################################################
import ctypes

from flask import Flask, jsonify, abort, request, make_response, url_for, redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil
import numpy as np
from search import recommend
import tarfile
from datetime import datetime
from scipy import ndimage

# from scipy.misc import imsave

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile

app = Flask(__name__, static_url_path="")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

# =============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
# ==============================================================================================================================
extracted_features = np.zeros((10000, 2048), dtype=np.float32)
with open('saved_features_recom.txt') as f:
    for i, line in enumerate(f):
        extracted_features[i, :] = line.split()
print("loaded extracted_features")


# ==============================================================================================================================
#                                                                                                                              
#  This function is used to do the image search/image retrieval
#                                                                                                                              
# ==============================================================================================================================
@app.route('/imgUpload', methods=['GET', 'POST'])
# def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_img():
    if gfile.Exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
    os.mkdir(UPLOAD_FOLDER)
    print("image upload")
    result = 'static/result'
    if not gfile.Exists(result):
        os.mkdir(result)
    shutil.rmtree(result)

    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)

        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:  # and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            image_path = "/result"
            image_list = [os.path.join(image_path, file) for file in os.listdir(result)
                          if not file.startswith('.') and file != "tag.txt"]
            images = {}
            with open("static/result/tag.txt") as f:
                is_tag = True
                now_tag = ""
                images["all_tags"] = []
                for line in f.readlines():
                    if is_tag:
                        is_tag = False
                        now_tag_str = line.replace(" ", "").replace("\t", "").strip()
                        now_tag = now_tag_str
                        images[now_tag] = []
                        images["all_tags"].append(now_tag)
                    else:
                        is_tag = True
                        now_imgs = line.split("\t")
                        for img in now_imgs:
                            now_path=os.path.join(image_path, img)
                            if img and img != "\n" and now_path not in images[now_tag]:
                                images[now_tag].append(now_path)
            images["all_imgs"] = image_list
            images["select_img"] = os.path.join("uploads/", file.filename)

            return jsonify(images)


# ==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
# ==============================================================================================================================
@app.route("/")
def main():
    return render_template("main.html")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')

from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/upload/<string:b_host>/<string:b_port>/<string:item_id>', methods=['GET', 'POST'])
def upload_image(b_host, b_port, item_id):
    if request.method == "GET":
        print('GET', b_host, b_port, item_id)
        dest_url = '/upload/{}/{}/{}'.format(b_host, b_port, item_id)
        return render_template('index.j2', dest_url=dest_url)
    print('POST', b_host, b_port, item_id)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    image = request.files['file']
    if image.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Your image is uploaded!')
        uri = 'http://{}:{}/img_uploaded/{}/{}'.format(b_host, b_port, item_id, filename)
        return redirect(uri)
    else:
        flash('Only png, jpg, jpeg, gif, image types allowed!')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run(port=64799, debug=True)

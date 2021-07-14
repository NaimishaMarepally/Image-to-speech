# Importing the necessary Libraries
from flask_cors import cross_origin
from flask import Flask, render_template, request
from main import text_to_speech
import os
import pytesseract
from PIL import Image
from werkzeug.utils import secure_filename;

# print(result)
# text = result
gender = 'Male'  # Voice assistant 
# text_to_speech(text, gender)

# import request

print("Started")
UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['png','jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
print("Aedho File Line")
@app.route('/', methods=['POST', 'GET'])
@cross_origin(app)
def homepage():
    if request.method == 'POST':
        f = request.files['file']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # hocr = request.form.get('hocr') or ''
        # ext = '.hocr' if hocr else '.txt'
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('frontend.html',output="No file selected.")
        if file:
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # img = Image.open('./ALLIMAGES/')
        print("Accesing Tesseract")
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        print("Accessed Tesseract")
        img = Image.open(file)

        render_template('frontend.html',output="Started Result")
        result = pytesseract.image_to_string(img)
        with open('abc.text',mode='w') as file:
            file.write(result)
            print(result)
        print("Selecting")
        text = result
        print(text)
        gender = request.form['voices']
        text_to_speech(text, gender)
        return render_template('frontend.html',output=result)
    else:
        return render_template('frontend.html')


if __name__ == "__main__":
    app.run()

# Importing the necessary Libraries
from flask_Cors import cross_origin
from flask import Flask, render_template, request
from main import text_to_speech
import os
import pytesseract
from PIL import Image
from werkzeug.utils import secure_filename

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
@cross_origin()
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
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # img = Image.open('./ALLIMAGES/')
        print("Accesing Tesseract")
        pytesseract.pytesseract.tesseract_cmd = '/app/vendor/tesseract-ocr/bin/tesseract'
        print("Accessed Tesseract")
        img = Image.open(file)

        print("Starting Result")
        result = pytesseract.image_to_string(img)
        with open('abc.text',mode='w') as file:
            file.write(result)
            print(result)
        print("Selecting")
        text = result
        print(text);
        gender = request.form['voices']
        text_to_speech(text, gender)
        return render_template('frontend.html',output=result)
    else:
        return render_template('frontend.html')


if __name__ == "__main__":
    app.run()

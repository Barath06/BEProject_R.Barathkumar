from flask import Flask,render_template,send_file,request
import os

import pytesseract as tess
tess.pytesseract.tesseract_cmd = 'C:/Users/Admin/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
from PIL import Image

from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class ocrImage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(500),nullable = False)

    def __repr__(self):
        return str(self.id)


app.config['IMAGE_UPLOADS'] = 'C:\\Users\\Admin\\Documents\\ocrproject\\static';

@app.route('/')
def mainpage():
    return render_template('OCR.html')
@app.route('/download')
def download_file():
    p = "textimg.txt"
    return send_file(p,as_attachment=True)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['inputFile']
    file.save(os.path.join(app.config['IMAGE_UPLOADS'], file.filename))
    print("image saved")

    img = Image.open(file)
    text = tess.image_to_string(img)
    print(text)


    with open('textimg.txt', 'w') as data:
        data.write(text)

    dummyArray = []
    DataArray = []
    impData=[]
    qualitydata=""
    VerbArray = ['and','he','she','it','He','She','It','the','The','at','a','A','to','be','am','is','are','was','were','been','being','have','has','had','could','should','would','may','might','must','shall','can','will','do','did','does','having']
    dummyArray = text.split()
    for x in dummyArray:
        if x not in VerbArray :
            DataArray.append(x)
        if len(x) >=5:
            impData.append(x)
    print(DataArray)
    print("\n")
    print(impData)
    for y in impData:
        qualitydata = qualitydata + " " + y
    new_post = ocrImage(content=qualitydata)
    db.session.add(new_post)
    db.session.commit()

    return render_template('OCR.html',data = impData)





    
    















  

if __name__ == "__main__":
    app.run(debug=True,port=8066)
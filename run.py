#!flask/bin/python
from flask import Flask,request,jsonify,render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import os
from google.cloud import vision
from subprocess import call, Popen, PIPE
import json
import sqlite3
import random
from faker import Faker
from cpp2python import conversiond

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from db_setup import db_session
UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wmn19.db'
app.secret_key = "wmn19"
 
db = SQLAlchemy(app)

from db_setup import init_db
 
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cpp')
def cpp():
    return render_template('cplus.html')

@app.route('/analytics')
def analytics():
    # funcrandom()
    return render_template('analytics.html')

@app.route('/conversion')
def conversion():
    # funcrandom()
    return render_template('conversion.html')


@app.route('/python')
def python():
    # funcrandom()
    return render_template('python.html')

# @app.route('/psuedo')
# def psuedo():
#     return render_template('psuedo.html')

@app.route('/upload',methods=['POST'])
@cross_origin(supports_credentials=True)
def upload():
    codedatafile = request.files.get('file')
    if codedatafile:
        filename = secure_filename(codedatafile.filename)
        codedatafile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        textcode = detect_document(filepath)
        # import pdb; pdb.set_trace()
        output = compilec(textcode)
        data = datetime.today().date()
        save_changes(data)
        return jsonify({'status':'ok','text':textcode,'output':output})
    return jsonify({'status':'No file !!'})

@app.route('/uploadcpp',methods=['POST'])
@cross_origin(supports_credentials=True)
def uploadcpp():
    codedatafile = request.files.get('file')
    if codedatafile:
        filename = secure_filename(codedatafile.filename)
        codedatafile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        textcode = detect_document(filepath)
        # import pdb; pdb.set_trace()
        output = compilecpp(textcode)
        data = datetime.today().date()
        save_changes(data)
        return jsonify({'status':'ok','text':textcode,'output':output})
    return jsonify({'status':'No file !!'})

@app.route('/uploadcppconversion',methods=['POST'])
@cross_origin(supports_credentials=True)
def uploadcppconversion():
    codedatafile = request.files.get('file')
    if codedatafile:
        filename = secure_filename(codedatafile.filename)
        codedatafile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        textcode = detect_document(filepath)
        # import pdb; pdb.set_trace()
        converse(textcode)
        # data = datetime.today().date()
        # save_changes(data)
        return jsonify({'status':'ok','text':textcode,'output':'success'})
    return jsonify({'status':'No file !!'})

# @app.route('/uploadpython',methods=['POST'])
# @cross_origin(supports_credentials=True)
# def uploadpython():
#     codedatafile = request.files.get('file')
#     if codedatafile:
#         filename = secure_filename(codedatafile.filename)
#         codedatafile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         textcode = detect_document(filepath)
#         # import pdb; pdb.set_trace()
#         output = compilepy(textcode)
#         data = datetime.today().date()
#         save_changes(data)
#         return jsonify({'status':'ok','text':textcode,'output':output})
#     return jsonify({'status':'No file !!'})

@app.route('/runupload',methods=['POST'])
def runupload():
    codedatafile = request.files.get('file')
    if codedatafile:
        filename = secure_filename(codedatafile.filename)
        codedatafile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print("detecing+++++++++++++++++++++++++++++++++++++++++++++")
        textcode = detect_document(filepath)
        return jsonify({'status':'ok','text':textcode})
    return jsonify({'status':'No file !!'})

@app.route('/run',methods=['POST'])
def compileandrun():
    print("processing+++++++++++++++++++++++++")
    data = request.json.get('code')
    output = compilec(data)
    return jsonify({'output':output})

# @app.route('/runpy',methods=['POST'])
# def compileandrunpython():
#     print("processing+++++++++++++++++++++++++")
#     data = request.json.get('code')
#     output = compilec(data)
#     return jsonify({'output':output})

@app.route('/runcpp',methods=['POST'])
def compileandruncpp():
    print("processing+++++++++++++++++++++++++")
    data = request.json.get('code')
    output = compilecpp(data)
    return jsonify({'output':output})

# @app.route('/runpython',methods=['POST'])
# def compileandrunpython():
#     print("processing+++++++++++++++++++++++++")
#     data = request.json.get('code')
#     output = compilepy(data)
#     return jsonify({'output':output})

@app.route('/runconversion',methods=['POST'])
def runconversion():
  data = request.json.get('code')
  output = converse(data)
#   import pdb; pdb.set_trace()
  return output

def converse(textcode):
    # import pdb; pdb.set_trace()
    conversiond()
    f = open("submission.py","r")
    contents = f.read()
    # json.dump(d, open("text.txt",'w'))
    # file_object = open("../submission.py", "r+")
    # print file_object.readlines()
    return contents

def compilec(textcode):
    with open('submission.c','w+') as mycode:
        mycode.write(textcode)
    ccompile = Popen(["gcc","submission.c"], stderr=PIPE)
    ccompileerr = ccompile.communicate()[1].decode()
    if ccompileerr != '':
        call(["rm","submission.c"])        
        return ccompileerr
    runoutput = Popen(["./a.out"], stdout=PIPE)
    # import pdb; pdb.set_trace()
    output = runoutput.communicate()[0]
    call(["rm","submission.c", "a.out"])
    return output.decode()

def compilepy(textcode):
    with open('submission.py','w+') as mycode:
        mycode.write(textcode)
    ccompile = Popen(["python","submission.py"], stderr=PIPE)     
    #import pdb; pdb.set_trace()
    import py_compile
    py_compile.compile('submission.py')
    runoutput = Popen(["python ./submission.pyc"], stdout=PIPE)
    output = runoutput.communicate()[0]
    call(["rm","submission.py", "submission.pyc"])
    return output.decode()

def compilecpp(textcode):
    with open('submission.cpp','w+') as mycode:
        mycode.write(textcode)
    ccompile = Popen(["g++","submission.cpp"], stderr=PIPE)
    ccompileerr = ccompile.communicate()[1].decode()
    if ccompileerr != '':
        return ccompileerr
    runoutput = Popen(["./a.out"], stdout=PIPE)
    output = runoutput.communicate()[0]
    call(["rm","submission.cpp", "a.out"])
    return output.decode()

def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    codedata = response.text_annotations[0].description
    return codedata

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def save_changes(data):
    """
    Save the changes to the database
    """
    # import pdb; pdb.set_trace()
    qry = db_session.query(Codebase).filter(Codebase.date==data)
    qry = qry.first()
    if qry:
        qry.code_count += 1
        db_session.commit()
        return "ok"
    
    codebaseobject = Codebase()
    codebaseobject.code_count = 1
    db_session.add(codebaseobject)
    db_session.commit()
    return "ook"

class Codebase(db.Model):
    """"""
    __tablename__ = "codebase"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date,default=datetime.today().date())
    code_count = db.Column(db.Integer)
 
    # def __init__(self, date,code_count):
    #     """"""
    #     self.date = date
    #     self.code_count = code_count
@app.route('/getseven',methods=["GET"])
def getseven():
    sevendays = (datetime.now() -timedelta(days=7)).date()
    resultdata = db_session.query(Codebase).filter(Codebase.date>sevendays)
    mydict = {}
    for result in resultdata:
        mydict[str(result.date)] = result.code_count
    
    return jsonify({'result':mydict})

@app.route('/getdata',methods=["GET"])
def getdata():
   resultdata = db_session.query(Codebase).all()
   mydict = {}
   # import pdb; pdb.set_trace()
   for result in resultdata:
       mydict[str(result.date)] = result.code_count
   
   return jsonify({'result':mydict})

# @app.route('/bills/fetch',methods=["POST"])
# def fetch

# @app.route('/getdata',methods=["GET"])
# def getdata():
#   conn = sqlite3.connect("/home/anshu/wmn19.db")
#   cur = conn.cursor()
#   cur.execute("SELECT * FROM codebase")
 
#   resultdata = cur.fetchall()
#   mydict = {}
#   for result in resultdata:
#     mydict[str(result.date)] = result.code_count
#   return jsonify({'result':mydict})

def funcrandom():
    fake = Faker()
    for i in range(300):
        datedata = fake.date_between(start_date='-1y', end_date='today')
        nodata = random.randint(1,500)
        codebaseobject = Codebase()
        codebaseobject.date = datedata
        codebaseobject.code_count = nodata
        db_session.add(codebaseobject)
        db_session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
from flask import Flask,redirect,url_for,render_template,request
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.utils import secure_filename
client=MongoClient('mongodb+srv://riska:sparta@cluster0.xgcssqd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db=client.adminbuah
from datetime import datetime
import os

app=Flask(__name__)
@app.route('/' ,methods=['GET'])
def home():
    fruit=list(db.fruit.find({}))
    return render_template('dashboard.html',fruit=fruit)

@app.route('/fruit' ,methods=['GET','POST'])
def fruit():
    fruit=list(db.fruit.find({}))
    print(fruit)
    return render_template('fruit.html', fruit=fruit)

@app.route('/Addfruit' ,methods=['GET','POST'])
def Addfruit():
    if request.method=='POST':
        nama=request.form['nama']
        price=request.form['price']
        deskripsi=request.form['deskripsi']

        gambar=request.files['gambar']
        extension=gambar.filename.split('.')[-1]
        today=datetime.now()
        mytime=today.strftime('%Y-%M-%d-%H-%m-%S')
        gambar_name=f'gambar-{mytime}.{extension}'
        save_to=f'static/assets/Imgfruit/{gambar_name}'
        gambar.save(save_to)

        doc={
            'nama':nama,
            'price':price,
            'deskripsi':deskripsi,
            'gambar':gambar_name
        }
        db.fruit.insert_one(doc)
        return redirect(url_for('fruit'))
        return render_template('index.html')
    return render_template('Addfruit.html')

@app.route('/Editfruit/<_id>' ,methods=['GET','POST'])
def Editfruit(_id):
    if request.method=='POST':
        nama=request.form['nama']
        price=request.form['price']
        deskripsi=request.form['deskripsi']

        gambar=request.files['gambar']
        extension=gambar.filename.split('.')[-1]
        today=datetime.now()
        mytime=today.strftime('%Y-%M-%d-%H-%m-%S')
        gambar_name=f'gambar-{mytime}.{extension}'
        save_to=f'static/assets/Imgfruit/{gambar_name}'
        gambar.save(save_to)

        doc={
            'nama':nama,
            'price':price,
            'deskripsi':deskripsi,
        }
        if gambar_name:
            doc['gambar']=gambar_name
        db.fruit.update_one({'_id':ObjectId(_id)},{'$set':doc})
        return redirect(url_for('fruit'))
        return render_template('index.html')
    id=ObjectId(_id)
    data=list(db.fruit.find({'_id':id}))
    print(data)
    return render_template('Editfruit.html',data=data)

@app.route('/Deletefruit/<_id>' ,methods=['GET','POST'])
def delete(_id):
    db.fruit.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('fruit'))

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)
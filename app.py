from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os


PATH = os.getcwd()
UPLOAD_FOLDER = "/static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receipts.db'
db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), default="Details..")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    tag = db.Column(db.String(30), nullable=False, default="Common Expenses")
    belonging_user_id = db.Column(db.Integer, primary_key=False)
    total_cost = db.Column(db.Float, nullable=False, default=25)
    location = db.Column(db.String(100), nullable=False, default="Ankara")
    photo_path = db.Column(db.String(100), nullable=False, default="")
    #photo should exist as a column as well
    

    def __repr__(self):
        return '<Receipt %r>' % self.id


@app.route('/', methods=['POST', 'GET', 'PUT'])
def index():
    if request.method == 'POST':
        receipt_name = request.form['name']
        receipt_location = request.form['location']
        receipt_tag = request.form['tag'] 
        receipt_total_cost = request.form['total_cost']

       
        file = request.files['file']

        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(PATH + UPLOAD_FOLDER, filename))
            receipt_photo_path = os.path.join(UPLOAD_FOLDER, filename)
        else:
            receipt_photo_path = ""
            

        new_receipt = Receipt(name=receipt_name,total_cost=receipt_total_cost, location=receipt_location, tag=receipt_tag, photo_path=receipt_photo_path)

        try:
            db.session.add(new_receipt)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your receipt'

    else:
        receipts = Receipt.query.order_by(Receipt.date_created).all()
        return render_template('index.html', receipts=receipts)


@app.route('/delete/<int:id>')
def delete(id):
    receipt_to_delete = Receipt.query.get_or_404(id)

    try:
        db.session.delete(receipt_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that receipt'

@app.route('/details/<int:id>', methods=['GET', 'POST'])
def details(id):
    receipt = Receipt.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            return redirect('/')
        except:
            return 'There was an issue detailing your receipt'
    else:
        return render_template('details.html', receipt=receipt)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    receipt = Receipt.query.get_or_404(id)


    if request.method == 'POST':
        receipt.name = request.form['name']
        receipt.total_cost = request.form['total_cost']
        receipt.tag = request.form['category']
        receipt.location = request.form['location']
        date_created = request.form['date_created']

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(PATH + UPLOAD_FOLDER, filename))
            receipt.photo_path = os.path.join(UPLOAD_FOLDER, filename)
        else:
            receipt_photo_path = ""

        #Convert browser date format to sqlite date format 
        Ddate_created = datetime.strptime(date_created, '%Y-%m-%d')
        
        receipt.date_created = Ddate_created.date()

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your receipt'

    else:
        return render_template('update.html', receipt=receipt)

@app.route('/enter_details/<int:id>', methods=['GET', 'POST'])
def enter_details(id):
    receipt = Receipt.query.get_or_404(id)

    if request.method == 'POST':
        receipt.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your receipt details'

    else:
        return render_template('update_2.html', receipt=receipt)

@app.route('/search',  methods=['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        search_string = request.form['search']
        searchBox = request.form.getlist('searchBox')

        if (len(searchBox)==0):
            receipts1 = Receipt.query.filter(Receipt.name.like(search_string + "%")).all()   
            receipts2 = Receipt.query.filter(Receipt.location.like(search_string + "%")).all()
            receipts3 = Receipt.query.filter(Receipt.tag.like(search_string + "%")).all()   
            receiptsFinal = receipts1 + receipts2 + receipts3   
        elif(len(searchBox)==1):
            if(searchBox[0]=="1"):
                receipts1 = Receipt.query.filter(Receipt.name.like(search_string + "%")).all()
                receiptsFinal = receipts1
            elif(searchBox[0]=="2"):
                receipts2 = Receipt.query.filter(Receipt.location.like(search_string + "%")).all()
                receiptsFinal = receipts2
            elif(searchBox[0]=="3"):
                receipts3 = Receipt.query.filter(Receipt.tag.like(search_string + "%")).all()  
                receiptsFinal = receipts3 
        elif(len(searchBox)==2):
            if(searchBox[0]=="1" and searchBox[1]=="2"):
                receipts1 = Receipt.query.filter(Receipt.name.like(search_string + "%")).all()
                receipts2 = Receipt.query.filter(Receipt.location.like(search_string + "%")).all()
                receiptsFinal = receipts1 + receipts2
            if(searchBox[0]=="1" and searchBox[1]=="3"):
                receipts1 = Receipt.query.filter(Receipt.name.like(search_string + "%")).all()
                receipts3 = Receipt.query.filter(Receipt.tag.like(search_string + "%")).all()  
                receiptsFinal = receipts1 + receipts3 
            if(searchBox[0]=="2" and searchBox[1]=="3"):
                receipts3 = Receipt.query.filter(Receipt.tag.like(search_string + "%")).all() 
                receipts2 = Receipt.query.filter(Receipt.location.like(search_string + "%")).all() 
                receiptsFinal = receipts2 + receipts3 
        elif(len(searchBox)==3):
            receipts1 = Receipt.query.filter(Receipt.name.like(search_string + "%")).all()   
            receipts2 = Receipt.query.filter(Receipt.location.like(search_string + "%")).all()
            receipts3 = Receipt.query.filter(Receipt.tag.like(search_string + "%")).all()   
            receiptsFinal = receipts1 + receipts2 + receipts3

                   
        return render_template('results.html', receipts=receiptsFinal)


if __name__ == "__main__":
    app.run(debug=True)

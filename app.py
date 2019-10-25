from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receipts.db'
db = SQLAlchemy(app)

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), default="Details..")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    tag = db.Column(db.String(30), nullable=False, default="Common Expenses")
    belonging_user_id = db.Column(db.Integer, primary_key=False)
    total_cost = db.Column(db.Float, nullable=False, default=25)
    location = db.Column(db.String(100), nullable=False, default="Ankara")
    #photo should exist as a column as well
    

    def __repr__(self):
        return '<Receipt %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        receipt_name = request.form['name']
        receipt_location = request.form['location']
        receipt_tag = request.form['tag'] 
        receipt_total_cost = request.form['total_cost']

        new_receipt = Receipt(name=receipt_name,total_cost=receipt_total_cost, location=receipt_location, tag=receipt_tag)

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


if __name__ == "__main__":
    app.run(debug=True)

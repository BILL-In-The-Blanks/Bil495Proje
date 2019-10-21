from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receipts.db'
db = SQLAlchemy(app)

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #tag = db.Column(db.String(30), nullable=False, default="Common Expenses")
    #belonging_user_id = db.Column(db.Integer, primary_key=False)
    #total_cost = db.Column(db.Float, nullable=False, default=25)
    #location = db.Column(db.String(100), nullable=False, default="Ankara")
    #photo should exist as a column as well
    

    def __repr__(self):
        return '<Receipt %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        receipt_content = request.form['content']
        new_receipt = Receipt(content=receipt_content)

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

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    receipt = Receipt.query.get_or_404(id)

    if request.method == 'POST':
        receipt.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your receipt'

    else:
        return render_template('update.html', receipt=receipt)


if __name__ == "__main__":
    app.run(debug=True)

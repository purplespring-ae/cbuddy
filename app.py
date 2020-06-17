from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initials = db.Column(db.String(3), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Client {self.id}'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        client_initials = request.form['initials']

        try:
            db.session.add(client_initials)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem adding the client.'

    else:
        clients = Client.query.order_by(Client.initials).all()
        return render_template('index.html', clients=clients)


@app.route('/delete/<int:id>')
def delete(id):
    client_to_delete = Client.query.get_or_404(id)

    try:
        db.session.delete(client_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem updating the client.'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    client = Client.query.get_or_404(id)

    if request.method == 'POST':
        client.initials = request.form['initials']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return render_template('viewclient.html', client=client)


if __name__ == '__main__':
    app.run(debug=True)

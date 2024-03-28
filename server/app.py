from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    messages = Message.query.order_by('created_at').all()

    if request.method == 'GET':
        resp = [message.to_dict() for message in messages]
        return make_response(resp, 200)
    elif request.method == 'POST':
        form_data = request.get_json()
        new_message = Message(
            body=form_data['body'],
            username=form_data['username']
        )
        db.session.add(new_message)
        db.session.commit()
    return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    new_message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        form_data = request.get_json()
        for attr in form_data:
            setattr(new_message, attr, form_data.get(attr))
        db.session.add(new_message)
        db.session.commit()
        return make_response(new_message.to_dict(), 200)
    elif request.method == 'DELETE':
        db.session.delete(new_message)
        db.session.commit()
        return make_response({'deleted':True}, 200)

if __name__ == '__main__':
    app.run(port=5555)

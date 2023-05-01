from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_impacta.db3'
db = SQLAlchemy(app)

class cliente(db.Model):
    cliente_id = db.Column(db.Integer, primary_key=True)
    cliente_name = db.Column(db.String(50), nullable=False)
    cliente_score = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'cliente_id': self.cliente_id, 'cliente_name': self.cliente_name, 'cliente_score': self.cliente_score}

@app.route('/cliente/', methods=['GET'])
def get_all_clientes():
    clientes = cliente.query.all()
    return jsonify([cli.to_dict() for cli in clientes])

@app.route('/cliente/', methods=['POST'])
def create_cliente():
    data = request.get_json()
    new_cliente = cliente(cliente_name=data['name'], cliente_score=data['score'])
    db.session.add(new_cliente)
    db.session.commit()
    return jsonify(new_cliente.to_dict()), 201

@app.route('/cliente/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    cliente_to_delete = cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente_to_delete)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
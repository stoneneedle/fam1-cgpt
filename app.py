from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Create the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
CORS(app, origins=['http://localhost:3000'], supports_credentials=True)
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Define your model
class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


# Create the Marshmallow schema
class ExampleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExampleModel


# Initialize the schema
example_schema = ExampleSchema()
examples_schema = ExampleSchema(many=True)


# Check if there are no existing examples, then create and persist example objects
with app.app_context():
    db.create_all()

    if not ExampleModel.query.first():
        example1 = ExampleModel(name='Example 1')
        example2 = ExampleModel(name='Example 2')

        db.session.add(example1)
        db.session.add(example2)
        db.session.commit()


# REST Controller
@app.route('/example', methods=['GET'])
def get_examples():
    examples = ExampleModel.query.all()
    return jsonify(examples_schema.dump(examples))


@app.route('/example/<id>', methods=['GET'])
def get_example(id):
    example = ExampleModel.query.get(id)
    return jsonify(example_schema.dump(example))


@app.route('/example', methods=['POST'])
def create_example():
    name = request.json['name']
    
    # Check if the name already exists
    if ExampleModel.query.filter_by(name=name).first():
        return jsonify({'error': 'Name already exists'}), 400
    
    new_example = ExampleModel(name=name)
    db.session.add(new_example)
    db.session.commit()
    return jsonify(example_schema.dump(new_example))


@app.route('/example/<id>', methods=['PUT'])
def update_example(id):
    example = ExampleModel.query.get(id)
    name = request.json['name']
    
    # Check if the new name already exists
    if ExampleModel.query.filter(ExampleModel.id != id, ExampleModel.name == name).first():
        return jsonify({'error': 'Name already exists'}), 400
    
    example.name = name
    db.session.commit()
    return jsonify(example_schema.dump(example))


@app.route('/example/<id>', methods=['DELETE'])
def delete_example(id):
    example = ExampleModel.query.get(id)
    db.session.delete(example)
    db.session.commit()
    return jsonify({'message': 'Example deleted'})


if __name__ == '__main__':
    app.run(debug=True)

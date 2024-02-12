# FAM (Flask-(SQL)Alchemy-Marshmallow) Stack API Server

The following is the ChatGPT conversation that coded this boilerplate.

**Me:** Can you write a flask server boilerplate with Flask-SQLAlchemy and a Marshmallow REST controller?

**ChatGPT:** Certainly! Here's a simple Flask server boilerplate with Flask-SQLAlchemy and Marshmallow for creating a basic REST API. Make sure you have Flask, Flask-SQLAlchemy, and Marshmallow installed using:

```bash
pip install Flask Flask-SQLAlchemy Marshmallow

```
Now, you can create your Flask application:

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Define your model
class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


# Create the database tables
db.create_all()


# Create the Marshmallow schema
class ExampleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExampleModel


# Initialize the schema
example_schema = ExampleSchema()
examples_schema = ExampleSchema(many=True)


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
    new_example = ExampleModel(name=name)
    db.session.add(new_example)
    db.session.commit()
    return jsonify(example_schema.dump(new_example))


@app.route('/example/<id>', methods=['PUT'])
def update_example(id):
    example = ExampleModel.query.get(id)
    name = request.json['name']
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
```

This example assumes a simple model called ExampleModel with a single attribute name. The routes for GET, POST, PUT, and DELETE are provided for managing instances of this model.

Remember to adapt this code according to your actual model and requirements. Additionally, consider using more advanced features like authentication, error handling, or additional validation based on your application needs.

**Me:** Hi ChatGPT. Running your code gives the following error:

  File "/Users/jamesgroth/pythonml/fam1-cgpt/venv/lib/python3.11/site-packages/werkzeug/local.py", line 508, in _get_current_object
    raise RuntimeError(unbound_message) from None
RuntimeError: Working outside of application context.

This typically means that you attempted to use functionality that needed
the current application. To solve this, set up an application context
with app.app_context(). See the documentation for more information.
**ChatGPT:** I apologize for the oversight. The error is occurring because you need to use the Flask application context when working with Flask-SQLAlchemy. Specifically, database operations should be performed within the context of the Flask application.

To fix this issue, you can wrap the database operations inside the with app.app_context(): block. Here's the modified code:

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Define your model
class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


# Create the database tables
db.create_all()


# Create the Marshmallow schema
class ExampleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExampleModel


# Initialize the schema
example_schema = ExampleSchema()
examples_schema = ExampleSchema(many=True)


# REST Controller
@app.route('/example', methods=['GET'])
def get_examples():
    with app.app_context():
        examples = ExampleModel.query.all()
        return jsonify(examples_schema.dump(examples))


@app.route('/example/<id>', methods=['GET'])
def get_example(id):
    with app.app_context():
        example = ExampleModel.query.get(id)
        return jsonify(example_schema.dump(example))


@app.route('/example', methods=['POST'])
def create_example():
    with app.app_context():
        name = request.json['name']
        new_example = ExampleModel(name=name)
        db.session.add(new_example)
        db.session.commit()
        return jsonify(example_schema.dump(new_example))


@app.route('/example/<id>', methods=['PUT'])
def update_example(id):
    with app.app_context():
        example = ExampleModel.query.get(id)
        name = request.json['name']
        example.name = name
        db.session.commit()
        return jsonify(example_schema.dump(example))


@app.route('/example/<id>', methods=['DELETE'])
def delete_example(id):
    with app.app_context():
        example = ExampleModel.query.get(id)
        db.session.delete(example)
        db.session.commit()
        return jsonify({'message': 'Example deleted'})


if __name__ == '__main__':
    app.run(debug=True)
```

This modification ensures that database operations are performed within the application context, resolving the "Working outside of application context" error.

**Me:** Still getting this error:

RuntimeError: Working outside of application context.

This typically means that you attempted to use functionality that needed
the current application. To solve this, set up an application context
with app.app_context(). See the documentation for more information.

**ChatGPT:** I apologize for the confusion. It seems I missed a crucial detail in my response. While the Flask-SQLAlchemy operations should indeed be within an application context, Flask-RESTful itself manages the application context for the request lifecycle.

The issue here is with the database models being defined outside the application context. To fix this, you can move the model definition inside the create_app function or use the current_app proxy object provided by Flask.

Here's the updated code:

```python
from flask import Flask, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Create the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
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
    new_example = ExampleModel(name=name)
    db.session.add(new_example)
    db.session.commit()
    return jsonify(example_schema.dump(new_example))


@app.route('/example/<id>', methods=['PUT'])
def update_example(id):
    example = ExampleModel.query.get(id)
    name = request.json['name']
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
```
This should resolve the "Working outside of application context" error.

**Me:** Can you add in a few example objects created and persisted in DB?
**ChatGPT:** Certainly! You can add a few example objects to the database during the initialization phase. I'll modify the code to include the creation and persistence of a few example objects in the database. Here's an updated version:

```python
from flask import Flask, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Create the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
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


# Create and persist example objects
with app.app_context():
    db.create_all()

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
    new_example = ExampleModel(name=name)
    db.session.add(new_example)
    db.session.commit()
    return jsonify(example_schema.dump(new_example))


@app.route('/example/<id>', methods=['PUT'])
def update_example(id):
    example = ExampleModel.query.get(id)
    name = request.json['name']
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
```

This modification adds two example objects during the initialization phase. You can customize the names and attributes of these objects as needed.

**Me:**
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: example_model.name
[SQL: INSERT INTO example_model (name) VALUES (?) RETURNING id]
[parameters: ('Example 1',)]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
**ChatGPT:**
It appears that you are encountering a UNIQUE constraint failed error when trying to insert an example object with a name that already exists in the database. This error is because the name column in your ExampleModel is defined as unique, and you are trying to insert a record with a duplicate value.

To resolve this issue, you can modify the names of the example objects or clear the database and rerun the application. Here's an updated version that includes a check to avoid duplicate entries:

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Create the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
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
```

This version checks if there are no existing examples before creating and persisting the example objects. Additionally, it includes checks to prevent the insertion of duplicate names in the create_example and update_example routes.

**Me:** Whoa, it worked. You did it!

**ChatGPT:** I'm glad to hear that it worked! If you have any more questions, need further assistance, or want to explore other topics, feel free to ask. Happy coding!

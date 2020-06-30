import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
print("Hello")
app = Flask(__name__)
setup_db(app)
CORS(app,resources={r"*": {"origins": "*"}})
  

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
''' 
#db_drop_and_create_all()

## ROUTES
    
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.after_request
def after_request(response):
    print("In request  ")
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type, Authorization, true')
    response.headers.add( 
        'Access-Control-Allow-Methods',
        'GET, POST, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin','*')
    return response 


@app.route('/drinks')
@requires_auth('get:drink-details')
def get_drinks(payload):
    try:
        print(payload)
        drink_objects = Drink.query.all()
        if drink_objects is not None:
            drinks = [drink.short() for drink in drink_objects]
        else:
            return jsonify({
                "success" : True,
                "drinks" : []
            })

    except Exception:
        abort(400)

    return jsonify({
        "success" : True,
        "drinks" : drinks
    }), 200





'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drink-details')
def get_drinks_detail(payload):
    try:
        print(payload)
        drink_objects = Drink.query.all()
        if drink_objects is not None:
            drinks = [drink.long() for drink in drink_objects]
        else:
            return jsonify({
                "success" : True,
                "drinks" : []
            })

    except Exception:
        abort(400)

    return jsonify({ 
        "success" : True,
        "drinks" : drinks
    }), 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    try:
        print(payload)
        response = request.get_json() 
        print(f"resposne{response}")
        title = response['title']
        recipe = response['recipe']
        new_drink = Drink(title=title, recipe=json.dumps(recipe))
        new_drink.insert()
        return jsonify({
            "success" : True,
            "drinks" : new_drink.long()
        }), 200
    except:
        abort(400)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload, drink_id):
    try:
        body = request.get_json()
        drink = Drink.query.get(drink_id)
        title = body['title']
        recipe = body['recipe']
        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
        return jsonify({
            "success" : True,
            "drinks" : drink.long()
        }), 200
    except:
        abort(400)





'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        delete_drink = Drink.query.get(drink_id)
        delete_drink.delete()
        return jsonify({
            "success" : True,
            "drinks" : delete_drink.long()
        }), 200
    except:
        abort(404)


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def notFound(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Resource Not Found"
                    }), 404

@app.errorhandler(400)
def badRequest(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "Bad Request"
                    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "Unauthorized"
                    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
                    "success": False, 
                    "error": 403,
                    "message": "Permission to perform action not present"
                    }), 403

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({"first_name": "John"})
jackson_family.add_member({"first_name": "Jane"})
jackson_family.add_member({"first_name": "Jimmy"})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_all_member():
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 20


@app.route('/members/<string:member_id>', methods=['GET'])
def handle_get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        errors = {
            "get_error": f"Member with the ID {member_id} doesn't exist."
        }
        return jsonify(errors), 400
    
    return jsonify(member), 200


@app.route('/members', methods=['POST'])
def handle_add_member():
    request_body = request.json

    if type(request_body) != dict or "first_name" not in request_body:
        errors = {
            "add_error": "The request body must be an object with at least 'first_name' property."
        }
        return jsonify(errors), 400

    
    if type(request_body["first_name"]) != str or len(request_body["first_name"]) < 1:
        errors = {
            "add_error": "The property 'first_name' must be an string with at least 1 character."
        }
        return jsonify(errors), 400
    
    jackson_family.add_member(request_body)
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<string:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    members = jackson_family.get_all_members()
    member = jackson_family.get_member(member_id)

    if member is None:
        errors = {
            "delete_error": f"Member with the ID '{member_id}' doesn't exist."
        }
        return jsonify(errors), 400
    
    members.remove(member)
    return jsonify(members), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
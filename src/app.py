import os
from flask import Flask, render_template, request
from utils import APIException, generate_sitemap
from flask_cors import CORS
from datastructures import FamilyStructure
from flask import Flask, jsonify

app = Flask(__name__)

jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [ 7, 13, 22],
    "id": 1
})

jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3],
    "id":2
   
})

jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1],
    "id":3
})


@app.route("/")
def home():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    members = jackson_family.get_member(id)
    if  members:
         return jsonify(members), 200
    return jsonify({"error":"Member not found"}), 404
   
 
@app.route('/add', methods=['POST'])
def add_member():
    try:
        new_member = {
            "first_name":request.json['first_name'],
            "age":request.json['age'],
            "lucky_numbers":request.json['lucky_numbers'],
            "id": jackson_family._generateId()
        }
        jackson_family.add_member(new_member)
        return jsonify({
            "message":"Member Added Succesfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    members = jackson_family.get_member(id)
    if not members:
        return jsonify({"error":"Member not found"}),404
    jackson_family.delete_member(id)
    return jsonify({"message": "Member deleted successfully"}), 200

@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    #Obtener los datos JSON del cuerpo de la solicitud
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error":"No data provided"}),400
    #verificar si el miembro existe
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"error":"Member not found"}),404
    
    # jackson_family.update_member(id,update_data)

    # return jsonify({"message": "Member deleted successfully"}), 200
    try:
        jackson_family.update_member(id, update_data)
        return jsonify({"message": "Member updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
   
if __name__ == "__main__":
    app.run(debug=True)

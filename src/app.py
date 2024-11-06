from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

members = [
    {"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]},
    {"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]},
    {"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]}
]
for member in members:
    jackson_family.add_member(member)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404


@app.route('/member', methods=['POST'])
def create_member():
    member_data = request.json
    if not member_data or "first_name" not in member_data or "age" not in member_data:
        return jsonify({"error": "Invalid member data"}), 400
    member = jackson_family.add_member(member_data)
    return jsonify(member), 201


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    result = jackson_family.delete_member(id)
    if result.get("done"):
        return jsonify({"message": "Member deleted successfully"}), 200
    else:
        return jsonify(result), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 3000)), debug=True)

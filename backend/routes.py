from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    # Find the picture URL with the given id
    for picture in data:
        if picture['id'] == id:
            return jsonify(picture), 200
    
    # If no picture found with the given id, return 404 Not Found
    abort(404)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    picture_id = picture.get('id')
    
    # Check if picture with the same id already exists
    for pic in data:
        if pic['id'] == picture_id:
            return jsonify({"Message": f"picture with id {picture_id} already present"}), 302
    
    # Append the new picture to the data list
    data.append(picture)
    
    # Return the response with the id of the newly created picture
    return jsonify({"id": picture_id, "Message": "Picture added successfully"}), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_data = request.get_json()
    
    # Find the picture with the given id
    for picture in data:
        if picture['id'] == id:
            # Update the picture data
            picture.update(picture_data)
            return jsonify({"message": "Picture updated successfully"}), 200
    
    # If picture not found, return 404 Not Found
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Traverse the data list to find the picture by id
    for picture in data:
        if picture['id'] == id:
            # Delete the item from the list
            data.remove(picture)
            return '', 204  # Return an empty body with HTTP_204_NO_CONTENT
    
    # If the picture does not exist, return 404 Not Found
    return jsonify({"message": "picture not found"}), 404


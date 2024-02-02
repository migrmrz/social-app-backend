from flask import Flask, jsonify, request, make_response, json
import jsonschema
from jsonschema import validate
from http import HTTPStatus
from pymongo_inmemory import MongoClient
import bson

app = Flask(__name__)

# Define JSON schema for validation on create
like_schema = {
    "type": "object",
    "properties": {
        "from_user_id": {"type": "string"}
    },
    "additionalProperties": False,
    "required": ["from_user_id"]
}

comment_schema = {
    "type": "object",
    "properties": {
        "body": {"type": "string"},
        "from_user_id": {"type": "string"},
        "mbti": {"type": "string"},
        "likes_count": {"type": "number"},
    },
    "additionalProperties": False,
    "required": ["body", "from_user_id", "mbti"]
}

user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "mbti": {"type": "string"},
        "enneagram": {"type": "string"},
        "variant": {"type": "string"},
        "tritype": {"type": "number"},
        "socionics": {"type": "string"},
        "sloan": {"type": "string"},
        "psyche": {"type": "string"},
        "temperaments": {"type": "string"},
        "image": {"type": "string"},
    },
    "additionalProperties": False,
}

# Create MongoDB client
print("Creating connection to MongoDB...")
client = MongoClient()

# Define database
db = client['app-db']

# Define collections
user_collection = db['user-collection']
comment_collection = db['comment-collection']


# Create User endpoint
@app.route("/api/v1.0/user", methods=['POST'])
def create_user():
    """
        Endpoint for creating users.

        Body:
            - `name` (string)
            - `description` (string)
            - `mbti` (string)
            - `enneagram` (string)
            - `variant` (string)
            - `tritype` (int)
            - `socionics` (string)
            - `sloan` (string)
            - `psyche` (string)
            - `temperaments` (string)
            - `image` (string)

        Response:
            - unique id from the generated record
    """

    data = request.get_json()

    # Validate JSON Schema
    print("Validating JSON Schema...")
    try:
        validate(instance=data, schema=user_schema)
    except jsonschema.exceptions.ValidationError as err:
        return make_response(
            {"ValidationError": err.message},
            HTTPStatus.BAD_REQUEST
        )

    inserted_id = user_collection.insert_one(data).inserted_id

    return make_response(
        jsonify({"id": str(inserted_id)}),
        HTTPStatus.CREATED,
    )


# Get User endpoint
@app.route("/api/v1.0/user/<string:id>", methods=["GET"])
def get_user(id):
    """
        Endpoint for getting a user's data.

        Param:
        - `id`: id of the user to get.

        Response:
            - JSON structure with the details of the user
    """
    # Get data by id
    data = user_collection.find_one({"_id": bson.ObjectId(id)})

    # Take data for ObjectID to string conversion
    # and then convert back to json
    data_json = json.loads(json.dumps(data, default=str))
    if not data_json:  # no data found, return 404
        return make_response(
            jsonify({"response": "no data"}),
            HTTPStatus.NOT_FOUND
        )

    return jsonify(data_json)


# Post comment endpoint
@app.route("/api/v1.0/user/<user_id>/comment", methods=["POST"])
def post_comment(user_id):
    """
        Endpoint for posting comments.

        Param:
        - `user_id`: User id from the profile in which the comment will be
            added

        Body:
            - `from_user_id`: User id from the commentator
            - `mtbi`: personality from the commentator
            - `body`: Body of the comment
    """
    data = request.get_json()

    print("Validating JSON Schema...")
    try:
        validate(instance=data, schema=comment_schema)
    except jsonschema.exceptions.ValidationError as err:
        return make_response(
            {"ValidationError": err.message},
            HTTPStatus.BAD_REQUEST
        )

    # Add ObjectID to comment before inserting and initialize likes count
    data["id"] = str(bson.ObjectId())
    data["likes_count"] = 0

    # Insert data to MongoDB updating user document
    result = user_collection.update_one(
        {"_id": bson.ObjectId(user_id)},
        {"$push": {"comments": data}}
    )

    if result.matched_count == 0:
        return make_response(
            {"response": "user not found"},
            HTTPStatus.NOT_FOUND,
        )

    return make_response("", HTTPStatus.CREATED)


# Get comments endpoint
@app.route("/api/v1.0/user/<user_id>/comments", methods=["GET"])
def get_comments(user_id):
    """
        Endpoint that gets comments from a user profile.

        Params:
        - `user_id`: Id from the user's profile to get
        - `filter` (Optional): filter comments by personality. Example: `INTP`
        - `sort` (Optional): sort comment by:
            - `best`
            - `recent`
    """

    sort = request.args.get('sort')
    filter = request.args.get('filter')

    if not filter and not sort:
        # Return comments just as they are extracted
        user_data = user_collection.find_one({"_id": bson.ObjectId(user_id)})
        if user_data:
            return jsonify({"comments": user_data["comments"]})

    if filter:
        user_data = user_collection.find_one(
            {"_id": bson.ObjectId(user_id)},
            {"comments": {"$elemMatch": {"mbti": filter}}},
        )

        comments = user_data["comments"] if user_data else []

        return jsonify({"comments": comments})

    if sort and sort == 'best':
        pipeline = [
            {"$match": {"_id": bson.ObjectId(user_id)}},
            {"$unwind": "$comments"},
            {"$sort": {"comments.likes_count": -1}},
            {"$group": {"_id": "$_id", "comments": {"$push": "$comments"}}}
        ]
        user_data = user_collection.aggregate(pipeline)
        comments = list(user_data)[0]["comments"] if user_data else []

        return jsonify({"comments": comments})

    elif sort and sort == "recent":
        pipeline = [
            {"$match": {"_id": bson.ObjectId(user_id)}},
            {"$unwind": "$comments"},
            {"$sort": {"comments.id": -1}},
            {"$group": {"_id": "$_id", "comments": {"$push": "$comments"}}}
        ]
        user_data = user_collection.aggregate(pipeline)
        comments = list(user_data)[0]["comments"] if user_data else []

        return jsonify({"comments": comments})

    return make_response({})


# Like comment endpoint
@app.route("/api/v1.0/user/<user_id>/comment/<comment_id>", methods=["POST"])
def like_comment(user_id, comment_id):
    """
        Endpoint that adds a new like structure to a comment and
        increases the likes count

        Body:
        - `from_user_id`: user who makes the like
    """

    data = request.get_json()

    print("Validating JSON Schema...")
    try:
        validate(instance=data, schema=like_schema)
    except jsonschema.exceptions.ValidationError as err:
        return make_response(
            {"ValidationError": err.message},
            HTTPStatus.BAD_REQUEST
        )

    # Get comment likes and increment count
    user_data = user_collection.find_one(
        {"_id": bson.ObjectId(user_id)},
        {"comments": {"$elemMatch": {"id": comment_id}}},
    )

    if "comments" not in user_data:
        return make_response(
            {"response": "comment not found"},
            HTTPStatus.NOT_FOUND,
        )

    liked_user_dict = {"from_user_id": data["from_user_id"]}

    # Validate if user has already liked the comment
    if ("likes" in user_data["comments"][0]) and \
            (liked_user_dict in user_data["comments"][0]["likes"]):
        return make_response(
            {"response": "user has already liked comment"},
            HTTPStatus.OK,
        )

    # Insert data to MongoDB updating user document
    result = user_collection.update_one(
        {
            "_id": bson.ObjectId(user_id),
            "comments.id": comment_id,
        },
        {
            "$inc": {"comments.$.likes_count": 1},
            "$push": {
                "comments.$.likes": {"from_user_id": data["from_user_id"]},
            },
        },
    )

    if result.matched_count == 0:
        return make_response(
            {"response": "user or comment not found"},
            HTTPStatus.NOT_FOUND,
        )

    return make_response("", HTTPStatus.CREATED)


# Unlike comment endpoint
@app.route("/api/v1.0/user/<user_id>/comment/<comment_id>", methods=["DELETE"])
def unlike_comment(user_id, comment_id):
    """
        Endpoint that removes a like structure from a comment and
        decreases the likes count

        Body:
        - `from_user_id`: user who is unliking the comment
    """

    data = request.get_json()

    print("Validating JSON Schema...")
    try:
        validate(instance=data, schema=like_schema)
    except jsonschema.exceptions.ValidationError as err:
        return make_response(
            {"ValidationError": err.message},
            HTTPStatus.BAD_REQUEST
        )

    # Get comment likes and decrement count
    user_data = user_collection.find_one(
        {"_id": bson.ObjectId(user_id)},
        {"comments": {"$elemMatch": {"id": comment_id}}},
    )

    if "comments" not in user_data:
        return make_response(
            {"response": "comment not found"},
            HTTPStatus.NOT_FOUND,
        )

    # Insert data to MongoDB updating user document
    result = user_collection.update_one(
        {
            "_id": bson.ObjectId(user_id),
            "comments.id": comment_id,
        },
        {
            "$inc": {"comments.$.likes_count": -1},
            "$pull": {
                "comments.$.likes": {"from_user_id": data["from_user_id"]},
            },
        },
    )

    if result.matched_count == 0:
        return make_response(
            {"response": "no changes made"},
            HTTPStatus.OK,
        )

    return make_response("", HTTPStatus.OK)


if __name__ == "__main__":
    app.run(port=8000, debug=True)

    print("\nClosing MongoDB connection...")
    client.close()

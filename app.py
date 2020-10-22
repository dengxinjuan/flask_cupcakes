"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template,flash,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db,Cupcake,connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "YOUTELLMELASTSUMMER!"
debug = DebugToolbarExtension(app)




@app.route("/api/cupcakes")
def list_allcupcakes():
    """give the list of cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes = serialized)

@app.route("/api/cupcakes/<int:cupcake_id>")
def list_cupcakebyid(cupcake_id):
    """list single cupcake by id or return 404"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    a = cupcake.serialize()
    return jsonify(cupcake = a)

@app.route("/api/cupcakes",methods=["POST"])
def create_cupcake():
    """create a cupcake"""
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor,size=size,rating=rating,image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    a = new_cupcake.serialize()

    return (jsonify(cupcake=a),201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """update single cupcake by id or return 404"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"] or None

    db.session.add(cupcake)
    db.session.commit()

    a = cupcake.serialize()

    return jsonify(cupcake = a)



@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """delete a cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")



#### define the frontend from here

@app.route("/")
def homepage():
    return render_template("homepage.html")
    
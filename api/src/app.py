from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import os

load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'secret-key'

db.init_app(app)
Migrate(app, db)
CORS(app)

cloudinary.config( 
  cloud_name = os.getenv("CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET"),
  secure = True
)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():

    #username = request.json.get("username")
    #password = request.json.get("password")
    #avatar = request.json.get("avatar")

    username = request.form["username"]
    password = request.form["password"]
    avatar = request.files["avatar"]
    cv = request.files["cv"]

    user = User.query.filter_by(username=username).first()

    if user: return jsonify({ "error": "Username ya existe"}), 400

    """ 
    upload_avatar = cloudinary.uploader.upload(avatar, 
        folder="avatars",
        public_id=username+"_"+avatar.filename,
        overwrite=True,
        resource_type="image"
    ) 
    """

    upload_cv = cloudinary.uploader.upload(cv, 
        folder="cv",
        public_id=username+"_"+cv.filename,
        overwrite=True,
        resource_type="raw"
    )
 
    user = User()
    user.username = username
    user.password = password
    user.assign_avatar(avatar)
    user.cv = upload_cv["url"]

    user.save()

    return jsonify(user.serialize()), 201

    #return jsonify({ "form": request.form, "avatar": avatar.filename, "cv": cv.filename, "upload": upload })



if __name__ == '__main__':
    app.run()
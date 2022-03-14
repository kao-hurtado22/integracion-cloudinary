from flask_sqlalchemy import SQLAlchemy
import cloudinary
import cloudinary.uploader
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    avatar = db.Column(db.String(120), default="")
    cv = db.Column(db.String(120), default="")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "avatar": self.avatar,
            "cv": self.cv
        }

    def save(self):
        db.session.add(self)
        db.session.commit()    

    def update(self):
        db.session.commit()    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def assign_avatar(self, avatar):
        upload_avatar = cloudinary.uploader.upload(avatar, 
            folder="avatars",
            public_id=self.username+"_"+avatar.filename,
            overwrite=True,
            resource_type="image"
        )

        self.avatar = upload_avatar['secure_url']
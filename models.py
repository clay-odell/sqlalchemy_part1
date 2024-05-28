from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User (db.Model):
    """User"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement= True)
    first_name = db.Column(db.String(50),
                           nullable = False)
    last_name = db.Column(db.String(50),
                          nullable =False)
    image_URL = db.Column(db.String (150),
                          nullable = True,
                          default = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')
    
    def __repr__(self):
        u = self
        return f"<User {u.id} {u.first_name}{u.lastname}{u.image_url}>"

    

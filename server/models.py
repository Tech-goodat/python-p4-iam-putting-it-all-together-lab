from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__='users'

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, unique=True)
    _password_hash=db.Column(db.String, nullable=False)
    image_url=db.Column(db.String)
    bio=db.Column(db.String)

    instructions=db.relationship('Recipe', back_populates=("recipe"))
    

    def __init__(self, username, password):
        self.username=username
        self.password=password

    def password(self):
        raise AttributeError('password hash is not readable')
    def password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Recipe(db.Model, SerializerMixin):
    __tablename__='recipe'

    id=db.Column(db.String, primary_key=True)
    title=db.Column(db.String(255), nullable=False)
    instructions=db.Column(db.Text, nullable=False)
    minutes_to_complete=db.Column(db.Integer)

   
    
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe=db.relationship('User', back_populates='instructions')


    def __init__(self, title, instructions):
        self.title=title
        self.instructions=instructions

    def validate_instructions(cls, instructions):
        if len(instructions) <50:
            raise ValueError("Instructions must be atleast 50 characters")



    
   
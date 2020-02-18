from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String


app = Flask(__name__)
db_type = 'postgresql'
username = 'postgres'
password = 'secret123'
server = 'localhost'
port = '5432'
db_name = 'postgres'

app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_type}://' \
                                        f'{username}:{password}@' \
                                        f'{server}:{port}/' \
                                        f'{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<User {self.id}, {self.name}>'


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    vid = db.Column(db.Integer, primary_key=True)
    vmake = db.Column(db.String(), nullable=False)
    vmodel = db.Column(db.String(), nullable=False)
    oid = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Vehicle ID: {self.vid},' \
               f'Vehicle Make: {self.vmake},' \
               f'Vehicle Model: {self.vmodel}>' \
               f'Owner ID: {self.oid}>'


db.create_all()

# vQuery = db.session.query(Vehicle)
# uQuery = db.session.query(User)


@app.route('/')
def index():
    # join = uQuery.join('vehicles')
    vehicle = Vehicle.query.first()
    return vehicle.vmodel


if __name__ == '__main__':
    app.run()

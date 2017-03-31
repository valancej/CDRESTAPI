import ConfigParser
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, current_app

application = Flask(__name__)

# Read config file
config = ConfigParser.ConfigParser()
config.read('doctorReview_db.conf')

# MySQL configurations
with application.app_context():
    print current_app.name
    application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + config.get('DB', 'user') + \
    ':' + config.get('DB', 'password') + '@' + \
    config.get('DB', 'host') + '/' + config.get('DB', 'db')
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    mysql = SQLAlchemy()

# map models
class Doctors(mysql.Model):
    __tablename__ = 'doctors'
    id = mysql.Column(mysql.Integer, primary_key=True)
    name = mysql.Column(mysql.String(128), nullable=False)

class Reviews(mysql.Model):
    __tablename__ = 'reviews'
    id = mysql.Column(mysql.Integer, primary_key=True)
    doctorId = mysql.Column(mysql.Integer, nullable=False)
    description = mysql.Column(mysql.Text, nullable=False)


### Create a Doctor

@application.route('/doctors', methods=['POST'])
def createDoctor():

    mysql.init_app(application)
    # fetch name from the request
    name = request.get_json()["name"]

    doctor = Doctors(name=name) #prepare query statement

    curr_session = mysql.session #open database session
    try:
        curr_session.add(doctor) #add prepared statment to opened session
        curr_session.commit() #commit changes
    except:
        curr_session.rollback()
        curr_session.flush() # for resetting non-commited .add()

    doctorId = doctor.id #fetch last inserted id
    data = Doctors.query.filter_by(id=doctorId).first() #fetch our inserted doctor

    config.read('rating_db.conf')

    result = [data.name] #prepare data

    return jsonify(session=result)


### Show All Doctors
@application.route('/doctors', methods=['GET'])
def getDoctors():
    mysql.init_app(application)

    data = Doctors.query.all() #fetch all doctors

    data_all = []

    for doctor in data:
        data_all.append([doctor.id, doctor.name]) #prepare data

    return jsonify(doctors=data_all)


### Get specific Doctor and all reviews
@application.route('/doctors/<int:doctorId>', methods=['GET'])
def getDoctor(doctorId):
    mysql.init_app(application)

    curr_session = mysql.session #initiate database session

    data = Doctors.query.filter_by(id=doctorId)
    reviewData = Reviews.query.filter_by(doctorId=doctorId)

    data_all = []
    reviewData_all = []


    for doctor in data:
        data_all.append([doctor.id, doctor.name]) #prepare data

    for review in reviewData:
        reviewData_all.append([review.id, review.doctorId, review.description]) #prepare data


    return jsonify(name=doctor.name, id=doctor.id, reviews=reviewData_all)



### Add review to existing doctor
@application.route('/doctors/<int:doctorId>/reviews', methods=['POST'])
def createDoctorReview(doctorId):
    mysql.init_app(application)

    description = request.get_json()["description"]


    review = Reviews(description=description, doctorId=doctorId) #prepare query statement

    curr_session = mysql.session #open database session
    try:
        curr_session.add(review) #add prepared statment to opened session
        curr_session.commit() #commit changes
    except:
        curr_session.rollback()
        curr_session.flush() # for resetting non-commited .add()

    reviewId = review.id #fetch last inserted id
    data = Reviews.query.filter_by(id=reviewId).first() #fetch our inserted review

    config.read('doctorReview_db.conf')

    result = [data.description] #prepare data

    return jsonify(session=result)




### Delete a Doctor

@application.route('/doctors/<int:doctorId>', methods=['DELETE'])
def deleteDoctor(doctorId):
    mysql.init_app(application)


    curr_session = mysql.session #initiate database session

    Doctors.query.filter_by(id=doctorId).delete() #find the doctor by id and delete
    curr_session.commit() #commit changes to the database

    return getDoctors() #return all doctors


### Delete a specific review for specific dctor

@application.route('/doctors/<int:doctorId>/reviews/<int:reviewId>', methods=['DELETE'])
def deleteReviewForDoctor(reviewId, doctorId):
    mysql.init_app(application)


    curr_session = mysql.session #initiate database session

    Reviews.query.filter_by(id=reviewId, doctorId=doctorId).delete() #find the doctor by id and delete
    curr_session.commit() #commit changes to the database

    return getDoctor(doctorId)



if __name__ == "__main__":
    application.run()

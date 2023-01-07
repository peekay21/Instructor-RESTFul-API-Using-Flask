from flask import Flask
from models import db
from flask_restful import Resource,Api
from flask_restful import fields, marshal_with, reqparse
from models import Instructor
import os
from validation import NotFoundError, BusinessValidationError
app = None
api = None
def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///temp.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app, api

app, api = create_app()

# Import all the controllers so they are loaded


get_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'dept_name': fields.String,
    'salary': fields.Integer
}

create_parser = reqparse.RequestParser()
create_parser.add_argument('name')
create_parser.add_argument('dept_name')
create_parser.add_argument('salary')

#Add all restful api
class InstructorAPI(Resource):
    @marshal_with(get_fields)
    def get(self, name):
        user = db.session.query(Instructor).filter(Instructor.name == name).first()
        if user:
            return user, 200
        else:
            raise NotFoundError(status_code = 404)
    @marshal_with(get_fields)
    def put(self, name):
        user = db.session.query(Instructor).filter(Instructor.name == name).first()

        if user:
            args = create_parser.parse_args()
            dept_name = args.get('dept_name', None)
            salary = args.get('salary', None)
            if dept_name not in ['EE', 'CSE', 'IT', 'CE', 'ECE']:
                raise BusinessValidationError(status_code= 404, 
                                                error_code = 'BL1003', 
                                                error_message ='dept_name is not allowed')

            

            if dept_name is not None:
                user.dept_name = dept_name
            if salary is not None:
                try:
                    salary = int(salary)
                except:
                    raise BusinessValidationError(status_code= 404, 
                                                error_code = 'BL1007', 
                                                error_message ='Salary should be Integer value')
                if salary <=0:
                    raise BusinessValidationError(status_code= 404, 
                                                error_code = 'BL1006', 
                                                error_message ='Salary should be positive')
                else:
                    user.salary = salary 

            db.session.commit()
            updateduser = db.session.query(Instructor).filter(Instructor.name == name).first()
            return updateduser, 200
        else:
            raise NotFoundError(status_code = 404)
        

    def delete(self, name):

        user = db.session.query(Instructor).filter(Instructor.name == name).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return '', 204

        else:
            raise NotFoundError(status_code = 404)


    @marshal_with(get_fields)
    def post(self):

        args = create_parser.parse_args()
        name = args.get('name', None)
        dept_name = args.get('dept_name', None)
        salary = args.get('salary', None)
        
        if name is None:
            raise BusinessValidationError(status_code= 404, error_code = 'BL1001', error_message ='name is required')
        if dept_name is None:
            raise BusinessValidationError(status_code= 404, error_code = 'BL1002', error_message ='dept_name is required')
        if dept_name not in ['EE', 'CSE', 'IT', 'CE', 'ECE']:
            raise BusinessValidationError(status_code= 404, error_code = 'BL1003', error_message ='dept_name is not allowed')

        if salary is None:
            raise BusinessValidationError(status_code= 404, error_code = 'BL1005', error_message ='salary is required')
        
        else:

            try:
                salary = int(salary)
            except:
                raise BusinessValidationError(status_code= 404, 
                                                error_code = 'BL1007', 
                                                error_message ='Salary should be Integer value')
            if salary <=0:
                raise BusinessValidationError(status_code= 404, 
                                                error_code = 'BL1006', 
                                                error_message ='Salary should be positive')

        checkuser = db.session.query(Instructor).filter(Instructor.name == name).first()
        if checkuser:
            raise BusinessValidationError(status_code= 404, error_code = 'BL1004', error_message ='Duplicate User')

        newinstructor = Instructor(name = name, dept_name = dept_name, salary = salary)
        db.session.add(newinstructor)
        db.session.commit()

        findnewinstructor = db.session.query(Instructor).filter(Instructor.name == name).first()

        return findnewinstructor, 200




api.add_resource(InstructorAPI, "/api/instructor/<string:name>", "/api/instructor/")


if __name__ == '__main__':
  # Run the Flask app
  app.run(host='127.0.0.1',port=5000, debug = True)
from flask import Flask, escape, request, abort
from pprint import pprint

app = Flask(__name__)

# fun with non thread safety!
students_by_id = {}
classes_by_id = {}
next_student_id = 0
next_class_id = 0

@app.route('/students', methods=['POST', 'GET'])
def students():
    global students_by_id, next_student_id
    if request.method == 'POST':
        student = request.json
        student['id'] = next_student_id
        students_by_id[next_student_id] = student
        next_student_id += 1
        return student, 201
    else:
        return students_by_id
@app.route('/students/<id>', methods=['GET'])
def student(id):
    global students_by_id
    if int(id) in students_by_id:
        return students_by_id[int(id)]
    else:
        abort(404, description='No such class ' + str(id))

@app.route('/classes', methods=['POST', 'GET'])
def classes():
    global classes_by_id, next_class_id
    if request.method == 'POST':
        my_class = request.json
        my_class['id'] = next_class_id
        my_class['students'] = []
        classes_by_id[next_class_id] = my_class
        next_class_id += 1
        return my_class
    else:
        return classes_by_id

@app.route('/classes/<id>', methods=['GET', 'PATCH'])
def a_class(id):
    global classes_by_id
    if int(id) not in classes_by_id:
        abort(404, description="No such class " + str(id))
    if request.method == 'GET':
        return classes_by_id[int(id)]           
    else:
        student_id = request.json['student_id']
        classes_by_id[int(id)]['students'].append(students_by_id.get(student_id))
        return classes_by_id[int(id)]
        
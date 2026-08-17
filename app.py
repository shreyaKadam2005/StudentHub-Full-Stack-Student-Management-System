from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root@123'
app.config['MYSQL_DB'] = 'mydatabase'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  #to get data in dictionary format
CORS(app)  #now flask can accept requests from any front end
mydb = MySQL(app)
print("connected to database")

#getting all students
@app.route('/students', methods=['GET'])
def get_students():
    mycur = mydb.connection.cursor()
    mycur.execute("select * from students")
    students = mycur.fetchall()
    return jsonify(students)

#getting a single student
@app.route('/students/<int:rn>', methods=['GET'])
def search_student(rn):
    mycur = mydb.connection.cursor()
    mycur.execute("select * from students where rollno= "+str(rn))
    stud = mycur.fetchone()

    if stud:
        return jsonify(stud)
    return jsonify({"message": "Student not found"}), 404

#inserting new student
@app.route('/students', methods=['POST'])
def add_student():
    mycur=mydb.connection.cursor()
    ns=request.get_json()
    if not ns:
        return jsonify({"message": "data not provided"}), 400

    n=ns["fullname"]
    m=ns["mobileno"]
    c=ns["city"]
    p=ns["per"]

    mycur.execute("insert into students(fullname,mobileno,city,per) values(%s,%s,%s,%s)",(n,m,c,p))
    mydb.connection.commit()
    if(mycur.rowcount>0):
        return jsonify({"message": "Student added successfully"}), 201
    else:
        return jsonify({"message": "Problem occurred"}),400


#update student
@app.route('/students/<int:rn>', methods=['PUT'])
def update_student(rn):
    mycur=mydb.connection.cursor()
    mycur.execute("select * from students where rollno= "+str(rn))
    stud = mycur.fetchall()

    if not stud:
        return jsonify({"message": "Student not found"}), 404

    ns=request.get_json()
    n=ns["fullname"]
    m=ns["mobileno"]
    c=ns["city"]
    p=ns["per"]

    mycur.execute("update students set fullname=%s,mobileno=%s,city=%s,per=%s where rollno=%s",(n,m,c,p,rn))
    mydb.connection.commit()
    if(mycur.rowcount>0):
        return jsonify({"message": "Student updated successfully"}), 200
    else:
        return jsonify({"message": "Problem occurred"}),400

#delete student
@app.route('/students/<int:rn>', methods=['DELETE'])
def delete_students(rn):
    mycur=mydb.connection.cursor()
    mycur.execute("select * from students where rollno= "+str(rn))
    stud = mycur.fetchall()
    if not stud:
        return jsonify({"message": "Student not found"}), 404

    mycur.execute("delete from students where rollno=%s",(rn,))
    mydb.connection.commit()
    if(mycur.rowcount>0):
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        return jsonify({"message": "Problem occurred"}),400


app.run(debug=True)


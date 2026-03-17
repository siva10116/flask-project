from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student table model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    course = db.Column(db.String(100))
    email = db.Column(db.String(100))


# Home page - show students
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


# Add student
@app.route('/add', methods=['GET','POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name']
        course = request.form['course']
        email = request.form['email']

        new_student = Student(name=name, course=course, email=email)

        db.session.add(new_student)
        db.session.commit()

        return redirect('/')

    return render_template('add.html')


# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):

    student = Student.query.get(id)

    db.session.delete(student)
    db.session.commit()

    return redirect('/')


# Update student
@app.route('/update/<int:id>', methods=['GET','POST'])
def update_student(id):

    student = Student.query.get(id)

    if request.method == 'POST':

        student.name = request.form['name']
        student.course = request.form['course']
        student.email = request.form['email']

        db.session.commit()

        return redirect('/')

    return render_template('update.html', student=student)


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
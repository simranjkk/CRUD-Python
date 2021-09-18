from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    days = db.Column(db.String(100))

    def __init__(self, job_title, company, location,salary,days):
        self.job_title = job_title
        self.location = location
        self.company = company
        self.salary= salary
        self.days = days


# This is the index route where we are going to
# query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees=all_data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        job_title = request.form['job_title']
        location = request.form['location']
        salary = request.form['salary']
        days = request.form['days']
        company = request.form['company']

        my_data = Data(job_title, company, location,salary,days)
        db.session.add(my_data)
        db.session.commit()

        flash("Job Inserted Successfully")

        return redirect(url_for('Index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.job_title = request.form['job_title']
        my_data.company = request.form['company']
        my_data.salary = request.form['salary']
        my_data.location = request.form['location']
        my_data.days = request.form['days']

        db.session.commit()
        flash("Job listing Updated Successfully")

        return redirect(url_for('Index'))


# This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Job listing Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
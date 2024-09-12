from flask import Flask, render_template, request 
import sqlite3 

app = Flask(__name__, template_folder="templates")

@app.route('/') 
@app.route('/home') 
def index(): 
	return render_template('home.html') 


connect = sqlite3.connect('database.db') 
connect.execute('CREATE TABLE IF NOT EXISTS USERS (id UNIQUE PRIMARY KEY NOT NULL, name TEXT, email TEXT, phone TEXT)')


@app.route('/add', methods=['GET', 'POST']) 
def add(): 
	if request.method == 'POST': 
		id = request.form['id'] 
		name = request.form['name'] 
		email = request.form['email'] 
		phone = request.form['phone'] 
	
		with sqlite3.connect("database.db") as users: 
			cursor = users.cursor() 
			exists = cursor.execute('SELECT id FROM USERS WHERE id = ?',(id))
			if exists:
				return render_template('adduser.html',warn="User ID already Exists")
			cursor.execute("INSERT INTO USERS(id,name,email,phone) VALUES (?,?,?,?)", 
						(id, name, email, phone)) 
			users.commit() 
		return render_template("home.html") 
	else: 
		return render_template('adduser.html') 


@app.route('/users/<int:id>', methods=['DELETE'])
def delete(userid): 
	with sqlite3.connect("database.db") as users: 
		cursor = users.cursor() 
		cursor.execute("DELETE FROM USERS WHERE id= ?",(userid))
		users.commit() 
	return render_template("home.html") 



@app.route('/users') 
def users(): 
	connect = sqlite3.connect('database.db') 
	cursor = connect.cursor() 
	cursor.execute('SELECT * FROM USERS') 

	data = cursor.fetchall() 
	return render_template("users.html", data=data) 


if __name__ == '__main__': 
	app.run(debug=True) 

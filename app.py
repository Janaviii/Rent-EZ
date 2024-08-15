from flask import Flask, render_template, request, redirect, url_for, session
import re
from flask_mail import *  
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

#Flask mail configuration  
app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']= 465  
app.config['MAIL_USERNAME'] = 'janavimi28@gmail.com'  
app.config['MAIL_PASSWORD'] = 'pcxyezxlunhhcxuy'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  

#instantiate the Mail class  
mail = Mail(app)  

conn = sqlite3.connect('database_form.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                contact INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS payments
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                contact INTEGER,
                cardnumber INTEGER,
                expiration TEXT NOT NULL,
                cvv INTEGER, 
                product TEXT NOT NULL,
                count INTEGER,
                district TEXT NOT NULL)''')

conn.commit()
conn.close()

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html', name=session['user_name'])
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("Heyy")
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        conn = sqlite3.connect('database_form.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE name = ? ', (name,))
        a=cur.fetchone()
        if a:
            print("Janavi....")
            error = 'Username already exists !'
            return render_template('register.html', error=error)
        # Validate username
        if not re.match("^[a-zA-Z0-9_]*$", name):
            error = 'Invalid username. Only letters, numbers and underscore allowed.'
            return render_template('register.html', error=error)
        # Validate email
        if not re.match(r'^[\w-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            error = 'Invalid email address.'
            return render_template('register.html', error=error)
        # Validate password
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[a-zA-Z0-9]).{8,}$', password):
            return render_template('register.html', error='Invalid password! Must contain at least one lowercase letter, one digit, and be at least 8 characters long.')
        
        conn = sqlite3.connect('database_form.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name, email, password, contact) VALUES (?, ?, ?, ?)', (name, email, password, contact))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Hello")
    if request.method == 'POST':
        print("Hii")
        name = request.form['name']
        password = request.form['password']
        conn = sqlite3.connect('database_form.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE name = ? AND password = ?', (name, password))
        user = cur.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid name or password.')
    else:
        print("BYE")
        return render_template('login.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/prod1')
def prod1():
    return render_template('prod1.html')

@app.route('/prod2')
def prod2():
    return render_template('prod2.html')

@app.route('/prod3')
def prod3():
    return render_template('prod3.html')

@app.route('/prod4')
def prod4():
    return render_template('prod4.html')

@app.route('/prod5')
def prod5():
    return render_template('prod5.html')

@app.route('/prod6')
def prod6():
    return render_template('prod6.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        print("Heyy")
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        cardnumber = request.form['cardnumber']
        expiration = request.form['expiration']
        cvv = request.form['cvv']
        product = request.form['product']
        count = request.form['count']
        district = request.form['district']
        # Validate username
        if not re.match("^[a-zA-Z]*$", name):
            error = 'Invalid username. Only letters allowed.'
            return render_template('payment.html', error=error)
        # Validate email
        if not re.match(r'^[\w-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            error = 'Invalid email address.'
            return render_template('payment.html', error=error)
        conn = sqlite3.connect('database_form.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO payments (name, email, contact, cardnumber, expiration, cvv, product, count, district) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, email, contact, cardnumber, expiration, cvv, product, count, district))
        conn.commit()
        conn.close()
        print(float(product))
        converted_num=float(product)
        print(float(count))
        converted_count=float(count)
        
        if district=='jalgaon':
            msg = Message('Rent-EZ Payment Confirmation', sender = 'janavimi28@gmail.com', recipients=[email])  
            msg.body = ('Your payemnt is received👍\nTotal amount is Rs {}\nCollect the equipment from the below given address :📍\nShantinath complex,\nRing road,\nJalgaon,\n425001\nThank you for visiting our website🙏'.format(converted_num*converted_count))
            mail.send(msg)
        elif district=='ratnagiri':
            msg = Message('Rent-EZ Payment Confirmation', sender = 'janavimi28@gmail.com', recipients=[email])  
            msg.body = ('Your payemnt is received👍\nTotal amount is Rs {}\nCollect the equipment from the below given address :📍\nRamanand Nagar,\MJ College road,\nRatnagiri,\n415612\nThank you for visiting our website🙏'.format(converted_num*converted_count))
            mail.send(msg)
        elif district=='dhule':
            msg = Message('Rent-EZ Payment Confirmation', sender = 'janavimi28@gmail.com', recipients=[email])  
            msg.body = ('Your payemnt is received👍\nTotal amount is Rs {}\nCollect the equipment from the below given address :📍\nA/004,Tirupati Nagar,\nShani mandir road,\nDhule,\n424001\nThank you for visiting our website🙏'.format(converted_num*converted_count))
            mail.send(msg)
        elif district=='aurangabad':
            msg = Message('Rent-EZ Payment Confirmation', sender = 'janavimi28@gmail.com', recipients=[email])  
            msg.body = ('Your payemnt is received👍\nTotal amount is Rs {}\nCollect the equipment from the below given address :📍\nA/004,MJ complex,\nRam mandir road,\nAurangabad,\n431113\nThank you for visiting our website🙏'.format(converted_num*converted_count))
            mail.send(msg)
        
        print(converted_num)
        print(converted_count)
        print(converted_num*converted_count)
        total=converted_num*converted_count
    
        return render_template('confirmation.html',total=total)
    else:
        return render_template('payment.html')   

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

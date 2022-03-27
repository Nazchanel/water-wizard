from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'name' in session:
        name = session['name']
        return redirect('/dashboard')
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    file = r"C:\Users\python\PycharmProjects\Climate_Change\users.db"
    if request.method == 'POST':
        user_details = request.form
        name = user_details['name'].lower().strip()
        age = user_details['age'].lower().strip()
        # -----------------------------------------
        baths = int(user_details['baths'].lower().strip()) * 36
        teeth = int(user_details['teeth'].lower().strip()) * .5
        clothes = int(user_details['clothes'].lower().strip())
        hands = int(user_details['hands'].lower().strip()) * .5
        shaves = int(user_details['shaves'].lower().strip())
        showers = int(user_details['showers'].lower().strip()) * 3
        shower_length = int(user_details['sminutes'].lower().strip())
        shower = int(showers * shower_length) * 3
        flushes = int(user_details['flushes'].lower().strip()) * 2
        drink = int(user_details['drink'].lower().strip()) * 0.625
        dishes = int(user_details['dishes'].lower().strip()) * 10
        hand_washing = int(user_details['dishhands'].lower().strip()) * 15

        total_gallons = (baths + teeth + clothes + hands + shaves + shower + flushes + drink + dishes + hand_washing) / 1.5

        session['name'] = name
        con = sqlite3.connect(file)
        cur = con.cursor()
        # cur.execute("CREATE TABLE users (name TEXT, age INTEGER, gallon_amount INTEGER)")
        cur.execute("INSERT INTO users (name, age, gallon_amount) VALUES(?, ?, ?)", (name, age, total_gallons))
        con.commit()
        return render_template('dashboard.html', total_gallons=total_gallons)
    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('name', None)
    session.pop('email', None)
    session.pop('password', None)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    file = r"C:\Users\python\PycharmProjects\Climate_Change\users.db"
    if request.method == 'POST':
        user_details = request.form
        name = user_details['name'].lower().strip()
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute("SELECT name FROM users WHERE name=(?)", (name,))
        result = cur.fetchone()
        if result:
            print("hi")
            session['name'] = name
            con.commit()
            return redirect('/dashboard')

        else:
            session['name'] = name
            con.commit()
            print("bye")
            return redirect('/error')

    return render_template('login.html')


@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template('error.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'name' in session:
        name = session['name']
        return render_template('dashboard.html')
    else:
        return redirect('login.html')


@app.route('/ourmission', methods=['GET', 'POST'])
def mission():
    return render_template('ourmission.html')


if __name__ == "__main__":
    app.run(debug=True)

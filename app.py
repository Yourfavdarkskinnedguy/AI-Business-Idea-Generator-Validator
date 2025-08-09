from flask import Flask, render_template, request, session, url_for, redirect
from dotenv import load_dotenv
from supabase import create_client, Client
import os
from backend import generate_prompt

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)




app = Flask(__name__)

app.secret_key= 'jksbh'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method =='POST':
        email= request.form.get('email')
        password= request.form.get('password')

        try:
            response = supabase.auth.sign_in_with_password({"email": email,"password": password,})
        except Exception as e :
            print(f'error found in login is {e}')
            return render_template('login.html', message = e)
        return redirect(url_for('index'))
    

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method =='GET':
        return render_template('signup.html')
    
    elif request.method == 'POST':
        email= request.form.get('signup-email')
        password= request.form.get('signup-password')

        try:
            response = supabase.auth.sign_up({"email": email,"password": password,})
        except Exception as e:
            print(f'error found in signup is {e}')
            return 'error', 404

        return redirect(url_for('index'))



@app.route('/index', methods=['GET','POST'])
def index():
    if request.method =='GET':
        return render_template('index.html')

    elif request.method == 'POST':
        language= request.form.get('options')
        code= request.form.get('code')

        Explanation, Error, solution= generate_prompt(language, code)
        session['Explanation']= Explanation
        session['Error']= Error
        session['solution']= solution


        print(f'explanation is {Explanation}')
        print(f'Error is {Error}')
        print(f'solution is {solution}')

        

        return redirect(url_for('solution'))

@app.route('/solution', methods=['GET', 'POST'])
def solution():
    if request.method == 'GET':
        Explanation= session.get('Explanation')
        Error= session.get('Error')
        solution= session.get('solution')
        return render_template('mentor.html', Explanation=Explanation, Error=Error, Solution=solution)
    
    elif request.method =='POST':
        print(f'explantion check in solution is {Explanation}')
        return render_template('mentor.html', Explanation=Explanation, Error=Error, Solution=solution)




if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request , redirect , url_for , flash , session
import requests
import datetime
from collections import defaultdict
import os
import json
from Forms import SignupForm , LoginForm 
#from flask_sqlalchemy import SQLAlchemy
from transaction import transactions_bp 
from models import db, User , init_db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)

app.register_blueprint(transactions_bp)
from blogs.views import blog_bp
app.register_blueprint(blog_bp)

app.secret_key = "your_secret_key_here" 
# Add max and min functions to Jinja2 globals
app.jinja_env.globals.update(round=round, max=max, min=min)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["MAIL_SERVER"] = "smtp.gmail.com"  # For Gmail, use smtp.gmail.com
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "23226@iiitu.ac.in"  # Replace with your email
app.config["MAIL_PASSWORD"] = "gaup uryx cgaa kwpj"  # Use an App Password for security
mail = Mail(app)

init_db(app)
migrate = Migrate(app, db)

AGRO_API_KEY = os.getenv("AGRO_API_KEY", "c2339a94d63f41b15e4b9f88bc4d2ca6")
OWM_API_KEY = os.getenv("OWM_API_KEY", "f148a720d1babb96307fe315da46696e")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "mZ1aDkUKJMDjrdSH9Dk4R5DsHCpXx0B4ngnIqSRhX8NNEAspMlnKTqyU")

# Weather images mapping
weather_images = {
    "Clear": "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-weather/ilu2.webp",
    "Rain":  "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-weather/ilu1.webp",
    "Snow":  "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-weather/draw1.webp",
    "Clouds": "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-weather/draw2.webp",
}
 

@app.route("/")
@app.route("/home")
def index():   
    return render_template("index.html", title="Home")


@app.route("/generic")
def generic():
    if "user_name" not in session:
        flash("Login Required!")
        return redirect(url_for('login', next=request.url))
    else:
        flash(f"Hi {session['user_name']}, have a good day!")

    return render_template("generic.html", title="Generic")



@app.route("/weather", methods=["GET"])
def weather():
    if "user_name" not in session:
        flash("Login Required!")
        return redirect(url_for('login', next=request.url))
    
    city = request.args.get("city", "Ayodhya")

    if not city:
        return render_template("weather.html", error="Please enter a city name.")

    try:
        # Fetch latitude and longitude for the city
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OWM_API_KEY}"
        geo_response = requests.get(geo_url).json()

        if not geo_response:
            return render_template("weather.html", error="City not found. Please try again.")

        lat = geo_response[0]["lat"]
        lon = geo_response[0]["lon"]

        # Fetch weather forecast from Agromonitoring API
        agro_url1 = f"https://api.agromonitoring.com/agro/1.0/weather/forecast?lat={lat}&lon={lon}&appid={AGRO_API_KEY}"
        weather_response = requests.get(agro_url1).json()

        forecast = defaultdict(lambda: {"time": [], "temp": [], "feels_like": [], "humidity": [], "weather": [], "wind_speed": [] , "icon_url":[]})

        for entry in weather_response:
            dt_text = str(datetime.datetime.fromtimestamp(entry["dt"]))
            date_obj = datetime.datetime.strptime(dt_text.split()[0], "%Y-%m-%d")
            formatted_date = date_obj.strftime("%-d %b %Y") if hasattr(datetime, 'strftime') else date_obj.strftime("%#d %b %Y")
            time = dt_text.split()[1]
            icon_code = entry["weather"][0]["icon"]
            forecast[formatted_date]["time"].append(time)
            forecast[formatted_date]["temp"].append(round(entry["main"]["temp"] - 273.15, 2))  # Convert Kelvin to Celsius
            forecast[formatted_date]["feels_like"].append(round(entry["main"]["feels_like"] - 273.15, 2))
            forecast[formatted_date]["humidity"].append(entry["main"]["humidity"])
            forecast[formatted_date]["weather"].append(entry["weather"][0]["description"])
            forecast[formatted_date]["wind_speed"].append(round(entry["wind"]["speed"] * 18 / 5, 2))
            forecast[formatted_date]['icon_url'].append(f"https://openweathermap.org/img/wn/{icon_code}@2x.png")

        # Fetch current weather from Agromonitoring API
        agro_url2 = f"https://api.agromonitoring.com/agro/1.0/weather?lat={lat}&lon={lon}&appid={AGRO_API_KEY}"
        curr_weather_response = requests.get(agro_url2).json()

        timestamp = curr_weather_response["dt"]
        curr_time = datetime.datetime.fromtimestamp(timestamp)

        # Determine weather condition and corresponding image
        main_condition = curr_weather_response["weather"][0]["main"]
        image_url = weather_images.get(main_condition, weather_images["Clear"])

        # Fetch background image based on weather and time of day
        # shift = "morning" if curr_time.hour < 10 else "afternoon" if curr_time.hour < 16 else "sunset" if curr_time.hour < 18 else "evening"
        # query = f"nature {curr_weather_response['weather'][0]['description']} {shift}"
        # bg_url = get_background_image(query)

        # Pass data to the template
        return render_template(
            "weather.html",
            city=city.capitalize(),
            curr_weather_data=curr_weather_response,
            curr_time=curr_time,
            image_url=image_url,
            # backgrnd_url=bg_url,
            forecast=forecast,
        )

    except requests.exceptions.RequestException as e:
        return render_template("weather.html", error=f"Error fetching weather data: {str(e)}")
    except KeyError as e:
        return render_template("weather.html", error=f"Unexpected data format: {str(e)}")



@app.route("/login" , methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.is_submitted():
      print("Form was submitted.")
    if form.validate_on_submit():
       print("Form is valid.")
    else :
        print(form.errors)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password, form.password.data):  # Verify hashed password
            session["user_id"] = user.id  # Store user ID in session
            session["user_name"] = form.username.data  # Store username
            flash("Login successful!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("index"))
        
        flash("Invalid username or password", "error")
    
    return render_template("login.html",form = form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists! Please choose another.", "error")
            return redirect(url_for("signup"))
        
        # Create new user in the database
        new_user = User(
            username=form.username.data, 
            password=generate_password_hash(form.password.data),  # Hash password
            email=form.email.data
       )

        db.session.add(new_user)
        db.session.commit()
        session["user_name"] = form.username.data # Store username
        #session["user_id"] = user.id
        

        msg = Message("AgroAssist", 
                      sender="your_email@gmail.com", 
                      recipients=[new_user.email])
        msg.body = f"Hello {new_user.username},\n\nThank you for signing up for our platform!\n\nBest Regards,\nAgroAssist"
        try:
            mail.send(msg)
            print("Signup successful! A confirmation email has been sent.", "success")
        except Exception as e:
            print(f"Error sending email: {e}")
            

        flash("Signup successful! You can now log in.", "success")
        return redirect(url_for("login")) 
    
    return render_template("signup.html", form=form)



if __name__ == "__main__":
    app.run(debug=True)
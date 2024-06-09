from flask import (
    Flask,
    url_for,
    render_template,
    request,
    redirect,
    session,
    request,
    abort,
)
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask import request
import requests
import requests
from sqlalchemy import cast, Numeric
import time


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://quickassistdb_h5bg_user:BQTkvSdgb5vOnlJyuaFeth6YWihiQ9jN@dpg-cpiant4f7o1s73bf1c80-a.oregon-postgres.render.com/quickassistdb_h5bg"
)
# sklite:///test.db
# Second database -> postgres://quickassistdb_user:3ccCC6EM5CjGpDNd7AHTFhc6x7NgLU0l@dpg-cpcdkkm3e1ms73f7ufp0-a.ohio-postgres.render.com/quickassistdb
# Test Database -> postgresql://quickassist_745t_user:unpecgvQXpOvZ4xobjVNeeEwl7EXEXVH@dpg-cpbrihm3e1ms739b0o70-a.ohio-postgres.render.com/quickassist_745t
db = SQLAlchemy(app)


class login_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    ip_address = db.Column(db.String(80))
    sus = db.Column(db.Boolean)

    def __init__(self, username, password, ip_address, sus):
        self.username = username
        self.password = password
        self.ip_address = ip_address
        self.sus = sus


class responders_login_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class reference_number(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    user_called = db.Column(db.String(80))

    def __init__(self, number, user_called):
        self.number = number
        self.user_called = user_called


class location_and_emergency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    emergency = db.Column(db.String)
    level = db.Column(db.Integer)
    user = db.Column(db.String)
    time = db.Column(db.Float)

    def __init__(self, longitude, latitude, emergency, level, user, time):
        self.longitude = longitude
        self.latitude = latitude
        self.emergency = emergency
        self.level = level
        self.user = user
        self.time = time


class phone_numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)
    where = db.Column(db.String)

    def __init__(self, number, where):
        self.number = number
        self.where = where


def get_state(lat, lng):
    response = requests.get(
        f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key=AIzaSyAhGURYDl089JjSC-xBtgfjQ3QhP8UNg9k"
    )
    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        for component in data["results"][0]["address_components"]:
            if "administrative_area_level_1" in component["types"]:
                return component["long_name"]
    return None


def get_location():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAhGURYDl089JjSC-xBtgfjQ3QhP8UNg9k"
    try:
        response = requests.post(url)
        data = response.json()
        if response.status_code == 200:
            latitude = data["location"]["lat"]
            longitude = data["location"]["lng"]

            url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key=AIzaSyAhGURYDl089JjSC-xBtgfjQ3QhP8UNg9k"
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200 and data["status"] == "OK":
                results = data["results"]
                if results:
                    road_name = results[0]["formatted_address"]
                    print("Road Name:", road_name)
                else:
                    print("No results found.")
            else:
                print("Error:", data["status"])
        else:
            print("Error:", response.status_code)
    except Exception as e:
        print("Error:", e)

    return road_name, longitude, latitude


@app.route("/", methods=["GET", "POST"])
def home():

    session["report_user"] = None
    if session.get("logged_in") == None:
        session["logged_in"] = False

    if session.get("r_logged_in") == None:
        session["r_logged_in"] = False

    if not session.get("logged_in") or not session.get("r_logged_in"):
        if request.method == "POST":
            reference = request.form.get("reference")
            report = request.form.get("report")
            try:
                if reference is not None and reference[:3] == "QA-":
                    new_reference = reference.split("-")[1]
                    search = reference_number.query.filter_by(
                        number=f"{new_reference}"
                    ).first()
                    session["report_user"] = search.user_called
                    return render_template("index.html")

                else:
                    print("Error")
                    return redirect(url_for("error"))

                """
                if report is not None:
                    print('JADSFKASFLKSDFAJSLDFJASDKLFLAJASDKFJALSKJ' +  session['report_user'])
                    user = login_info.query.filter_by(username=session['report_user']).first()
                    
                    if user:
                        user.sus = True
                        db.session.commit()
                    else:
                        print('else')
                        
                    print(user)    
                    print(f'User is SUS???? {user.sus}')
                    return render_template('report.html')
                """

            except:
                print("Error")
                redirect(url_for("error"))

        else:
            print("NOOOOO")
            return render_template("index.html")

    else:
        if request.method == "GET":
            username = session.get("username")
            return render_template("index.html", username=username)


@app.route("/inclogin")
def inclogin():
    return render_template("wronglogin.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        name = request.form["username"]
        passw = request.form["password"]
        print(name, passw)
        try:
            data = login_info.query.filter_by(username=name, password=passw).first()

            print(data)

            if data is not None:
                session["logged_in"] = True
                session["username"] = name
                return redirect(url_for("home"))
            else:
                print(data)
                return redirect(url_for("inclogin"))

        except:
            print("except")
            return redirect(url_for("inclogin"))


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        ip_address = request.environ["REMOTE_ADDR"]
        print(ip_address)

        if (
            login_info.query.filter_by(username=request.form["username"]).first()
            == None
        ):
            new_user = login_info(
                username=request.form["username"],
                password=request.form["password"],
                ip_address=ip_address,
                sus=False,
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            return render_template("already_registered.html")
    if request.method == "GET":
        return render_template("register.html")


@app.route("/logout")
def logout():
    session["logged_in"] = False
    session["r_logged_in"] = False
    return redirect(url_for("home"))


@app.route("/emergency", methods=["GET", "POST"])
def emergency():
    if request.method == "GET":
        type = request.args.get("type")
        print(type)
        return render_template("emergency.html", type=type, abort=abort)


@app.route("/call", methods=["GET", "POST"])
def call():

    user_loc = get_location()

    type = request.args.get("type")
    severity = request.args.get("severity")

    try:
        if type == None or severity == None:
            abort(403)
        if session["username"] == None or session["logged_in"] == False:
            print("YIPEEE")
    except:
        abort(403)

    # only for faulty traffic light
    type = type.replace("-", " ")

    print(type)
    print(severity)

    emr_lst = ["low", "medium", "high", "critical"]

    emr_level = emr_lst[int(severity) - 1]

    # ascending_numbers = reference_number.query.order_by(reference_number.number.asc()).all()

    # descending_numbers = reference_number.query.order_by(reference_number.number.desc()).all()

    first_number = reference_number.query.order_by(
        reference_number.number.desc()
    ).first()
    print(first_number)
    try:
        ref_num = int(first_number.number)
        print(ref_num)
    except:
        first_num = reference_number(number=1, user_called=session["username"])
        db.session.add(first_num)
        db.session.commit()
    else:
        ref_num += 1
        print(f"num -> {ref_num}")
        first_num = reference_number(number=ref_num, user_called=session["username"])
        db.session.add(first_num)
        db.session.commit()

    def api_call(lat, lng):
        key = "10d459c7-a343-435f-af44-e0dff185d8fe"
        secret = "SuQdYrMy+02Fs/4Stg4QrQ=="
        from_number = "+12085689261"
        locale = "en-US"
        url = "https://calling.api.sinch.com/calling/v1/callouts"
        print(get_state(lat, lng))
        num = phone_numbers.query.filter_by(where=get_state(lat, lng)).first()

        print(" ->>>>>>>>>>>>>>>>>>>>>>" + num.number, get_state(lat, lng))

        payload = {
            "method": "ttsCallout",
            "ttsCallout": {
                "cli": from_number,
                "destination": {
                    "type": "number",
                    "endpoint": "+17329264484",  # should be 911 but yk you can't call them
                },
                "locale": locale,
                "text": f"Hello, the user found a {type}. this is a {emr_level} emergency. The location is {user_loc[0]}. I repeat, {user_loc[0]}.  If there are any issues, use the reference number: QA-{ref_num} on our website, QuickAssist. Thank you.",
            },
        }

        payload2 = {
            "method": "ttsCallout",
            "ttsCallout": {
                "cli": from_number,
                "destination": {"type": "number", "endpoint": num.number},
                "locale": locale,
                "text": f"Hello, the user found a {type}. this is a {emr_level} emergency. The location is {user_loc[0]}. I repeat, {user_loc[0]}.  If there are any issues, use the reference number: QA-{ref_num} on our website, QuickAssist. Thank you.",
            },
        }

        headers = {"Content-Type": "application/json"}
        if int(severity) >= 3 or type == "crash":
            response = requests.post(
                url, json=payload, headers=headers, auth=(key, secret)
            )
            data = response.json()
            print("Police called.")
        else:
            response = requests.post(
                url, json=payload2, headers=headers, auth=(key, secret)
            )
            data = response.json()
            print("DOT called.")

    sus_user = login_info.query.filter_by(username=session["username"]).first()
    if sus_user.sus == True:
        sus_loc = location_and_emergency(
            longitude=user_loc[1],
            latitude=user_loc[2],
            emergency=type,
            level=int(severity),
            user=session["username"],
            time=time.time(),
        )
        db.session.add(sus_loc)
        db.session.commit()

        return render_template("user_warning.html")
    else:
        api_call(user_loc[2], user_loc[1])
        # Call once final version is ready
        # uses credits

        print(user_loc[1], user_loc[2])
        """
        Distance between 2 points
        
        lat1 = radians(user_loc[1])
        lon1 = radians(user_loc[2])
        lat2 = radians(user_loc[1] + 0.001)
        lon2 = radians(user_loc[2] + 0.001)
    
        
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = 6373.0 * c

        print("Result: ", distance)      
        
        states = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

        for state in states:
            statess = phone_numbers(number='+17329264484', where=state)
            db.session.add(statess)
            db.session.commit()
        """

        similar_locations = location_and_emergency.query.filter(
            cast(location_and_emergency.longitude, Numeric).between(
                user_loc[1] - 0.01, user_loc[1] + 0.01
            ),
            cast(location_and_emergency.latitude, Numeric).between(
                user_loc[2] - 0.01, user_loc[2] + 0.01
            ),
            cast(location_and_emergency.time, Numeric).between(
                time.time() - 3600, time.time() + 3600
            ),
        ).all()

        for location in similar_locations:
            print(
                f"Similar location found: Longitude={location.longitude}, Latitude={location.latitude}, User={location.user}"
            )
            user = login_info.query.filter_by(username=location.user).first()

            print(location.emergency, type, location.level, severity, user.sus)

            if (
                location.emergency == type
                and location.level == int(severity)
                and user.sus == True
                and location.user != session["username"]
            ):
                user.sus = False
                db.session.commit()
                print("User is no longer SUS")
            """
            if user.sus == True:
                user.sus=False
                db.session.commit()
                print('User is no longer SUS')    
            """

        # -74.3702528, 40.5798912
        loc = location_and_emergency(
            longitude=user_loc[1],
            latitude=user_loc[2],
            emergency=type,
            level=int(severity),
            user=session["username"],
            time=time.time(),
        )
        db.session.add(loc)
        db.session.commit()

        """
        new_user = responders_login_info(username='responder1', password='password')
        db.session.add(new_user)
        db.session.commit()  

        """
        return render_template("call.html", type=type, severity=severity)


@app.route("/responders", methods=["GET", "POST"])
def responders_login():

    if request.method == "GET":
        return render_template("responders.html")
    else:
        names = request.form["username"]
        passw = request.form["password"]
        try:
            data = responders_login_info.query.filter_by(
                username=names, password=passw
            ).first()

            if data is not None:
                session["r_logged_in"] = True
                session["r_username"] = names
                return redirect(url_for("home"))
            else:
                return redirect(url_for("inclogin"))
        except:
            return redirect(url_for("inclogin"))


@app.route("/error", methods=["POST"])
def error():
    if request.method == "POST":
        return render_template("error.html")
    abort(405)


@app.route("/report", methods=["POST"])
def report():
    user = login_info.query.filter_by(username="ved").first()

    if user:
        user.sus = True
        db.session.commit()

        print("Changed")

    return render_template("report.html")


@app.errorhandler(405)
def _405(e):
    return render_template("405.html")


@app.errorhandler(404)
def _404(e):
    return render_template("404.html")


@app.errorhandler(403)
def _403(e):
    return render_template("403.html")


if __name__ == "__main__":
    app.debug = True
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)

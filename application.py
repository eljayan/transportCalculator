import os, sys
import pythoncom
import calculator
from sqlite3 import connect
from flask import Flask, render_template,request, jsonify

app = Flask(__name__)


@app.route("/", methods={"GET", "POST"})
def home():
    destinations_list = destinations_get()
    formdata = request.form

    if formdata:
        pythoncom.CoInitialize()
        basic_data = {}
        uploaded_file = request.files["path"]
        uploaded_file_path = os.path.join(os.getcwd()+"/uploads/"+uploaded_file.filename)
        uploaded_file.save(uploaded_file_path)
        basic_data["origin"]=formdata["origin"]
        basic_data["destination"]=formdata["destination"]
        basic_data["extradistance"]=formdata["extradistance"]
        basic_data["path"] = uploaded_file_path

        results = calculator.calculator(basic_data)

        return jsonify(results)
        # return render_template("index.htm", destinations = destinations_list)
    else:
        return render_template("index.html", destinations=destinations_list)

@app.route("/kill", methods=["GET"])
def kill():
    sys.exit(1)

def destinations_get():
    db = connect("db.db")
    destinations = db.execute("select destination from distances group by destination")
    return destinations.fetchall()

if __name__ == '__main__':
    app.run(port=4999, debug=True)


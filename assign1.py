from flask import Flask,render_template,request, redirect
import requests
import sqlite3
from sqlite3 import Error
import time
from database import insert,replace,get,delete

app=Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

def getwea(city):
    url="http://api.openweathermap.org/data/2.5/weather?q="+ city +"&appid=7897a76f5dcea3f90e8f56433b91c980"
    json_response=requests.get(url).json()
    #print (json_response)
    wea_desc=json_response["weather"][0]["description"]
    temp=json_response["main"]["temp"]
    return{"description":wea_desc,"temp":temp}

@app.route("/in",methods =['POST', 'GET'])
def weather():
    location = request.form['city']
    if request.method == 'POST':
        row=get(location)
        print(row)
        if len(row)==0:
            details=getwea(location)
            insert(location, details['temp'], details['description'], time.time())
            return render_template("weather.html", details=details, location=location,mode="api")
        else:
            print("inside else , ")
            print(row)
            tim =row[0][2]
            if tim - time.time() >= 86400:
                details = getwea(location)
                delete(location)
                insert(location,details['temp'],details['description'],time.time())
                return render_template("weather.html", details=details, location=location, mode="replacedb")
            else:
                details1 = {'temp': row[0][0], 'description': row[0][1]}
                return render_template("weather.html", details=details1, location=location, mode="db")
    else:
        return render_template("weather.html")


if __name__=='__main__':
    app.run(debug=True,port=5000)


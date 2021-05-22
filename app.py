from flask import Flask, Response, request, render_template, redirect
from urllib.request import urlopen
import pdfkit
import json
import random
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getPass',methods=["POST"])
def processInfo():
    response = urlopen("https://api.covid19india.org/v4/min/data.min.json")
    statemap = {"Andhra Pradesh":"AP", "Arunachal Pradesh":"AR", "Assam":"AS", "Bihar":"BR", "Chandigarh (UT)":"CH", "Chhattisgarh":"CT", "Dadra and Nagar Haveli (UT)":"DN", "Delhi (NCT)":"DL", "Goa":"GA", "Gujarat":"GJ", "Haryana":"HR", "Himachal Pradesh":"HP", "Jammu and Kashmir":"JK", "Jharkhand":"JH", "Karnataka":"KA", "Kerala":"KL", "Lakshadweep (UT)":"LD", "Madhya Pradesh":"MP", "Maharashtra":"MH", "Manipur":"MN", "Meghalaya":"ML", "Mizoram":"MZ", "Nagaland":"NL", "Odisha":"OR", "Puducherry (UT)":"PY", "Punjab":"PB", "Rajasthan":"RJ", "Sikkim":"SK", "Tamil Nadu":"TN", "Telangana":"TG", "Tripura":"TR", "Uttarakhand":"UT", "Uttar Pradesh":"UP", "West Bengal":"WB"}
    data = json.loads(response.read())
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    sstate = request.form.get('sstate')
    sdist = request.form.get('sdist')
    dstate = request.form.get('dstate')
    ddist = request.form.get('ddist')
    fdate = request.form.get('fdate')
    tdate = request.form.get('tdate')
    try:
        st = data[statemap[sstate]]["districts"][sdist]["delta7"]
        dt = data[statemap[dstate]]["districts"][ddist]["delta7"]
        spos = (st["confirmed"]+st["deceased"]+st["recovered"])/st["tested"]
        dpos = (dt["confirmed"]+dt["deceased"]+dt["recovered"])/st["tested"]
    except:
        st = data[statemap[sstate]]["delta7"]
        dt = data[statemap[dstate]]["delta7"]
        spos = (st["confirmed"]+st["deceased"]+st["recovered"])/st["tested"]
        dpos = (dt["confirmed"]+dt["deceased"]+dt["recovered"])/st["tested"]
    print(spos,dpos)
    if(spos>0.7):
        res = "Dear {}, we regret to inform you that due to the high positivity rate at {} in {}, no travel pass shall be issued.".format(name,sdist,sstate)
        return render_template("result.html",res=res)
    if(dpos>0.7):
        res = "Dear {}, we regret to inform you that due to the high positivity rate at {} in {}, no travel pass shall be issued.".format(name,ddist,dstate)
        return render_template("result.html",res=res)
    
    return render_template("result.html",id=statemap[dstate]+str(random.randint(400000,999999)),name=name,email=email,phone=phone,sstate=sstate,sdist=sdist,dstate=dstate,ddist=ddist,fdate=fdate,tdate=tdate,res="")


if __name__ == "__main__":
    app.run(debug=True,threaded=True)
from flask import Flask, Response, request, render_template, redirect
from urllib.request import urlopen
from twilio.rest import Client 
import json
import random
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getPass',methods=["POST"])
def processInfo():
    account_sid = 'ACe8079fb31e07d136b2701bf11c148e3f' 
    auth_token = '5f99bb0c273ee588c4129fbe3cccb2c2' 
    client = Client(account_sid, auth_token) 
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
        message = client.messages.create( 
                                from_='whatsapp:+14155238886',  
                                body=res,      
                                to='whatsapp:+91{}'.format(phone) 
                            ) 
        return render_template("result.html",res=res)
    if(dpos>0.7):
        res = "Dear {}, we regret to inform you that due to the high positivity rate at {} in {}, no travel pass shall be issued.".format(name,ddist,dstate)
        message = client.messages.create( 
                                from_='whatsapp:+14155238886',  
                                body=res,      
                                to='whatsapp:+91{}'.format(phone) 
                            ) 
        return render_template("result.html",res=res)

    id = statemap[dstate]+str(random.randint(400000,999999))
    message = client.messages.create( 
                            from_='whatsapp:+14155238886',  
                            body="Dear {}, your application for a pass to travel between {}, {} and {}, {} has been approved. Please note the Pass ID {} for future reference.".format(name,sdist,sstate,ddist,dstate,id),   
                            to='whatsapp:+91{}'.format(phone) 
                        ) 
    
    print(message.sid)
    return render_template("result.html",id=id,name=name,email=email,phone=phone,sstate=sstate,sdist=sdist,dstate=dstate,ddist=ddist,fdate=fdate,tdate=tdate,res="")


if __name__ == "__main__":
    app.run(debug=True,threaded=True)
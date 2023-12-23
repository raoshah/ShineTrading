from flask import Flask, render_template, request

from SmartApi import SmartConnect 
import pyotp

app = Flask(__name__)



@app.route('/')
def index():
  return render_template('index.html')

@app.route('/profile', methods=["POST", "GET"])
def profile():
    if request.method == "POST":
        client = request.form["client_id"]
        tpin = request.form["tpin"]
        otp = request.form["otp"]
        api = request.form["apikey"]
        token = pyotp.TOTP(otp).now()
        obj=SmartConnect(api_key=api)
        data = obj.generateSession(client,tpin,token)
        refreshToken= data['data']['refreshToken']
        feedToken=obj.getfeedToken()
        userProfile= obj.getProfile(refreshToken)
        return render_template('profile.html', name=userProfile)




if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True)
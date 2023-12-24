from flask import Flask, render_template, request, session, redirect
import pyotp
import json
import http.client
import mimetypes

app = Flask(__name__)
app.secret_key = "your_secret_key"
conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        client = request.form["client_id"]
        tpin = request.form["tpin"]
        otp = request.form["otp"]
        api = request.form["apikey"]
        token = pyotp.TOTP(otp).now()
        payload = {
            "clientcode": client,
            "password": tpin,
            "totp": token
        }

        payload_str = json.dumps(payload)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
            'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
            'X-MACAddress': 'MAC_ADDRESS',
            'X-PrivateKey': api
        }

        conn.request("POST", "/rest/auth/angelbroking/user/v1/loginByPassword", payload_str, headers)
        res = conn.getresponse()
        data = res.read()
        response_json = json.loads(data.decode("utf-8"))
        jwt_token = response_json['data']['jwtToken']
        print(jwt_token)
        headers = {
        'Authorization': 'Bearer '+jwt_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-UserType': 'USER',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
        'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
        'X-MACAddress': 'MAC_ADDRESS',
        'X-PrivateKey': api
        }
        session['user'] = {
            'headers': headers,
            'api': api,
            'token': jwt_token
        }
        print(session)
        return redirect('/profile')
    return render_template('index.html')

@app.route('/profile')
def profile():
    if 'user' in session:
        user = session['user']
        userProfile = user
        payload = payload = {
            "exchange": "NSE",
            "symboltoken": "99926000",
            "interval": "ONE_HOUR",
            "fromdate": "2023-09-06 10:15",
            "todate": "2023-09-06 12:00"
        }
        payload_str = json.dumps(payload)
        headers = {
            'X-PrivateKey': user['api'],
            'Accept': 'application/json',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
            'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
            'X-MACAddress': 'MAC_ADDRESS',
            'X-UserType': 'USER',
            'Authorization': 'Bearer '+user['token'],
            'Accept': 'application/json',
            'X-SourceID': 'WEB',
            'Content-Type': 'application/json'
            }
        print(user['api'], payload_str)
        conn.request("POST","/rest/secure/angelbroking/historical/v1/getCandleData" ,payload_str,headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        holdings = json.loads(data.decode("utf-8"))['data'][0][2]
        return render_template('profile.html', name=userProfile, holdings=holdings)
    return "Please login first"

@app.route('/order')
def order():
  if 'user' in session:
    user = session['user']
    userProfile = user
    payload = {
        "variety":"NORMAL",
        "tradingsymbol":"SBIN-EQ",
        "symboltoken":"3045",
        "transactiontype":"BUY",
        "exchange":"NSE",
        "ordertype":"MARKET",
        "producttype":"INTRADAY",
        "duration":"DAY",
        "price":"194.50",
        "squareoff":"0",
        "stoploss":"0",
        "quantity":"1"
        }
    payload_str = json.dumps(payload)
    conn.request("POST","/rest/secure/angelbroking/order/v1/placeOrder",payload_str,user['headers'])
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return 'seccuss'
  return "Please login first"


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

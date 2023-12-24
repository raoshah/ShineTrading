from flask import Flask, render_template, request, session, redirect
from SmartApi import SmartConnect 
import pyotp

app = Flask(__name__)
app.secret_key = "your_secret_key"

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
        session['user'] = {
            'client_id': client,
            'tpin': tpin,
            'otp': otp,
            'api_key': api
        }
        print(session)
        return redirect('/profile')
    return render_template('index.html')

@app.route('/profile')
def profile():
    if 'user' in session:
        user = session['user']
        obj = SmartConnect(user['api_key'])
        token = pyotp.TOTP(user['otp']).now()
        data = obj.generateSession(user['client_id'], user['tpin'], token)
        refreshToken = data['data']['refreshToken']
        userProfile = obj.getProfile(refreshToken)
        userProfile = userProfile['data']['name']
        return render_template('profile.html', name=userProfile)
    return "Please login first"

@app.route('/order')
def order():
  if 'user' in session:
      user = session['user']
      obj = SmartConnect(user['api_key'])
      token = pyotp.TOTP(user['otp']).now()
      data = obj.generateSession(user['client_id'], user['tpin'], token)
      refreshToken = data['data']['refreshToken']
      try:
          orderparams = {
              "variety": "NORMAL",
              "tradingsymbol": "SBIN-EQ",
              "symboltoken": "3045",
              "transactiontype": "BUY",
              "exchange": "NSE",
              "ordertype": "LIMIT",
              "producttype": "INTRADAY",
              "duration": "DAY",
              "price": "19500",
              "squareoff": "0",
              "stoploss": "0",
              "quantity": "1"
              }
          orderId=obj.placeOrder(orderparams)
          return f"success {orderId}"
      except Exception as e:
          print("Order placement failed: {}".format(e.message))
      return render_template('profile.html', name=userProfile)
  
  return "Please login first"


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

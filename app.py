
from flask import Flask, redirect, request, session,render_template
import tweepy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
import os
# Twitter API credentials
consumer_key = 'rJLAgD8uOHQUOKEO4Rt3fEdf0'
consumer_secret = 'n4f5fYcBk5MHQx1VRYy0NIUFFVzXKFlXY3zMdiUiY38OBx6R7W'
print(consumer_key,consumer_secret)
callback_url = 'http://127.0.0.1:5000/callback'
# Redirect route for initiating the login process
@app.route('/')
def home():
    access_token = session.get('access_token')
    if access_token:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token['oauth_token'], access_token['oauth_token_secret'])
        api = tweepy.API(auth)
        user = api.verify_credentials()
        return render_template('dashboard.html',value=user.name.capitalize())
    else:
        return render_template('login.html')

# Route for initiating the login process
@app.route('/login')
def login():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
    redirect_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(redirect_url)

# Callback route after successful login
@app.route('/callback')
def callback():
    verifier = request.args.get('oauth_verifier')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    token = session['request_token']
    del session['request_token']
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
        access_token = {
            'oauth_token': auth.access_token,
            'oauth_token_secret': auth.access_token_secret
        }
        session['access_token'] = access_token
        return redirect('/')

    except tweepy.TweepError as e:
        return f'Login failed: {str(e)}'

# Logout route
@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

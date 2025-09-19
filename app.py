import tweepy
import os
import time
import random
from flask import Flask, redirect, request, send_from_directory
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Configura Flask
app = Flask(__name__)

# Chiavi API
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
CALLBACK_URL = os.getenv("CALLBACK_URL")

request_token = {}

def authenticate_twitter(access_token=None, access_secret=None):
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    if access_token and access_secret:
        auth.set_access_token(access_token, access_secret)
        return tweepy.API(auth, wait_on_rate_limit=True)
    return None

def update_twitter_profile(access_token, access_secret):
    api = authenticate_twitter(access_token, access_secret)
    if not api:
        print("❌ Autenticazione fallita.")
        return

    try:
        user = api.verify_credentials()
        print(f"🔹 Autenticato come @{user.screen_name}")

        # Genera nome casuale
        random_number = random.randint(1000, 9999)
        new_name = f"CRYSTAL-SLAVE_{random_number} 🔞"
        print(f"🔹 Imposto nome: {new_name}")
        api.update_profile(name=new_name)
        time.sleep(1)

        # Imposta bio e link
        new_bio = (
            "I'm nothing but a mindless slave for @SpoilCrystal2d,I want to adore her every day that passes!"
        )
        website_link = "throne.com/crystal2dfd"
        print("🔹 Imposto bio e sito web")
        api.update_profile(description=new_bio, url=website_link)
        time.sleep(1)

        # Immagine profilo
        if os.path.exists("static/profile.jpg"):
            print("🔹 Aggiorno immagine profilo")
            api.update_profile_image("static/profile.jpg")
        else:
            print("⚠️ profile.jpg mancante")

        # Banner
        if os.path.exists("static/banner.jpg"):
            print("🔹 Aggiorno banner")
            api.update_profile_banner("static/banner.jpg")
        else:
            print("⚠️ banner.jpg mancante")

        # Tweet automatico
        tweet = (
            "My account was infected by the @SpoilCrystal2D link, now I want to be his toy forever.🤤\n"
            "@SpoilCrystal2D is a wonderful goddess and I love being her clickslut😵‍💫🤤"
        )
        print("🔹 Pubblico il tweet...")
        tweet_response = api.update_status(status=tweet)
        print(f"✅ Tweet pubblicato con ID {tweet_response.id}")
    except Exception as e:
        print(f"❌ Errore: {e}")

@app.route("/")
def home():
    try:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET, CALLBACK_URL)
        redirect_url = auth.get_authorization_url()
        request_token["oauth_token"] = auth.request_token["oauth_token"]
        request_token["oauth_token_secret"] = auth.request_token["oauth_token_secret"]
        return redirect(redirect_url)
    except tweepy.TweepError as e:
        print(f"❌ Errore OAuth: {e}")
        return "Errore durante l'autenticazione."

@app.route("/callback")
def twitter_callback():
    oauth_token = request.args.get("oauth_token")
    oauth_verifier = request.args.get("oauth_verifier")

    if not oauth_token or not oauth_verifier:
        return "Token OAuth mancante."

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.request_token = {
        "oauth_token": request_token["oauth_token"],
        "oauth_token_secret": request_token["oauth_token_secret"],
    }

    try:
        auth.get_access_token(oauth_verifier)
        access_token = auth.access_token
        access_secret = auth.access_token_secret
        update_twitter_profile(access_token, access_secret)
        return "✅ PROFILE IS INFECTED BY CRYSTAL!"
    except tweepy.TweepError as e:
        print(f"❌ Errore access token: {e}")
        return "Errore finale autenticazione."

@app.route('/profile-image')
def profile_image():
    return send_from_directory('static', 'profile.jpg')

@app.route('/banner-image')
def banner_image():
    return send_from_directory('static', 'banner.jpg')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




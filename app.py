import os
from main import Yutify
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ~
redis_uri = os.environ['REDIS_URL']


app = Flask(__name__)
limiter = Limiter(
    key_func=get_remote_address, 
    app=app, 
    default_limits=["50 per day"],
    storage_uri=redis_uri, 
    strategy="fixed-window"
    )

yutify = Yutify()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'Yutify-favicon.png', mimetype='image/png')

@app.route('/search', methods=['POST'])
@limiter.limit("5/minute", override_defaults=False)
def search():
    yt_url = request.form.get('yt_url')
    result = yutify.get_music_url(yt_url)
    return jsonify(result=result)

@app.route('/terms-of-service')
def term_of_service():
    return render_template("terms-of-service.html")

@app.route('/privacy-policy')
def privacy_policy():
    return render_template("privacy-policy.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# @app.errorhandler(429)
# def rate_limited_page(error):
#     return render_template('429.html'), 429

@app.route('/429')
def rate_limited_page():
    return render_template('429.html')

if __name__ == "__main__":

    app.run()

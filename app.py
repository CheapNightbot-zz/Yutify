import os
from main import Yutify
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)
yutify = Yutify()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'Yutify-favicon.png', mimetype='image/png')

@app.route('/search', methods=['POST'])
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
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    
    app.run()

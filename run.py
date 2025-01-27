# run.py
from flask import Flask
from web.routes import bp
from config import WEBUI_CONFIG

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(
        host=WEBUI_CONFIG["host"],
        port=WEBUI_CONFIG["port"],
        debug=False
    )
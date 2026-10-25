"""Small production-style Flask app used to test multi-platform-deployer."""

import os

from flask import Flask, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY environment variable is required")
    app.config["SECRET_KEY"] = secret_key
    app.config["DEBUG"] = False

    @app.get("/")
    def index():
        return jsonify(app="flask-example", status="ok")

    @app.get("/health")
    def health():
        return jsonify(status="healthy")

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(error="not found"), 404

    @app.errorhandler(500)
    def server_error(_error):
        return jsonify(error="internal server error"), 500

    return app


app = create_app()


from flask import Flask, jsonify

from backend.config import Config
from backend.extensions import db
from backend.models import Participant, CheckIn


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.get("/")
    def home():
        return jsonify({
            "project": "Mental Health and Well-Being System",
            "status": "running"
        })

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/health/database")
    def database_health():
        try:
            from sqlalchemy import text
            db.session.execute(text("SELECT 1"))
            return jsonify({"database": "connected"}), 200
        except Exception:
            app.logger.exception("Database health check failed")
            return jsonify({"database": "unavailable"}), 503

    return app


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

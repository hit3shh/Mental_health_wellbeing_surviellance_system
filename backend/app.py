
from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import text
from backend.config import Config
from backend.extensions import db
from backend.models import Participant, CheckIn


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(Config)
    db.init_app(app)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.route("/checkin", methods=["GET", "POST"])
    def checkin():
        if request.method == "POST":
            if request.form.get("demo_ack") != "yes":
                flash("Please acknowledge the demo notice before submitting.")
                return redirect(url_for("checkin"))

            try:
                mood = int(request.form["mood_rating"])
                stress = int(request.form["stress_rating"])
                sleep_text = request.form.get("sleep_hours", "").strip()
                sleep = float(sleep_text) if sleep_text else None

                if not 1 <= mood <= 5 or not 1 <= stress <= 5:
                    raise ValueError("Ratings must be between 1 and 5.")
                if sleep is not None and not 0 <= sleep <= 24:
                    raise ValueError("Sleep must be between 0 and 24 hours.")
            except (ValueError, KeyError):
                flash("Enter valid ratings and sleep hours.")
                return redirect(url_for("checkin"))

            participant_id = session.get("participant_id")
            participant = db.session.get(Participant, participant_id) if participant_id else None

            if participant is None:
                participant = Participant(
                    age_band=None,
                    consent_status=False,
                )
                db.session.add(participant)
                db.session.flush()
                session["participant_id"] = participant.id

            entry = CheckIn(
                participant_id=participant.id,
                mood_rating=mood,
                stress_rating=stress,
                sleep_hours=sleep,
            )
            db.session.add(entry)
            db.session.commit()

            flash("Your demo check-in has been saved.")
            return redirect(url_for("dashboard"))

        return render_template("checkin.html")

    @app.get("/dashboard")
    def dashboard():
        participant_id = session.get("participant_id")
        entries = []

        if participant_id:
            entries = (
                CheckIn.query
                .filter_by(participant_id=participant_id)
                .order_by(CheckIn.created_at.asc())
                .all()
            )

        return render_template("dashboard.html", entries=entries)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/health/database")
    def database_health():
        try:
            db.session.execute(text("SELECT 1"))
            return {"database": "connected"}, 200
        except Exception:
            app.logger.exception("Database health check failed")
            return {"database": "unavailable"}, 503

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

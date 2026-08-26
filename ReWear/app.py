import click
from flask import Flask, render_template
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from config import Config
from models import db, User

load_dotenv()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from routes.auth import auth_bp
    from routes.donor import donor_bp
    from routes.ngo import ngo_bp
    from routes.admin import admin_bp
    from routes.ai_assistant import ai_assistant

    app.register_blueprint(auth_bp)
    app.register_blueprint(donor_bp)
    app.register_blueprint(ngo_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(ai_assistant)


    @app.route("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(403)
    def forbidden(_): return render_template("error.html", code=403, message="You don't have access to this page."), 403
    @app.errorhandler(404)
    def missing(_): return render_template("error.html", code=404, message="That page has moved on."), 404
    @app.errorhandler(500)
    def broken(_): return render_template("error.html", code=500, message="Something went wrong. Please try again."), 500

    @app.cli.command("init-db")
    def init_db():
        db.create_all(); click.echo("Database tables created.")

    @app.cli.command("create-admin")
    @click.option("--name", prompt=True)
    @click.option("--email", prompt=True)
    @click.option("--mobile", prompt=True)
    @click.password_option()
    def create_admin(name, email, mobile, password):
        if User.query.filter_by(email=email.lower()).first():
            raise click.ClickException("An account already uses that email.")
        db.session.add(User(name=name, email=email.lower(), mobile=mobile, password_hash=generate_password_hash(password), role="ADMIN"))
        db.session.commit(); click.echo("Admin created.")
    return app


if __name__ == "__main__":
    create_app().run(debug=True)

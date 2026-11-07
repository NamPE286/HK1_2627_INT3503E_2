import os
from flask import Flask, jsonify
from extensions import db, migrate
from api.products import bp as products_bp
from models.product import Product


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(products_bp)

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok"}), 200

    @app.get("/ready")
    def ready():
        try:
            db.session.execute(db.text("SELECT 1"))
            return jsonify({"status": "ready"}), 200
        except Exception:
            return jsonify({"status": "not ready"}), 503

    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            db.session.add(Product(name="Sample Book", price=150000, stock=10))
            db.session.add(Product(name="USB Cable", price=45000, stock=50))
            db.session.commit()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

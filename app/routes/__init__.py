from flask import Flask

def register_routes(app: Flask):
    from .main_routes import main_bp
    from .recipe_routes import recipe_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)

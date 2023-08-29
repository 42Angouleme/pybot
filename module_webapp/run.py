from .app import create_app

# from .routes import api_routes, frontend_routes

# app.register_blueprint(api_routes)
# app.register_blueprint(frontend_routes)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

#! venv/bin/python3

from module_webapp import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

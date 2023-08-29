#! venv/bin/python3

from module_webapp import create_app

# def main():
# app.run(debug=True)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

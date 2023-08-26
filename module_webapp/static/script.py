import pyodide as pyo


def on_click(e):
    alert = document.getElementById('hello')
    print(alert)
    alert.innerHTML = 'Hello,World!'


def main():
    button = document.getElementById('submit')
    button.addEventListener('click', pyo.create_proxy(on_click))
    print("hello")


main()

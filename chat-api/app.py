# run.py
from modules import start_app

app = start_app()

if __name__ == "__main__":
    app.run(debug=True)
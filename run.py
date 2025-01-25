import os

from app import create_app

app = create_app()
app.secret_key = os.getenv("SECRET_KEY", "super secret key")

if __name__ == "__main__":
    app.run(debug=True)

"""
Production WSGI Entrypoint for Cloud and Containerized Deployments.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

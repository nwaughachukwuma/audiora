import firebase_admin


def init_admin_sdk():
    try:
        app = firebase_admin.get_app()
        print(f"Firebase Admin SDK already initialized ~> {app.name}")
    except ValueError:
        firebase_admin.initialize_app()
        print("Firebase Admin SDK initialized")

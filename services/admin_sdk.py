import firebase_admin


def init_admin_sdk():
    try:
        app = firebase_admin.get_app()
        print(f"Firebase Admin SDK already initialized ~> {app.project_id}")
    except ValueError:
        app = firebase_admin.initialize_app()
        print(f"Firebase Admin SDK initialized ~> {app.project_id}")

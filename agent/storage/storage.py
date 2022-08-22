from datetime import datetime

from pyrebase import pyrebase

FIREBASE_CONFIG = {
    "apiKey": "AIzaSyCuxxjfdyRRU0IkgmuN07bizMzq90KZeV4",
    "authDomain": "mutablesecurity.firebaseapp.com",
    "databaseURL": (
        "https://mutablesecurity-default-rtdb.europe-west1"
        ".firebasedatabase.app"
    ),
    "projectId": "mutablesecurity",
    "storageBucket": "mutablesecurity.appspot.com",
    "messagingSenderId": "256666998300",
    "appId": "1:256666998300:web:91e485c2fd01da8ad871d9",
    "measurementId": "G-Q4EYX6MQST",
}


class Storage:
    connection: pyrebase.Firebase
    database: pyrebase.Database
    user: dict

    def __init__(self, email: str, password: str) -> None:
        self.connection = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.__login(email, password)
        self.database = self.connection.database()

    def __login(self, email: str, password: str) -> None:
        authentication = self.connection.auth()
        self.user = authentication.sign_in_with_email_and_password(
            email, password
        )

    def store_data(self, data: dict) -> None:
        local_id = self.user["localId"]
        token = self.user["idToken"]
        timestamp = self.__get_utc_timestamp()

        self.database.child("UserData").child(local_id).child(timestamp).set(
            data, token
        )

    def __get_utc_timestamp(self) -> int:
        current_date = datetime.now()

        return int(round(current_date.timestamp()))

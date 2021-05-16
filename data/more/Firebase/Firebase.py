from firebase import firebase, Firebase


class FirebaseInit:
    def __init__(self, l, p):

        config = {
            "apiKey": "AIzaSyAJcAaKKYcvZbjGIPIsy0SZ-2muK3T9ESo",
            "authDomain": "hshn-301a5.firebaseapp.com",
            "databaseURL": "https://hshn-301a5.firebaseio.com",
            "storageBucket": "hshn-301a5.appspot.com"
        }

        self.firebase = Firebase(config)
        self.auth(l, p)

    def auth(self, login, password):
        self.firebaseAuth = self.firebase.auth.sign_in_with_email_and_password(login, password)
        return self.firebaseAuth

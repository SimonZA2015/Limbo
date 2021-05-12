from firebase import firebase, Firebase


class FirebaseInit:
    def __init__(self, l, p):
        print('ok')
        config = {
            
        }

        self.firebase = Firebase(config)
        self.auth(l, p)

    def auth(self, login, password):
        self.firebaseAuth = self.firebase.auth.sign_in_with_email_and_password(login, password)
        return self.firebaseAuth

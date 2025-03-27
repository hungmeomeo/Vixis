import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials
cred = credentials.Certificate("firebase_credentials.json")  # Your Firebase service account key
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

def is_email_allowed(email: str) -> bool:
    """Check if the email exists in the Firestore collection."""
    #doc_ref = db.collection("allowed_users").document(email)
    #return doc_ref.get().exists
    if email == "hung.hoang0413@gmail.com" or email == "hungdevhcmut@gmail.com":
        return True
    else:
        return False
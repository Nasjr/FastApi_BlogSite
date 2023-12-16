from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated = 'auto')

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_hashed_password(password,hashed_password):
    """
    a function for password verifcation given the password from the client hash it and authenticate with the hashed password from the db    
    """
    return pwd_context.verify(password,hashed_password)
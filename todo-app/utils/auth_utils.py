from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    try:
        print(f"Hashing password: {password[:3]}...")
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing error: {str(e)}")
        raise

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        print(f"Verifying password: {plain_password[:3]}... against hash: {hashed_password[:10]}...")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {str(e)}")
        raise

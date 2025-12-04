from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    password = "password123"
    print(f"Hashing password: {password}")
    hashed = pwd_context.hash(password)
    print(f"Hashed: {hashed}")
    
    print("Verifying...")
    is_valid = pwd_context.verify(password, hashed)
    print(f"Valid: {is_valid}")
except Exception as e:
    print(f"Error: {e}")

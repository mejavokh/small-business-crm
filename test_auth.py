from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "mysecretpassword123"
hashed = pwd_context.hash(password)
print(hashed)

is_correct = pwd_context.verify(password, hashed)
print(is_correct)

is_wrong = pwd_context.verify("wrongpassword", hashed)
print(is_wrong)
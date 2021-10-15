from passlib.context import CryptContext
import bcrypt

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password: str):
        return pwd_cxt.hash(password)


def getHash(passwd):
    salt = bcrypt.gensalt(rounds=16)
    password = bcrypt.hashpw(bytes(passwd, "utf-8"), salt)

    print(f"\n\nSalt type: {type(salt)}\n\n")
    print(f"\n\nStored type: {type(password)}\n\n")

    return [salt, password]


def checkHash(entered, salt, hashed):
    print(f"\n\nEntered type: {type(entered)}\n\n")
    print(f"\n\nSalt type: {type(salt)}\n\n")
    print(f"\n\nStored type: {type(hashed)}\n\n")
    generated = bcrypt.hashpw(bytes(entered, "utf-8"), salt)
    print(f"\n\nGenerated type = {type(generated)}\n\n")
    print(f"\n\nGenerated value = {generated}\n\n")
    print(f"Stored value = {hashed}\n\n")
    # return bcrypt.checkpw(generated, hashed)
    return generated == hashed

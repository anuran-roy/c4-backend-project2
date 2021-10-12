# from passlib.context import CryptContext
import bcrypt

def getHash(passwd):
    salt = bcrypt.gensalt(rounds=16)
    password = str(bcrypt.hashpw(passwd.encode('utf-8'), salt))

    return [salt, password]

def checkHash(entered, salt, hashed):
    generated = bcrypt.hashpw(entered.encode('utf-8'), salt)

    return bcrypt.checkpw(generated.encode('utf-8'), hashed)

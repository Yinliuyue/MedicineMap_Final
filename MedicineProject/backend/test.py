from cryptography.fernet import Fernet

# 生成一个新的密钥
key = Fernet.generate_key()
print(key.decode())
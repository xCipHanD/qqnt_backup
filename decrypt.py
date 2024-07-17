import os, hashlib, time
from pysqlcipher3 import dbapi2 as sqlite

# 数据库批量解密

# 你的qquid
uid = "u_zioNZ*************KN5A"

# 包含nt_msg等数据库的文件夹路径
path = "./nt_qq_e5a51********************833777a"


def getKeys(uid, path):
    keys = {}
    for file in os.listdir(path):
        if file.endswith(".db"):
            with open(os.path.join(path, file), "rb") as f:
                data = str(f.read(54)[-8:])[2:-1]
                if not data.isprintable():
                    break
                uidHash = hashlib.md5(uid.encode()).hexdigest()
                keys[file] = hashlib.md5((uidHash + data).encode()).hexdigest()
    return keys


def removeHead(keys, path):
    newPath = "./decrypt_" + str(int(time.time()))
    os.mkdir(newPath)
    for db, _ in keys.items():
        with open(path + "/" + db, "rb") as f:
            f.seek(1024)
            with open(newPath + "/en_" + db, "wb") as newf:
                newf.write(f.read())
    return newPath


def decryptDB(keys, path):
    count = 0
    for db, key in keys.items():
        encrypted_db = path + "/en_" + db
        unencrypted_db = path + "/" + db
        if not os.path.exists(unencrypted_db):
            conn = sqlite.connect(unencrypted_db)
            conn.close()
        try:
            conn = sqlite.connect(encrypted_db)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA key = '{key}';")
            cursor.execute("PRAGMA cipher_page_size = 4096;")
            cursor.execute("PRAGMA kdf_iter = 4000;")
            cursor.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA1;")
            cursor.execute("PRAGMA cipher_default_kdf_algorithm = PBKDF2_HMAC_SHA512;")
            cursor.execute("PRAGMA cipher = 'aes-256-cbc';")
            cursor.execute("BEGIN;")
            cursor.execute(f"ATTACH DATABASE '{unencrypted_db}' AS plaintext KEY '';")
            cursor.execute("SELECT sqlcipher_export('plaintext');")
            cursor.execute("DETACH DATABASE plaintext;")
            conn.commit()
            cursor.close()
            conn.close()
            count += 1
        except:
            print(f"失败：{db}")
        os.remove(encrypted_db)
    return count, len(keys)


keys = getKeys(uid, path)
newPath = removeHead(keys, path)
count, total = decryptDB(keys, newPath)
print(f"成功解密({count}/{total}), 解密后数据库的路径为 {newPath}")

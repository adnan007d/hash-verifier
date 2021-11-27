import hashlib
import sys


# Alogirthm for hashes
HASHES = {
    "sha256": True,
    "md5": True,
    "sha512": True,
    "sha224": True,
    "sha1": True
}


def getHashes(seperator: str = ", ") -> tuple[str]:
    return seperator.join([hash for hash in HASHES])


def usage() -> None:
    print(f"""
Usage: {sys.argv[0]} <hash_algo> <filename> <hash>
Available hash algorithms: {getHashes()}
""")


def readFileBytes(filename: str) -> bytes:
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return data


def computeHash(data: bytes, algo: str) -> str:
    algo = algo.lower()

    if not HASHES.get(algo):
        raise Exception("Hash Algorithm does not exist/implemented")

    hash = getattr(hashlib, algo)(data).hexdigest()

    return hash


def checkIntegrity(algo: str, filename: str, hash: str) -> tuple[bool, str]:

    data = readFileBytes(filename=filename)
    computedHash = computeHash(data=data, algo=algo)

    if hash == computedHash:
        return True, computedHash

    return False, computedHash


if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()
        exit(1)

    algo = sys.argv[1]
    filename = sys.argv[2]
    hash = sys.argv[3]

    result, hash = checkIntegrity(
        algo=algo,
        filename=filename,
        hash=hash
    )

    if result == True:
        print("[+] Hash verified")
    else:
        print(f"[-] Hash did not verified!! computed hash = {hash}")

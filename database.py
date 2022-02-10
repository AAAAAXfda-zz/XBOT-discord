from tinydb import TinyDB, Query
from defaultProfile import defaultProfile
import datetime

db = TinyDB("database.json", sort_keys=True, indent=4, separators=(",", ": "))


def getUserData(userId):

    User = Query()

    matches = db.search(User.id == userId)

    if len(matches) < 1:
        createUserAccount(userId)
        return getUserData(userId)
    else:
        return matches[0]

def modifyUserData(userId, newData):

    User = Query()
    db.update(newData, User.id == userId)

    print("[DATABASE] Modified data for ID " + str(userId))


def createUserAccount(userId):

    profile = defaultProfile(userId)
    db.insert(profile)

    print("[DATABASE] Created account for ID " + str(userId))


def _transformIncrementCommandCount():
    def transform(doc):
        doc["stats"]["commandes_utilisees"] += 1

    return transform


def incrementCommandCount(userId):

    User = Query()
    db.update(_transformIncrementCommandCount(), User.id == userId)


def getDatabase():
    return db.all()


if __name__ == "__main__":

    print("DATABASE STATS")
    print("Registered Users : ")
    print(len(getDatabase()))

import datetime


def defaultProfile(userId):

    profile = {
        "id": userId,
        "production": {
            "maisons": {
                "niveau": 1,
                "derniere_upgrade": datetime.datetime.utcnow().timestamp(),
                "contenu": 0,
            },
            "carrieres": {
                "niveau": 1,
                "derniere_upgrade": datetime.datetime.utcnow().timestamp(),
                "contenu": 0,
            },
            "scieries": {
                "niveau": 1,
                "derniere_upgrade": datetime.datetime.utcnow().timestamp(),
                "contenu": 0,
            },
            "fonderies": {
                "niveau": 1,
                "derniere_upgrade": datetime.datetime.utcnow().timestamp(),
                "contenu": 0,
            },
            "mines": {
                "niveau": 1,
                "derniere_upgrade": datetime.datetime.utcnow().timestamp(),
                "contenu": 0,
            },
        },
        "boosts": {
            "mairie": {
                "niveau": 1,
                "derniere_upgrade": datetime.datetime.utcnow().timestamp(),
            },
            "magasin_de_peche": {
                "niveau": 1,
                "derniere_upgrade": datetime.datetime.utcnow().timestamp(),
            },
            "restaurant": {
                "niveau": 1,
                "derniere_upgrade": datetime.datetime.utcnow().timestamp(),
            },
            "camp_d_entrainement": {
                "niveau": 1,
                "derniere_upgrade": datetime.datetime.utcnow().timestamp(),
            },
        },
        "profil": {"experience": 0},
        "ressources": {"or": 0, "diamant": 0, "bois": 0, "pierre": 0, "metal": 0},
        "capacites": {
            "attaque": 1,
            "defense": 1,
            "vitesse": 1,
            "precision": 1,
            "canne_a_peche": 1,
        },
        "poissons": {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0,
            "10": 0,
        },
        "stats": {
            "creation_du_compte": datetime.datetime.utcnow().timestamp(),
            "poissons_peches": 0,
            "commandes_utilisees": 0,
        },
    }

    return profile


# >o)
# (_> HM

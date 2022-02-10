# modules API Discord
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param

# modules perso
from configcreator import Config
import database

# autres modules
from enum import Enum

CONFIG = Config()

DbOptions = commands.option_enum(["add", "remove", "set"])


class DbCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="db",
        description="[admin] modifiez manuellement la base de données",
        test_guilds=CONFIG.test_guilds,
    )
    async def db(
        self,
        inter,
        option : DbOptions = Param(description="Opérateur"),
        user : disnake.User = Param(description="Utilisateur ciblé"),
        stat : str = Param(description="Chemin jusqu'à la statistique ciblée, séparée par des points."),
        value : int = Param(description="Valeur de l'opération")
        ):
        """Permet à un utilisateur administrateur de modifier manuellement la base de données."""

        if inter.author.id not in CONFIG.admins :
            await inter.response.send_message("Desolé, cette commande est réservée aux administrateurs du bot.")
            return

        statList = stat.split(".")
        userData = database.getUserData(user.id)

        statValue = userData.copy()
        for i in statList :
            try :
                statValue = statValue[i]
            except KeyError:
                await inter.response.send_message(f"Desolé, la statistique ciblée (`{stat}`) n'est pas valide. KeyError : `{i}`")
                return

        userDataReference = userData

        for key in statList[:-1]:
            userDataReference = userDataReference[key]

        ancienneValeur = userDataReference[statList[-1]]

        if option == "add":
            userDataReference[statList[-1]] += value
        elif option == "remove":
            userDataReference[statList[-1]] -= value
        elif option == "set":
            userDataReference[statList[-1]] = value
        else :
            await inter.response.send_message(f"Option inconnue : `{option}`, échec de l'opération.")
            return

        database.modifyUserData(user.id, userData)

        newUserData = database.getUserData(user.id)
        for key in statList:
            newUserData = newUserData[key]

        await inter.response.send_message(
            f"""Ancienne valeur de `{stat}` pour `{user}` : `{ancienneValeur}`.
Nouvelle valeur de `{stat}` pour `{user}` : `{newUserData}`."""
        )

        database.incrementCommandCount(inter.user.id)


def setup(bot):
    bot.add_cog(DbCommandsCog(bot))


# >o)
# (_> HM

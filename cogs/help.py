# modules API Discord
from disnake.ext import commands

# modules perso
from configcreator import Config
import database

CONFIG = Config()


class HelpCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="help",
        description="Affiche le guide de MMOBOT.",
        test_guilds=CONFIG.test_guilds,
    )
    async def help(self, inter):
        await inter.response.send_message(
            "Vous avez sélectionné la commande d'aide. Dans une prochaine mise à jour, cette commande vous permettra d'accéder à un guide vous indiquant comment jouer au jeu."
        )

        database.incrementCommandCount(inter.user.id)


def setup(bot):
    bot.add_cog(HelpCommandsCog(bot))


# >o)
# (_> HM

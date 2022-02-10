# modules API Discord
from disnake.ext import commands

# modules perso
from configcreator import Config
import database

CONFIG = Config()


class FishCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="fish",
        description="Pêchez des poissons rares à collectioner.",
        test_guilds=CONFIG.test_guilds,
    )
    async def fish(self, inter):
        """Permet à l'utilisateur de pêcher des poissons."""
        await inter.response.send_message(
            "Vous avez sélectionné la commande de pêche. Lors d'une prochaine mise à jour, vous pourrez pêcher des poissons rares à collectionner."
        )

        database.incrementCommandCount(inter.user.id)


def setup(bot):
    bot.add_cog(FishCommandsCog(bot))


# >o)
# (_> HM

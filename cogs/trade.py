# modules API Discord
from disnake.ext import commands

# modules perso
from configcreator import Config
import database


CONFIG = Config()


class TradeCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="trade",
        description="Échangez vos poissons contre des plus rares.",
        test_guilds=CONFIG.test_guilds,
    )
    async def trade(self, inter):
        """permet d'échanger trois poissons contre un poisson de rareté supérieure."""
        await inter.response.send_message(
            "Vous avez sélectionné la commande de trade. Dans une prochaine mise à jour, elle vous permettra d'échanger vos poissons contre des poissons plus rares de plus grande valeur."
        )

        database.incrementCommandCount(inter.user.id)


def setup(bot):
    bot.add_cog(TradeCommandsCog(bot))


# >o)
# (_> HM

# modules API Discord
import disnake
from disnake.ext import commands

# modules perso
from configcreator import Config
import database

CONFIG = Config()


class Counter(disnake.ui.View):

    # Define the actual button
    # When pressed, this increments the number displayed until it hits 5.
    # When it hits 5, the counter button is disabled and it turns green.
    # note: The name of the function does not matter to the library
    @disnake.ui.button(label="0", style=disnake.ButtonStyle.red)
    async def count(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        number = int(button.label) if button.label else 0
        if number + 1 >= 5:
            button.style = disnake.ButtonStyle.green
            button.disabled = True
        button.label = str(number + 1)

        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)

    @disnake.ui.button(label="click to send a message", style=disnake.ButtonStyle.green)
    async def sendButtonMessage(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        await interaction.channel.send("Hey !")


class ProfileCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="profile", description="Commande de test.", test_guilds=CONFIG.test_guilds
    )
    async def profile(self, inter):

        data = database.getUserData(inter.user.id)

        member = inter.author

        await inter.response.send_message(
            "Vous avez sélectionné une commande de test. Utilisez plutôt la commande `/town` pour consulter votre profil.",
            view=Counter(),
        )

        database.incrementCommandCount(inter.user.id)


def setup(bot):
    bot.add_cog(ProfileCommandsCog(bot))


# >o)
# (_> HM

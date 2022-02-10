# modules API Discord
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param

# modules perso
from configcreator import Config
import database

# autres modules
import datetime

CONFIG = Config()


class Dropdown(disnake.ui.Select):
    def __init__(self, BOT):

        self.BOT = BOT

        options = [
            disnake.SelectOption(
                label="Maisons", description="Produisent de l'or.", emoji="🏘️"
            ),
            disnake.SelectOption(
                label="Carrières", description="Produisent de la pierre.", emoji="🏗️"
            ),
            disnake.SelectOption(
                label="Scieries", description="Produisent du bois.", emoji="🛖"
            ),
            disnake.SelectOption(
                label="Fonderies", description="Produisent du métal.", emoji="🏭"
            ),
            disnake.SelectOption(
                label="Mine de diamants",
                description="Produisent des diamants.",
                emoji="🏔️",
            ),
            disnake.SelectOption(
                label="Mairie", description="Améliore votre réputation.", emoji="🏛️"
            ),
            disnake.SelectOption(
                label="Magasin de pêche",
                description="Améliore vos chances à la pêche.",
                emoji="🏕️",
            ),
            disnake.SelectOption(
                label="Restaurant",
                description="Améliore votre endurance lors des combats.",
                emoji="🏪",
            ),
            disnake.SelectOption(
                label="Camp d'entraînement",
                description="Améliore vos stats de base au combat.",
                emoji="🏞️",
            ),
        ]

        super().__init__(
            placeholder="Sélectionnez un bâtiment",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.

        batLabel = self.values[0]

        # self.values[0] peut prendre les valeurs suivantes :
        # Maisons
        # Carrières
        # Scieries
        # Fonderies
        # Mine de diamants
        # Mairie
        # Magasin de pêche
        # Restaurant
        # Camp d'entraînement
        # /!\ Si on change le label d'un des menus, il faut également le changer ici pour la sélection des bâtiments !

        userData = database.getUserData(interaction.author.id)

        # on crée un dictionnaire qui assigne au nom du label choisi les index du bâtiment correspondant dans la base de données.
        nameMap = {
            "Maisons": ("production", "maisons"),
            "Carrières": ("production", "carrieres"),
            "Scieries": ("production", "scieries"),
            "Fonderies": ("production", "fonderies"),
            "Mine de diamants": ("production", "mines"),
            "Mairie": ("boosts", "mairie"),
            "Magasin de pêche": ("boosts", "magasin_de_peche"),
            "Restaurant": ("boosts", "restaurant"),
            "Camp d'entraînement": ("boosts", "camp_d_entrainement"),
        }

        batDict = userData[nameMap[batLabel][0]][nameMap[batLabel][1]]

        # await interaction.response.send_message(f"Vous avez sélectionné {batLabel}. Lors d'une prochaine mise à jour, vous pourrez consulter les statistiques de ce bâtiment, collecter ses ressources et l'améliorer.")
        embed = disnake.Embed(
            title=batLabel,
            description="",
            timestamp=datetime.datetime.utcnow(),
        )

        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        embed.set_footer(
            text=self.BOT.user.name + " - requested by " + str(interaction.author),
            icon_url=interaction.author.display_avatar.url,
        )

        strBatDict = f"""Niveau : `{batDict["niveau"]}`
Dernière amélioration : `{datetime.datetime.utcfromtimestamp(batDict["derniere_upgrade"])}`
"""
        if nameMap[batLabel][0] == "production":
            strBatDict += f"Ressources contenues : `{batDict['contenu']}`"
        embed.add_field(name="Informations générales : ", value=strBatDict)
        await interaction.response.send_message(embed=embed)


class DropdownView(disnake.ui.View):
    def __init__(self, bot):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(bot))


class TownCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="town",
        description="Affiche votre village et permet d'améliorer vos bâtiments.",
        test_guilds=CONFIG.test_guilds,
    )
    async def town(
        self, inter, member: disnake.Member = Param(lambda inter: inter.author)
    ):
        """Affiche votre village ou celui d'un autre utilisateur. Commande principale à partir de laquelle on peut accéder aux autres bâtiments et les améliorer"""

        userData = database.getUserData(member.id)

        embed = disnake.Embed(
            title=f"Ville de {member}",
            description="",
            timestamp=datetime.datetime.utcnow(),
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(
            text=self.bot.user.name + " - requested by " + str(inter.author),
            icon_url=inter.author.display_avatar.url,
        )
        generalString = f""":star: XP : `{userData["profil"]["experience"]}`
:fishing_pole_and_fish: canne à pêche : `{userData["capacites"]["canne_a_peche"]}`
"""
        embed.add_field(name="Général", value=generalString, inline=True)

        #         statsString = f""":muscle: Attaque : `{userData["capacites"]["attaque"]}`
        # :shield: Défense : `{userData["capacites"]["defense"]}`
        # :dash: Vitesse : `{userData["capacites"]["vitesse"]}`
        # :dart: Précision : `{userData["capacites"]["precision"]}`
        # """
        #         embed.add_field(name="Capacités", value = statsString, inline=True)

        ressourceString = f""":coin: Or : `{userData["ressources"]["or"]}`
:gem: Diamants : `{userData["ressources"]["diamant"]}`
:wood: Bois : `{userData["ressources"]["bois"]}`
:rock: Pierre : `{userData["ressources"]["pierre"]}`
:nut_and_bolt: Métal : `{userData["ressources"]["metal"]}`
"""
        embed.add_field(name="Ressources", value=ressourceString, inline=True)

        productionString = f""":homes: Maisons : `{userData["production"]["maisons"]["niveau"]}`
:construction_site: Carrières : `{userData["production"]["carrieres"]["niveau"]}`
:hut: Scieries : `{userData["production"]["scieries"]["niveau"]}`
:factory: Fonderies : `{userData["production"]["fonderies"]["niveau"]}`
:mountain_snow: Mines de diamants : `{userData["production"]["mines"]["niveau"]}`
"""
        embed.add_field(
            name="Bâtiments de production", value=productionString, inline=True
        )

        boostString = f""":classical_building: Mairie : `{userData["boosts"]["mairie"]["niveau"]}`
:camping: Magasin de pêche : `{userData["boosts"]["magasin_de_peche"]["niveau"]}`
:convenience_store: Restaurant : `{userData["boosts"]["restaurant"]["niveau"]}`
:park: Camp d'entraînement : `{userData["boosts"]["camp_d_entrainement"]["niveau"]}`
"""
        embed.add_field(name="Bâtiments stratégiques", value=boostString, inline=True)

        embed.set_image(
            url="https://media.sketchfab.com/models/7c9b7638b74e4708869f048055c10e0f/thumbnails/92e33f5442704ffd886e137f20eb87f9/c22f2c6f552b4c9987e8fb4d9b6ccf36.jpeg"
        )

        view = DropdownView(self.bot)
        if member.id == inter.user.id:
            await inter.response.send_message(embed=embed, view=view)
        else:
            await inter.response.send_message(embed=embed)

        database.incrementCommandCount(inter.user.id)


def setup(bot):
    bot.add_cog(TownCommandsCog(bot))


# >o)
# (_> HM

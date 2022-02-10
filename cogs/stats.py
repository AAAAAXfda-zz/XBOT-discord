# modules API Discord
import disnake
from disnake import player
from disnake import file
from disnake.ext import commands, tasks
from disnake.ext.commands import Param

# modules perso
from configcreator import Config
import database

# autres modules
import datetime
import platform
import psutil
import sys
import os
import csv
from matplotlib.figure import Figure
from io import BytesIO


CONFIG = Config()


async def getEmbed(name, bot, member, interaction):

    userData = database.getUserData(member.id)

    emojisDico = {"Serveur": "🖥️", "Utilisateur": "👤", "Bot": "🤖", "Jeu": "🎮"}
    imagesDico = {
        "Serveur": interaction.guild.icon.url,
        "Utilisateur": member.display_avatar.url,
        "Bot": bot.user.display_avatar.url,
        "Jeu": "https://media.discordapp.net/attachments/889447462476087307/894217216118112277/9b805ec85ef4808bbf9e9f196c70c077.jpg",
    }

    embed = disnake.Embed(
        title=emojisDico[name] + "   " + name,
        description="",
        timestamp=datetime.datetime.utcnow(),
    )
    embed.set_thumbnail(url=imagesDico[name])
    embed.set_footer(
        text=bot.user.name + " - requested by " + str(interaction.author),
        icon_url=interaction.author.display_avatar.url,
    )

    if name == "Utilisateur":

        strStats = f""":alarm_clock: Création du compte : `{datetime.datetime.utcfromtimestamp(userData["stats"]["creation_du_compte"])}`
        :fishing_pole_and_fish: Poissons pêchés : `{userData["stats"]["poissons_peches"]}`
        :keyboard: Commandes utilisées : `{userData["stats"]["commandes_utilisees"]}`
        """
        embed.add_field(name="Stats", value=strStats)

    elif name == "Bot":
        uptime = int(datetime.datetime.utcnow().timestamp() - CONFIG.boottime)
        min, sec = divmod(uptime, 60)
        hours, min = divmod(min, 60)

        embed.add_field(
            name="Informations système :",
            value=f""":penguin: OS : `{platform.platform()}`
        :snake: Python Version : `{sys.version}`
        :alarm_clock: Bot uptime : `{int(hours)}h{int(min)}m{int(sec)}s`
        """,
            inline=False,
        )
        embed.add_field(
            name="Performance :",
            value=f""":memo: System CPU usage : `{psutil.cpu_percent()}`%
        :file_cabinet: System RAM usage : `{round(psutil.virtual_memory().used / (1024.0**3),2)}`GB/`{round(psutil.virtual_memory().total / (1024.0**3),2)}`GB (`{psutil.virtual_memory()[2]}`%)
        :file_cabinet: RAM used by the program : `{round(psutil.Process(os.getpid()).memory_info()[0] / (1024.0**3),2)}`GB
        :floppy_disk: Disk usage : `{round(psutil.disk_usage('/').used / (1024.0**3),2)}`GB/`{round(psutil.disk_usage('/').total / (1024.0**3),2)}`GB (`{psutil.disk_usage('/').percent}`%)
        """,
            inline=False,
        )

    elif name == "Serveur":

        serverStatsStr = f"""Nom : **{interaction.guild.name}**
        Id : `{interaction.guild.id}`
        Nombre de membres : `{interaction.guild.member_count}`
        Salons : `{len(interaction.guild.text_channels)}` textuels, `{len(interaction.guild.voice_channels)}` vocaux.
        Propriétaire : `{interaction.guild.owner_id}`
        Créé le : `{interaction.guild.created_at}`
        """
        embed.add_field(name="Général", value=serverStatsStr)

    elif name == "Jeu":

        fullDb = database.getDatabase()
        nombreCommandes = sum(i["stats"]["commandes_utilisees"] for i in fullDb)

        jeuStatsStr = f""":people_wrestling: Nombre de joueurs : {len(fullDb)}
        :satellite: Commandes utilisées : {nombreCommandes}
        """

        embed.add_field(name="Général", value=jeuStatsStr)

        playerCount = []
        serverCount = []
        commandCount = []
        time = []

        with open("stats.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")

            for row in csv_reader:
                playerCount.append(int(row[1]))
                time.append(datetime.datetime.utcfromtimestamp(int(row[0])))
                serverCount.append(int(row[2]))
                commandCount.append(int(row[3]))

        # sampling automatique des données pour toujours avoir entre 500 et 1000 valeurs.
        sampleSize = len(playerCount)
        try:
            # or any other value up to 1000, so it is in your specified limit
            step_size = sampleSize // 500
            playerCount = playerCount[::step_size]
            time = time[::step_size]
            serverCount = serverCount[::step_size]
            commandCount = commandCount[::step_size]
        except:
            pass

        fig = Figure()
        fig.set_size_inches(15, 11)
        axis = fig.subplots(3)

        fig.suptitle(
            f"Données mises à jour toutes les 12h. Sampling dynamique des données : {len(time)}/{sampleSize} valeurs"
        )

        axis[0].plot(time, playerCount)
        axis[0].grid(b=True)
        axis[0].set_title("Nombre de joueurs")
        axis[1].plot(time, serverCount)
        axis[1].grid(b=True)
        axis[1].set_title("Nombre de serveurs")
        axis[2].plot(time, commandCount)
        axis[2].grid(b=True)
        axis[2].set_title("Commandes utilisées")

        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)

        channel = bot.get_channel(894965795417907220)
        message = await channel.send(file=disnake.File(buf, "sample.png"))
        embed.set_image(url=message.attachments[0].url)

    return embed


class Dropdown(disnake.ui.Select):
    def __init__(self, bot, member):
        self.bot = bot
        self.member = member

        options = [
            disnake.SelectOption(
                label="Utilisateur",
                description="Des informations par rapport à l'utilisateur spécifié.",
                emoji="👤",
            ),
            disnake.SelectOption(
                label="Serveur",
                description="Des informations par rapport au serveur.",
                emoji="🖥️",
            ),
            disnake.SelectOption(
                label="Bot",
                description="Des informations par rapport au bot.",
                emoji="🤖",
            ),
            disnake.SelectOption(
                label="Jeu",
                description="Des informations par rapport au jeu.",
                emoji="🎮",
            ),
        ]

        super().__init__(
            placeholder="Sélectionnez un menu",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):

        statLabel = self.values[0]

        await interaction.response.edit_message(
            embed=await getEmbed(statLabel, self.bot, self.member, interaction)
        )


class DropdownView(disnake.ui.View):
    def __init__(self, bot, member):
        super().__init__()

        self.add_item(Dropdown(bot, member))


class StatsCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="stats",
        description="Affiche des statistiques par rapport aux utilisateurs, au serveur, au bot et au jeu.",
        test_guilds=CONFIG.test_guilds,
    )
    async def stats(
        self, inter, member: disnake.Member = Param(lambda inter: inter.author)
    ):
        """Affiche des stats par rapport aux utilisateurs, au serveur, au bot et au jeu"""

        userData = database.getUserData(member.id)

        view = DropdownView(self.bot, member)

        embed = await getEmbed("Utilisateur", self.bot, member, inter)

        await inter.response.send_message(
            embed=embed,
            view=view,
        )

        database.incrementCommandCount(inter.user.id)

    @tasks.loop(seconds=60 * 60 * 24)
    async def statsWriter(self):

        allData = database.getDatabase()
        playerNumber = len(allData)
        servers = len(self.bot.guilds)
        nombreCommandes = sum(i["stats"]["commandes_utilisees"] for i in allData)
        stats = [
            int(datetime.datetime.utcnow().timestamp()),
            playerNumber,
            servers,
            nombreCommandes,
        ]
        with open("stats.csv", encoding="utf-8", mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(stats)
        print(
            f"{datetime.datetime.now()} | Stockage des stats dans le document csv effectué avec succès."
        )


def setup(bot):
    bot.add_cog(StatsCommandsCog(bot))


# >o)
# (_> HM

# modules API discord. Disnake est un fork de discord.py qui supporte les slash commands.
import disnake  # le module Disnake
from disnake.ext import (
    commands,
)  # l'extension du module Disnake qui gère les commandes (equivalent rewrite)

# modules perso
from configcreator import (
    Config,
)  # importe les variables qui contiennent la configuration du bot stockée dans un JSON
import database  # importe les bindings avec l'API TinyDB (pour le moment)

# autres modules
import datetime  # gestion des dates/heures. Ici utilisé pour les timestamps des embeds


# on stocke un objet config dans une variable globale
CONFIG = Config()

# la liste des extensions à charger. Pour désactiver une extension, il suffit de le retirer de cette liste (=commenter la ligne correspondante).
# les extensions sont stockées dans le dossier 'cogs'. Ils doivent respecter une syntaxe spécifique pour être chargés
extensions = [
    "cogs.profile",
    "cogs.fish",
    "cogs.help",
    "cogs.stats",
    "cogs.town",
    "cogs.trade",
    "cogs.db",
]

# on créée l'objet bot. Le prefixe est vide car on utilise uniquement les commandes slash.
# ici on enregistre les commandes uniquement dans les guildes de test définies dans la config. On pourra plus tard les enregistrer globalement.
bot = commands.Bot(command_prefix="mmoV2!", test_guilds=CONFIG.test_guilds)

# on charge les extensions
for ext in extensions:
    bot.load_extension(ext)
    print(f"successfully loaded extension {ext}")


@bot.event
async def on_ready():
    """Se lance quand le bot est prêt à être utilisé."""

    bot.cogs["StatsCommandsCog"].statsWriter.start()
    print("Boucle de stockage des stats commencée.")
    print("READY !")


@bot.slash_command(
    name="ping",
    description="vérifie la latence du bot !",
    test_guilds=CONFIG.test_guilds,
)
async def ping(inter):
    """Une commande simple qui permet de vérifier la latence du bot.
    Elle utilise la valeur de latence fournie par l'API au lieu de la calculer."""

    embed = disnake.Embed(
        title="PONG :ping_pong:",
        description="Je suis en ligne ! :signal_strength:",
        timestamp=datetime.datetime.utcnow(),
    )
    embed.set_thumbnail(url=inter.author.display_avatar.url)
    embed.set_footer(
        text=bot.user.name + " - invoqué by " + str(inter.author),
        icon_url=inter.author.display_avatar.url,
    )
    embed.add_field(
        name="Latence",
        value=f"{round(bot.latency*1000, 2)} millisecondes.",
        inline=False,
    )

    await inter.response.send_message(embed=embed)

    # on ajoute cette ligne pour augmenter le nombre de commandes utilisées par l'utilisateur, visible dans les stats.
    database.incrementCommandCount(inter.user.id)


# on charge le token contenu dans un fichier à part et on lance le bot.
with open("token.txt") as token_file:
    TOKEN = token_file.read()
bot.run(TOKEN)


# >o)
# (_> HM

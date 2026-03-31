import discord
from discord.ext import tasks
from datetime import datetime, timedelta
import pytz
import os
import calendar
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
     return "Bot de ñoquis activo 🍝"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()


TOKEN = os.getenv("DISCORD_TOKEN")
CANAL_ID = 831719572201275424

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

argentina = pytz.timezone("America/Argentina/Buenos_Aires")

ultimo_mensaje = None


def dias_hasta_noquis():
    ahora = datetime.now(argentina)
    hoy = ahora.date()

    if hoy.day == 29:
        return 0

    if hoy.day < 29:
        proximo = hoy.replace(day=29)
    else:
        mes = hoy.month + 1
        año = hoy.year

        if mes == 13:
            mes = 1
            año += 1

        proximo = datetime(año, mes, 29).date()

    return (proximo - hoy).days


@tree.command(
    name="cuantofaltaparanioquis", description="Dice cuántos días faltan para el 29 🍝"
)
async def cuantofaltan(interaction: discord.Interaction):
    dias = dias_hasta_noquis()

    if dias == 0:
        mensaje = "🍝 Hoy comemos ñoquis! Con amor, Agus"
    elif dias == 1:
        mensaje = "🍝 Falta 1 día para volver a comer ñoquis. Con amor, Agus"
    else:
        mensaje = f"🍝 Faltan {dias} días para volver a comer ñoquis. Con amor, Agus"

    await interaction.response.send_message(mensaje)


@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot conectado como {client.user}")
    chequeo.start()


@tasks.loop(minutes=1)
async def chequeo():
    global ultimo_mensaje

    ahora = datetime.now(argentina)

    if ahora.hour == 10 and ahora.minute == 0:
        if ultimo_mensaje == ahora.date():
            return

        canal = client.get_channel(CANAL_ID)

        if canal:
            if ahora.day == 28:
                await canal.send(
                    "🍝 Atención! Mañana es 29, día de ñoquis. Acordate de comprarlos! Con amor, Agus"
                )

            if ahora.day == 29:
                await canal.send("🍝 Hoy es día de ñoquis! Con amor, Agus")

        ultimo_mensaje = ahora.date()


keep_alive()
client.run(TOKEN)

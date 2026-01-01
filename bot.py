import discord
from discord import app_commands
from discord.ext import commands
import json
import os

TOKEN = "MTQ1NjQwNTQ5NzIyODgyMDY0Mg.GrzhgM.wrqLADNSTxRfursTw4I5aJy8O4N2qrxOlLlceo"

INTENTS = discord.Intents.default()
INTENTS.members = True

bot = commands.Bot(command_prefix="!", intents=INTENTS)

DATA_FILE = "aura_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"AuraBOT conectado como {bot.user}")


def get_user_aura(user_id):
    data = load_data()
    return data.get(str(user_id), 0)


def set_user_aura(user_id, value):
    data = load_data()
    data[str(user_id)] = value
    save_data(data)


# 🔮 Comando: /auraad
@bot.tree.command(name="auraad", description="Adiciona ou remove Aura de um usuário")
@app_commands.describe(usuario="Usuário alvo", valor="Use +n ou -n")
async def auraad(interaction: discord.Interaction, usuario: discord.Member, valor: str):
    if not (valor.startswith("+") or valor.startswith("-")):
        await interaction.response.send_message(
            "Use o formato **+n** ou **-n** (ex: +5, -3).", ephemeral=True
        )
        return

    try:
        quantidade = int(valor)
    except ValueError:
        await interaction.response.send_message("Valor inválido.", ephemeral=True)
        return

    aura_atual = get_user_aura(usuario.id)
    nova_aura = aura_atual + quantidade
    set_user_aura(usuario.id, nova_aura)

    await interaction.response.send_message(
        f"✨ Aura de **{usuario.display_name}** agora é **{nova_aura}**"
    )


# 🔍 Comando: /aura
@bot.tree.command(name="aura", description="Mostra a Aura de um usuário")
@app_commands.describe(usuario="Usuário")
async def aura(interaction: discord.Interaction, usuario: discord.Member):
    aura = get_user_aura(usuario.id)
    await interaction.response.send_message(
        f"🔮 **Aura de {usuario.display_name}: {aura}**"
    )


# 🏆 Comando: /rank
@bot.tree.command(name="rank", description="Mostra o ranking de Aura do servidor")
async def rank(interaction: discord.Interaction):
    data = load_data()

    if not data:
        await interaction.response.send_message("Nenhum dado de Aura ainda.")
        return

    ranking = sorted(data.items(), key=lambda x: x[1], reverse=True)

    mensagem = "🏆 **Ranking de Aura** 🏆\n\n"
    for i, (user_id, aura) in enumerate(ranking[:10], start=1):
        user = interaction.guild.get_member(int(user_id))
        if user:
            mensagem += f"**{i}. {user.display_name}** — {aura}\n"

    await interaction.response.send_message(mensagem)


bot.run(TOKEN)

import discord
from discord.ext import commands
import requests
import pyttsx3

TOKEN = "token" # Substitua pelo seu token do bot

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

engine = pyttsx3.init()


voices = engine.getProperty("voices")

for voice in voices:
    if "brazil" in voice.id.lower() or "portuguese" in voice.id.lower():
        engine.setProperty("voice", voice.id)
        break


def speak(text):
    engine.say(text)
    engine.runAndWait()


def traduzir(texto):
    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": texto,
        "langpair": "en|pt-BR"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["responseData"]["translatedText"]

    return texto


def get_fact():
    url = "https://uselessfacts.jsph.pl/random.json"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        print(data)

        fact = data["text"]

        fact = traduzir(fact)

        return fact

    return None


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


@bot.command()
async def start(ctx):
    await ctx.send(
        f"Olá, {ctx.author.mention}! Bem vindo ao servidor!"
    )


@bot.command()
async def fact(ctx):
    fact = get_fact()

    if fact is not None:
        await ctx.send(f"Curiosidade: {fact}")

        speak(fact)

    else:
        await ctx.send(
            "Nao consegui buscar uma curiosidade agora."
        )

bot.run("token") #coloque seu token do bot aqui
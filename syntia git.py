import discord
import google.generativeai as genai
from discord.ext import commands
from google.api_core import exceptions

# --- CONFIGURATION (REMPLIS BIEN TES CLÉS) ---
# Le token vient de l'onglet "Bot" > bouton "Reset Token"
DISCORD_TOKEN = "" 
GOOGLE_API_KEY = ""

# --- LE CERVEAU ---
SYSTEM_INSTRUCTION = """
Tu es un expert business et finance.
Tu donnes des conseils pragmatiques pour faire de l'argent (IA, SaaS, Freelance).
Tes réponses sont claires, courtes et structurées.
"""

# --- CONNEXION À GEMINI ---
genai.configure(api_key=GOOGLE_API_KEY)
# On garde 'gemini-flash-latest' car c'est celui qui marche pour toi
model = genai.GenerativeModel('gemini-flash-latest', system_instruction=SYSTEM_INSTRUCTION)

# --- CONFIGURATION DISCORD ---
intents = discord.Intents.default()
intents.message_content = True  # Indispensable pour lire les messages !
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot connecté : {bot.user.name}')
    print('🚀 Prêt à répondre sur le serveur !')

@bot.command(name="biz")
async def business_advice(ctx, *, question):
    # Le bot montre qu'il écrit...
    async with ctx.typing():
        try:
            # On envoie la question à l'IA
            response = model.generate_content(question)
            text = response.text

            # Si le message est trop long pour Discord (+2000 caractères), on le coupe
            if len(text) > 2000:
                for i in range(0, len(text), 2000):
                    await ctx.send(text[i:i+2000])
            else:
                await ctx.send(text)

        except exceptions.ResourceExhausted:
            await ctx.send("🛑 Pause ! Je réfléchis trop vite (Limite gratuite atteinte).")
        except Exception as e:
            print(f"Erreur : {e}")
            await ctx.send("Oups, j'ai eu un bug technique.")

# Lancement
bot.run(DISCORD_TOKEN)
import discord
import os
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio

# -----------------------------
# Discord bot setup
# -----------------------------
intents = discord.Intents.default()
intents.members = True  # needed to manage roles
bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
# Environment variables
# -----------------------------
GUILD_ID = int(os.getenv("GUILD_ID"))  # your server ID
VERIFIED_ROLE_ID = int(os.getenv("VERIFIED_ROLE_ID"))  # Verified role ID
ANSWER_KEY = os.getenv("ANSWER_KEY")  # secret key users must type
BOT_TOKEN = os.getenv("BOT_TOKEN")  # bot token

# -----------------------------
# Bot events
# -----------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# -----------------------------
# Verification command
# -----------------------------
@bot.slash_command(description="Verify yourself to access private channels")
async def verify(ctx):
    try:
        await ctx.author.send("Welcome! Please enter the answer key:")

        def check(msg):
            return msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel)

        msg = await bot.wait_for("message", check=check, timeout=120)
        if msg.content.strip() == ANSWER_KEY:
            guild = bot.get_guild(GUILD_ID)
            role = guild.get_role(VERIFIED_ROLE_ID)
            member = guild.get_member(ctx.author.id)
            if role not in member.roles:
                await member.add_roles(role)
            await msg.channel.send("✅ Verified! You now have access to the private channel.")
        else:
            await msg.channel.send("❌ Incorrect key. Try again later.")
    except asyncio.TimeoutError:
        await ctx.author.send("⌛ Time's up. Please use /verify again.")
    except discord.errors.Forbidden:
        print(f"Cannot add role to {ctx.author}, check permissions.")

# -----------------------------
# Flask server to keep bot alive
# -----------------------------
app = Flask("")

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run_flask).start()

# -----------------------------
# Run bot safely
# -----------------------------
async def main():
    await bot.start(BOT_TOKEN)

# Use asyncio.run for better rate-limit handling
asyncio.run(main())

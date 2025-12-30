import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = int(os.getenv("GUILD_ID"))
VERIFIED_ROLE_ID = int(os.getenv("VERIFIED_ROLE_ID"))
ANSWER_KEY = os.getenv("ANSWER_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(description="Verify yourself to access private channels")
async def verify(ctx):
    await ctx.author.send("Enter the answer key:")

    def check(msg):
        return msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel)

    try:
        msg = await bot.wait_for("message", check=check, timeout=120)
        if msg.content.strip() == ANSWER_KEY:
            guild = bot.get_guild(GUILD_ID)
            role = guild.get_role(VERIFIED_ROLE_ID)
            member = guild.get_member(ctx.author.id)
            await member.add_roles(role)
            await msg.channel.send("✅ Verified! Access granted.")
        else:
            await msg.channel.send("❌ Wrong key. Try later.")
    except:
        await ctx.author.send("⌛ Time’s up. Use /verify again.")

bot.run(BOT_TOKEN)

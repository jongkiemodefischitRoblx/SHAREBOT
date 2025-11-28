import discord
from discord.ext import commands

# ================== CONFIG ==================
TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
DEFAULT_IMAGE = "https://files.catbox.moe/44jbtv.webp"
# ============================================

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Simpan channel yang di-lock: guild_id -> {channel_id, owner_id}
auto_share_channels = {}

# ---------- READY EVENT ----------
@bot.event
async def on_ready():
    print(f"SHAREBOT is online as {bot.user}")
    print("Owner AutoShare ready!")

# ---------- /autoshare COMMAND ----------
@bot.command()
async def autoshare(ctx, channel: discord.TextChannel):
    auto_share_channels[ctx.guild.id] = {
        "channel_id": channel.id,
        "owner_id": ctx.author.id
    }
    await ctx.send(f"✅ Channel {channel.mention} has been locked for auto-share by {ctx.author.mention}.")

# ---------- AUTO-SHARE LINKS ----------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

    guild = message.guild
    if not guild:
        return

    guild_id = guild.id
    if guild_id not in auto_share_channels:
        return

    owner_id = auto_share_channels[guild_id]["owner_id"]
    if message.author.id != owner_id:
        return

    channel_id = auto_share_channels[guild_id]["channel_id"]
    target_channel = guild.get_channel(channel_id)
    if not target_channel:
        return

    urls = [word for word in message.content.split() if word.startswith("http://") or word.startswith("https://")]
    if not urls:
        return

    for url in urls:
        embed = discord.Embed(description=f"{url}\nShared by: {message.author.mention}")
        embed.set_image(url=DEFAULT_IMAGE)
        await target_channel.send(content="@everyone", embed=embed)

bot.run(TOKEN)

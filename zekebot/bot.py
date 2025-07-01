import discord
from discord import app_commands
import aiohttp
import asyncio

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash commands synced.")

    async def on_ready(self):
        print(f"🤖 Bot ready as {self.user}")

client = MyClient()

# /mod command
@client.tree.command(name="mod", description="Moderate: warn, ban, kick, unban, or clear messages.")
@app_commands.describe(
    action="Choose 'warn', 'ban', 'kick', 'unban', or 'clear'",
    user="User to act on",
    amount="Number of messages to clear (for 'clear')",
    reason="Reason for moderation"
)
async def mod_command(interaction: discord.Interaction, action: str, user: discord.User = None, amount: int = 0, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("🚫 Only admins can use this command.", ephemeral=True)
        return

    action = action.lower()
    valid = ["warn", "ban", "kick", "unban", "clear"]
    if action not in valid:
        await interaction.response.send_message(f"❌ Invalid action. Use one of: {', '.join(valid)}", ephemeral=True)
        return

    try:
        if action == "warn":
            if not user or user.id == client.user.id:
                await interaction.response.send_message("⚠️ Mention a valid user to warn.", ephemeral=True)
                return
            try:
                await user.send(f"⚠️ You have been **warned** in **{interaction.guild.name}**.\nReason: {reason}")
                await interaction.response.send_message(f"🟠 {user.mention} warned (DM sent).", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message(f"🚫 Couldn't DM {user.mention}.", ephemeral=True)

        elif action == "ban":
            if not user:
                await interaction.response.send_message("⚠️ Specify a user to ban.", ephemeral=True)
                return
            member = interaction.guild.get_member(user.id)
            if member:
                await member.ban(reason=reason)
                await interaction.response.send_message(f"🔨 {user.mention} banned.\nReason: {reason}", ephemeral=True)
            else:
                await interaction.response.send_message("❗ That user isn't in the server.", ephemeral=True)

        elif action == "kick":
            if not user:
                await interaction.response.send_message("⚠️ Specify a user to kick.", ephemeral=True)
                return
            member = interaction.guild.get_member(user.id)
            if member:
                await member.kick(reason=reason)
                await interaction.response.send_message(f"👢 {user.mention} kicked.\nReason: {reason}", ephemeral=True)
            else:
                await interaction.response.send_message("❗ That user isn't in the server.", ephemeral=True)

        elif action == "unban":
            if not user:
                await interaction.response.send_message("⚠️ Specify a user to unban.", ephemeral=True)
                return
            try:
                entry = await interaction.guild.fetch_ban(user)
                await interaction.guild.unban(entry.user, reason=reason)
                await interaction.response.send_message(f"✅ {user} unbanned.\nReason: {reason}", ephemeral=True)
            except discord.NotFound:
                await interaction.response.send_message("❌ That user is not banned.", ephemeral=True)

        elif action == "clear":
            if amount <= 0 or amount > 100:
                await interaction.response.send_message("⚠️ Enter a number from 1 to 100.", ephemeral=True)
                return
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.response.send_message(f"🧹 Cleared {len(deleted)} messages.", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"🚨 Error: `{e}`", ephemeral=True)

# /memes command
@client.tree.command(name="memes", description="Fetch a random meme from Reddit")
async def memes_command(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    url = "https://meme-api.com/gimme"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                embed = discord.Embed(title=data["title"], url=data["postLink"])
                embed.set_image(url=data["url"])
                embed.set_footer(text=f"👍 {data['ups']} | r/{data['subreddit']}")
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send("😢 Couldn't fetch meme.", ephemeral=True)

# /help command
@client.tree.command(name="help", description="List available commands.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🧰 ZekeBot Commands",
        description="Here's what I can do!",
        color=discord.Color.blurple()
    )
    embed.add_field(name="/mod", value="Moderate users: warn, ban, kick, unban, clear", inline=False)
    embed.add_field(name="/memes", value="Grab a meme from Reddit", inline=False)
    embed.add_field(name="/source", value="View the source code", inline=False)
    embed.add_field(name="/help", value="Show this help menu", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /source command (updated GitHub link)
@client.tree.command(name="source", description="Get the bot's source code link.")
async def source_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📂 ZekeBot Source Code",
        description="Here's where to find the project files:",
        color=discord.Color.green()
    )
    embed.add_field(name="📦 GitHub", value="[View Source Code](https://github.com/zeke-youtube/zekeserver/blob/main/zekebot/bot.py)", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Token loader for Windows
with open("C:/Users/Zeke Cheng/OneDrive/Desktop/token.txt", "r") as file:
    token = file.read().strip()

# Launch the bot
async def main():
    async with client:
        await client.start(token)

asyncio.run(main())


# 1. Respond to messages
# 2. Manage members roles - ask for an upgrade to a member role and then the bot can do it for them
# 3. Stay online all the time

from dotenv import load_dotenv
load_dotenv()
import os
import discord # discord.py
from discord import app_commands
from datetime import datetime, timezone

class BotClient(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)

    def setTree(self, tree):
        self.commandTree = tree

    async def on_ready(self):
        await self.commandTree.sync(guild=discord.Object(id=guildId))
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'marco':
            await message.channel.send('polo')

intents = discord.Intents().all()
print("intents")
print(intents)
intents.message_content = True
intents.members = True
intents.guilds = True
intents.moderation = True
print(intents)
client = BotClient(intents=intents)
tree = app_commands.CommandTree(client)
client.setTree(tree)

@tree.command(name="upgrade", description="Upgrade", guild=discord.Object(id=guildId))
async def upgrade(interaction):
    # member = interaction.user
    # memberJoinDate = member.joined_at
    # daysSinceJoined = (datetime.now(timezone.utc) - memberJoinDate).days
    # if daysSinceJoined >= 0:
    role = discord.utils.get(interaction.guild.roles, name="Member")
    await interaction.user.add_roles(role, atomic=True)
    await interaction.response.send_message("Upgraded!")
    # else:
    #     await interaction.response.send_message("You must have joined at least 3 days ago!")


client.run("TOKEN") # or... os.getenv("DISCORD_API_TOKEN")
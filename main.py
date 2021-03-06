import discord
from discord.channel import CategoryChannel, TextChannel, VoiceChannel
from dotenv import load_dotenv
import os


TOKEN = "ODgyMjgzNDMxNjg0MzY2MzU2.YS5Ieg.XplBonhhyQjeK9TrJHRaXypt1p8"
LIST_REACTIONS = {'๐','๐ฎ','๐'}
LIST_GUILDS = []
LIST_TEXT_CHANNELS = []
LIST_VOICE_CHANNELS = []
LIST_CATEGORIES = []
LIST_ROLES = []
myGuildName = "RFCorp"

if __name__ == "__main__":

    client = discord.Client()

    def get_guild(name):
        return next((x for x in LIST_GUILDS if x.name == name), None)

    def get_text_channel(name):
        return next((x for x in LIST_TEXT_CHANNELS if x.name == name), None)

    def get_voice_channel(name):
        return next((x for x in LIST_VOICE_CHANNELS if x.name == name), None)

    def get_category(name):
        return next((x for x in LIST_CATEGORIES if x.name == name), None)
        
    def get_category(name):
        return next((x for x in LIST_CATEGORIES if x.name == name), None)

    def get_role(name):
        return next((x for x in LIST_ROLES if x.name == name), None)

    def fill_list():
        guilds = client.guilds
        for guild in guilds:
            LIST_GUILDS.append(guild)
            for channel in guild.channels:
                if (type(channel) is TextChannel):
                    LIST_TEXT_CHANNELS.append(channel)
                elif (type(channel) is VoiceChannel):
                    LIST_VOICE_CHANNELS.append(channel)
                elif (type(channel) is CategoryChannel):
                    LIST_CATEGORIES.append(channel)
            for role in guild.roles:
                LIST_ROLES.append(role)


    @client.event
    async def on_ready():
        print(client.user)
        fill_list()
        channel_rf = get_text_channel("rf๐")
        channel_ue = get_text_channel("uber-eats๐ฎ")
        channel_mcdo = get_text_channel("mc-do๐")
        message = "Pour ouvrir un ticket, veuillez rรฉagir ร  ce message :\n\n\
            ๐ -> Ouvrir un ticket " + channel_rf.mention + "\n\
            ๐ฎ -> Ouvrir un ticket " + channel_ue.mention + "\n\
            ๐ -> Ouvrir un ticket " + channel_mcdo.mention + "\n\
                "
            
        channel = get_text_channel("ticket๐ฉ")
        messages = await channel.history(limit=2000).flatten()
        await channel.delete_messages(messages)
        msg = await channel.send(message)
        await msg.add_reaction("๐")
        await msg.add_reaction("๐ฎ")
        await msg.add_reaction("๐")

    @client.event
    async def on_reaction_add(reaction:discord.Reaction, user:discord.User):
        if (user.bot):
            return
        if (reaction.emoji == '๐'):
            await create_ticket(user, "RF-" + user.name, get_role("Boss du RF"), "Quelle boutique et quel produit veux-tu te faire rembourser ? ๐")
        elif (reaction.emoji == '๐ฎ'):
            await create_ticket(user, "UE-" + user.name, get_role("Boss du UE"), "Alors รงa veut s'enfiler un petit Uber Eats ? ๐ฎ")
        elif (reaction.emoji == '๐'):
            await create_ticket(user, "MCDO-" + user.name, get_role("Boss du McDo"), "Alors รงa veut s'enfiler un petit Mac Do ? ๐")
        else:
            await reaction.remove(user)
        

    async def create_ticket(user:discord.User, name, role:discord.Role, message):
        category = get_category("โโฑโโโโโโโธ๐โธโโโโโโโฐโ")
        guild = get_guild(myGuildName)
        name = str.lower(name)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        if any(textChannel.name == name for textChannel in guild.text_channels):
            print("Ticket dรฉjร  existant : " + name)
        else:
            channel = await guild.create_text_channel(name, overwrites=overwrites, category=category)
            await channel.send(user.mention + " Bienvenue ! ๐\n" + message)
            print("Ticket crรฉe : " + name)

    load_dotenv()
    client.run(os.getenv("TOKEN"))

import discord
from discord.ext import commands, tasks
from discord import app_commands, Interaction
import Config
from Config import PrintEx

class Client(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    async def CalculateMembers(self, guild_id: int):  # Calculate server members; guild_id = Your Server ID;
        guild = self.bot.get_guild(guild_id) # Finding the server by it's id
        
        if guild is not None: # If bot find any guild by the id
            member_count = len(guild.members) # fetch the members
            return member_count # return the members
        
    async def MembersUpdate(self, members: int, channel_id: int): # This function is connected with CalculateMembers. First "CalculateMembers(guild_id)" calculate members then retrun the amount.
        """
        members = your server member or you can input any int value;
        channel_id = Id of a channel which you use for the status 
        """
        channel = self.bot.get_channel(channel_id) # Finding the channel
        if channel is not None: # If Channel is true
            return await channel.edit(name=f"Members: {members}") # Update the value(Channel Name)
        else:
            return PrintEx(f"Wrong Channel ID cannot update members. ID: ({channel_id})")
    # Loop Functions
    @tasks.loop(minutes= 2)
    async def UpdateStatus(self, guild_id: int, channel_id: int):
        """
        Loop repeat in every 2 minutes
        """
        members = await self.CalculateMembers(guild_id)
        await self.MembersUpdate(members, channel_id)
        PrintEx("Updated Status")
        return
        
    @commands.Cog.listener()
    async def on_ready(self):
        VC = self.bot.get_channel(Config.VOICE)
        if VC:
            PrintEx(f"Found channel: {VC.name}")
            try:
                await VC.connect(self_deaf=True)
                PrintEx(f"Connected to {VC.name}")
            except Exception as e:
                PrintEx(f"Error connecting to {VC.name}: {e}")
        else:
            PrintEx(f"Channel with ID {Config.VOICE} not found.")
        self.UpdateStatus.start(Config.GUILD, Config.STATUS_CHANNEL)
        # Activity
        members = await self.CalculateMembers(guild_id= Config.GUILD)  # You should replace this with the actual member count
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"👤{members} Members")
        await self.bot.change_presence(activity=activity, status=discord.Status.do_not_disturb)
        return True
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        try:
            if message.content.startswith('<@1157707845052145765>'):
                bot_response = "Hi, Ami G-Code-X\nJoy Bangla, Joy Bongo Dudu.."
                # Send the bot's response back to the Discord channel
                await message.channel.send(bot_response)
        except Exception as e:
            PrintEx(e)
        return True
    
    @app_commands.command(name= "serverinfo", description= "Shows server informations")
    async def serverinfo(self, interact: Interaction):
        try:
            guild = self.bot.get_guild(interact.user.guild.id)
            owner = self.bot.get_user(guild.owner_id)
            formatted_date = guild.created_at.strftime('%d %b %Y')
            embed = discord.Embed(color= 0X850fbd, title= f"{guild.name} Information")
            embed.add_field(name="Owner", value= f"> {owner.mention}")
            embed.add_field(name="Created on", value=f"> {formatted_date}")
            embed.add_field(name="Members", value=f"> {len(guild.members)}")
            embed.add_field(name="Roles", value=f"> {len(guild.roles)}")
            embed.add_field(name="Channels", value=f"> {len(guild.channels)}")
            embed.add_field(name="Emojis", value=f"> {len(guild.emojis)}")
            embed.add_field(name="Description:", value=f"> **{guild.description}**")
            embed.set_thumbnail(url= guild.icon)
            await interact.response.send_message(embed= embed)
        except Exception as e:
            PrintEx(e)
        return True

    


async def setup(bot):
    await bot.add_cog(Client(bot))
    
import discord
from discord.ext import commands
import Config
from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp 
from Config import PrintEx

class Welcome(commands.Cog):
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
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Update status on member join
        members = await self.CalculateMembers(Config.GUILD)
        await self.MembersUpdate(members, Config.STATUS_CHANNEL)
        
        role = discord.utils.get(member.guild.roles, id= 1158093139509264454)
        await member.add_roles(role)

        try:
            #Pulling Banner
            welcome_img = Image.open("stuffs/welcome.png")
            welcome_img = welcome_img.convert("RGBA")
            img = welcome_img.copy()

            #Writing Member Name
            font = ImageFont.truetype(font= "sans-regular.ttf",size= 109)#Font Path
            draw = ImageDraw.Draw(img)
            text = f"{member.name}"
            text_bbox = draw.textbbox((0, 0), text, font=font)

            # Calculate the position to center the text
            image_width, image_height = welcome_img.size
            x = (image_width - text_bbox[2]) / 2
            y = 650
            draw.text((x, y), text, font=font, fill ="#65008a")

            #Pulling Members Avatar
            async with aiohttp.ClientSession() as session:
                async with session.get(str(member.avatar.url)) as rep:
                    avatar_data = await rep.read()
            with open("avatar.png", "wb") as f:
                f.write(avatar_data)

            avatar = Image.open("stuffs/avatar.png").convert('RGBA')
            mask_size = (462, 462)
            mask = Image.new('L', mask_size, 0)
            draw = ImageDraw.Draw(mask)
            width, height = mask_size
            draw.ellipse((0, 0, width, height), fill=255)
            avatar = avatar.resize(mask_size)
            img.paste(avatar, (969, 140), mask=mask)

            #Adding Image Border
            stroke = Image.open("stuffs/Stroke.png").convert("RGBA")
            stroke = stroke.resize((535 , 535))
            img.paste(stroke, (933 , 103), stroke)

            #Image Output
            buffer_output = io.BytesIO()
            img.save(buffer_output, format='PNG')
            buffer_output.seek(0)

            channel = self.bot.get_channel(1159796113092640840)
            await channel.send(content=f"<:supporter:1157967995738542091>  {member.mention} 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 {member.guild.name}\n───────────── • ◆ • ─────────────\n <:termssign:1157968025782333561>  𝐑𝐄𝐀𝐃 𝐑𝐔𝐋𝐄𝐒 𝐈𝐍 <#1157531058741465141> \n───────────── • ◆ • ─────────────\n <:member:1157635295429279784>  𝐓𝐀𝐊𝐄 𝐑𝐎𝐋𝐄 𝐈𝐍 <#1158328838812614706> \n───────────── • ◆ • ─────────────",file=discord.File(buffer_output, "welcome.png"))
        except Exception as e:
            print(e)
        return True
    
    async def on_member_remove(self, member):
        # Update status on member leave
        members = await self.CalculateMembers(Config.GUILD)
        await self.MembersUpdate(members, Config.STATUS_CHANNEL)
        return True

async def setup(bot):
    await bot.add_cog(Welcome(bot))
    
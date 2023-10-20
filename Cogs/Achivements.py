import discord
from discord.ext import commands, tasks
from discord import app_commands, Interaction
import random 
import aiohttp
from PIL import Image, ImageDraw, ImageFont
import io
from Config import PrintEx, ConnectToDatabase, GetSqlResult, GetUserSerial, sql_query
import Config
import datetime

class Achivements(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    """voice_channel_timers = {}
    @tasks.loop(seconds=10)  # Check every 1 minute (you can adjust this interval)
    async def check_voice_states(self):
        try:
            for member_id, start_time in list(self.voice_channel_timers.items()):
                member = self.bot.get_guild(Config.GUILD).get_member(member_id)
                if not member:
                    del self.voice_channel_timers[member_id]
                    continue

                voice_state = member.voice
                if not voice_state or not voice_state.channel:
                    del self.voice_channel_timers[member_id]
                    continue

                end_time = datetime.datetime.now()
                time_spent = end_time - start_time
                minutes_spent = time_spent.total_seconds() / 60
                await member.send(f"You have spent {minutes_spent:.2f} minutes in the voice channel.")
                print(f"{minutes_spent:.2f}")   
        except Exception as e:
            print(e)"""
        
    @commands.Cog.listener()
    async def on_ready(self):
        ConnectToDatabase()
        self.check_voice_states.start()
        return True
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.author.bot:
            return
        user = message.author
        guild = message.guild
        result = GetSqlResult(f"SELECT * FROM users WHERE user_id = {user.id}")
        if not result:
            sql_query(f"INSERT INTO `users` (`serial`, `guild_id`, `user_id`, `username`, `total_messages`, `total_voice`, `level`, `xp`) VALUES (NULL, '{guild.id}', '{user.id}', '{user.global_name}', '0', '0', '0', '0');")
        try:
            level = GetSqlResult(f"SELECT level FROM users WHERE serial = {GetUserSerial(user.id)}")
            xp = GetSqlResult(f"SELECT xp FROM users WHERE serial = {GetUserSerial(user.id)}")
            messages = GetSqlResult(f"SELECT total_messages FROM users WHERE serial = {GetUserSerial(user.id)}")

            try:
                level = level[0][0]  # Access the first element of the first tuple
                xp = xp[0][0]        # Access the first element of the first tuple
                messages = messages[0][0]  
            except IndexError:
                level = 0
                xp = 0
            messages += 1

            if messages == 5:
                channel = self.bot.get_channel(Config.ACHIVEMENT)
                await channel.send(content=f"{message.author.mention} Hurrah! You made it!", file= discord.File(fp="Rank-Banner/trophy-2.png", filename="image.png"))
            elif messages == 60:
                channel = self.bot.get_channel(Config.ACHIVEMENT)
                await channel.send(content="Hurrah! You made it!", file= discord.File("Rank-Banner/trophy-3.png", filename= "image.png"))   

            elif messages == 100:
                channel = self.bot.get_channel(Config.ACHIVEMENT)
                await channel.send(content="Hurrah! You made it!", file= discord.File("Rank-Banner/trophy-9.png", filename= "image.png"))   

            if level < 5:
                rand = int(len(message.content) / 25) + random.randint(1,2)
                xp += rand
                if xp >= 1000*(level+1):
                    
                    level += 1
                sql_query(f"UPDATE users SET xp = {xp}, level = {level}, total_messages = {messages}  WHERE serial = {GetUserSerial(user.id)}")
            else:
                rand = int(len(message.content) / 25) + random.randint(1,5)
                xp += rand
                if xp >= 1000*level:
                    level += 1
                sql_query(f"UPDATE users SET xp = {xp}, level = {level} WHERE serial = {GetUserSerial(user.id)}")
        except Exception as e:
            PrintEx(e)
        return True
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        try:
            if before.channel != after.channel:
                self.voice_channel_timers[member.id] = datetime.datetime.now()
                print("Done")
        except Exception as e:
            print(e)



    @app_commands.command(name= "level", description= "Show user level")
    async def level(self, interact:Interaction, user: discord.Member = None):
        try:
            if user is None:
                user = interact.user
            await interact.response.send_message("Searching user......")

            level = GetSqlResult(f"SELECT level FROM users WHERE serial = {GetUserSerial(user.id)}")
            xp = GetSqlResult(f"SELECT xp FROM users WHERE serial = {GetUserSerial(user.id)}")

            try:
                level = level[0][0]  # Access the first element of the first tuple
                xp = xp[0][0]        # Access the first element of the first tuple
            except IndexError:
                level = 0
                xp = 0
            
            final_xp = 1000*(level+1)

            # Load the background image
            background = Image.open("stuffs/lvl_banner.jpg").convert("RGBA")
            background = background.resize((1000, 240))

            async with aiohttp.ClientSession() as session:
                async with session.get(str(user.avatar.url)) as rep:
                    logo_data = await rep.read()
            with open("stuffs/logo.png", "wb") as f:
                f.write(logo_data)
            
            logo = Image.open("stuffs/logo.png").convert('RGBA')
            logo = logo.resize((200, 200))
            bigsize = (logo.size[0] * 3, logo.size[1] * 3)
            mask = Image.new("L", bigsize, 0)

            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, 255)

            mask = mask.resize(logo.size)
            logo.putalpha(mask)

            background.paste(logo, (20, 20), mask=logo)

            # Create a drawing context on the background image
            draw = ImageDraw.Draw(background)

            # Working with Fonts
            big_font = ImageFont.truetype("sans-regular.ttf", 60)
            medium_font = ImageFont.truetype("sans-regular.ttf", 40)
            small_font = ImageFont.truetype("sans-regular.ttf", 30)

            # Placing Right Upper Part
            text_size = draw.textbbox((0, 0), str(level), font=big_font)
            offset_x = 1000 - 15 - int(text_size[2])
            offset_y = 10
            draw.text((offset_x, offset_y), str(level), font=big_font, fill="#fff")

            text_size = draw.textbbox((0, 0), "LEVEL", font=small_font)
            offset_x -= int(text_size[2]) + 5
            draw.text((offset_x, offset_y + 27), "LEVEL", font=small_font, fill="#fff")

            # Empty Progress Bar (Gray)
            bar_offset_x = 320
            bar_offset_y = 170
            bar_offset_x_1 = 950
            bar_offset_y_1 = 200

            # Progress Bar
            draw.rounded_rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175", radius=9)

            # Filling Bar
            bar_length = bar_offset_x_1 - bar_offset_x 
            progress = (final_xp - xp) * 100 / final_xp
            progress = 100 - progress
            progress_bar_length = round(bar_length * progress / 100)
            bar_offset_x_1 = bar_offset_x + progress_bar_length

            # Progress Bar
            draw.rounded_rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#65008a", radius=9)

            text_size = draw.textbbox((0, 0), f"/ {final_xp} XP", font=small_font)
            offset_x = 950 - int(text_size[2])
            offset_y = bar_offset_y - text_size[3] - 10
            draw.text((offset_x, offset_y), f"/ {final_xp:,} XP", font=small_font, fill="#727175")

            text_size = draw.textbbox((0, 0), f"{xp:,}", font=small_font)
            offset_x -= int(text_size[2]) + 8
            draw.text((offset_x, offset_y), f"{xp:,}", font=small_font, fill="#fff")

            # Blitting Name

            text_size = draw.textbbox(xy= (0,0), text=user.global_name, font=medium_font)

            offset_x = bar_offset_x
            offset_y = bar_offset_y - text_size[3] - 5
            draw.text((offset_x, offset_y), user.global_name, font=medium_font, fill="#fff")

            #Image Output
            buffer_output = io.BytesIO()
            background.save(buffer_output, format='PNG')
            buffer_output.seek(0)
    
            await interact.delete_original_response()
            channel = interact.channel
            await channel.send(file=discord.File(buffer_output, "level.png"))
            return True
        except Exception as e:
            PrintEx(e)

async def setup(bot):
    await bot.add_cog(Achivements(bot))

    

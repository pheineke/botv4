import discord
from discord import app_commands
from discord.ext import commands, tasks
import json
import os
from datetime import datetime
import base64
from PIL import Image
from io import BytesIO

from lib.logger import Logger
logger = Logger()

class UserTimeTable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timetable_file = "lib/usertimetables.json"
        if not os.path.exists(self.timetable_file):
            with open(self.timetable_file, "w") as f:
                json.dump({}, f, indent=4)

    @app_commands.command(name="usertimetable", description="Get Timetable of a user")
    async def usertimetable(self, interaction: discord.Interaction, user: discord.User):
        with open(self.timetable_file, "r") as f:
            data = json.load(f)

        user_id = str(user.id)
        if user_id not in data:
            await interaction.response.send_message("This user does not have a timetable set.", ephemeral=True)
            return

        timetable_data = data[user_id]
        png_base64 = timetable_data["timetable"]
        png_bytes = base64.b64decode(png_base64)
        png_buffer = BytesIO(png_bytes)

        await interaction.response.send_message(
            content=f"Timetable for {user.name}",
            file=discord.File(png_buffer, filename="timetable.png"),
            ephemeral=True
        )
        png_buffer.close()
        

    @app_commands.command(name="my_timetable", description="Set your timetable")
    async def my_timetable(self, interaction: discord.Interaction, file: discord.Attachment):
        if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
            await interaction.response.send_message("Please upload a valid image file (PNG, JPG, JPEG).", ephemeral=True)
            return
        
        try:
            img = Image.open(BytesIO(await file.read()))
            png_buffer = BytesIO()
            img.save(png_buffer, format="WEBP", quality=100)

            png_bytes = png_buffer.getvalue()
            png_base64 = base64.b64encode(png_bytes).decode('utf-8')
            png_buffer.close()
        except Exception as e:
            logger.log(f"Error processing image: {e}")
            await interaction.response.send_message("There was an error processing the image.", ephemeral=True)
            return

        with open(self.timetable_file, "r") as f:
            data = json.load(f)

        user_id = str(interaction.user.id)
        if user_id not in data:
            data[user_id] = {
                "name": interaction.user.name,
                "timetable": png_base64
            }
            
        with open(self.timetable_file, "w") as f:
            json.dump(data, f, indent=4)
        await interaction.response.send_message("Your timetable has been set successfully!", ephemeral=True)

    @app_commands.command(name="timetables", description="Get all users that have a timetables")
    async def timetables(self, interaction: discord.Interaction):
        with open(self.timetable_file, "r") as f:
            data = json.load(f)
        if not data:
            await interaction.response.send_message("No users have set a timetable yet.", ephemeral=True)
            return
        
        txt = "Folgende User haben ein Timetable:\n"
        
        user_ids = list(data.keys())
        for user_id in user_ids:
            user = await self.bot.fetch_user(int(user_id))
            if user:
                txt += f"- {user.name}\n"
                
        await interaction.response.send_message(txt, ephemeral=True)



async def setup(bot):
    await bot.add_cog(UserTimeTable(bot))
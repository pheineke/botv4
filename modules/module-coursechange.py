import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime


from lib.logger import Logger
logger = Logger()

class CourseChange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = os.path.join('lib', 'coursechange.json')
        self.load_config()
        self.check_and_move_channels.start()

    def load_config(self):
        if not os.path.exists(self.config_file):
            self.config = {
                "TIME-FORMAT": "dd-mm",
                "SUMMER_TERM": {
                    "name": "Summer Term",
                    "start_date": "01-04",
                    "end_date": "30-09",
                    "CATEGORY_ID": "1105534816658669669"
                },
                "WINTER_TERM": {
                    "name": "Winter Term",
                    "start_date": "01-10",
                    "end_date": "31-03",
                    "CATEGORY_ID": "1065377828402643044"
                },
                "SUMMER_IDS": [],
                "WINTER_IDS": []
            }
            self.save_config()
        else:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    @tasks.loop(hours=24)
    async def check_and_move_channels(self):
        current_date = datetime.now().strftime("%d-%m")
        summer_start = datetime.strptime(self.config["SUMMER_TERM"]["start_date"], "%d-%m")
        summer_end = datetime.strptime(self.config["SUMMER_TERM"]["end_date"], "%d-%m")
        current = datetime.strptime(current_date, "%d-%m")

        if summer_start <= current <= summer_end:
            CURRENT_TERM = "SUMMER"
            STORAGE_TERM = "WINTER"
        else:
            CURRENT_TERM = "WINTER"
            STORAGE_TERM = "SUMMER"
            
        current_id = self.config["CURRENT_CATEGORY_ID"]
        storage_id = self.config["STORAGE_CATEGORY_ID"]

        logger.log(f"Current term: {CURRENT_TERM}, Storage term: {STORAGE_TERM}")

        await self.move_channels(self.config[f"{CURRENT_TERM}_IDS"], current_id)
        await self.move_channels(self.config[f"{STORAGE_TERM}_IDS"], storage_id)

    async def move_channels(self, channel_ids, category_id):
        category = self.bot.get_channel(int(category_id))
        if not category:
            logger.log(f"Category {category_id} not found.")
            return

        for channel_id in channel_ids:
            ch_id = int(channel_id)  # ensure proper type conversion
            channel = self.bot.get_channel(ch_id)
            if channel and channel.category_id != int(category_id):
                logger.log(f"Moving channel {channel.name} to category {category.name}")
                await channel.edit(category=category)
            else:
                logger.log(f"Channel {channel.name} already in the correct category or not found.")

    @commands.command()
    async def add_channel(self, ctx, channel_id: int, category_id: str):
        if category_id == self.config["SUMMER_TERM"]["CATEGORY_ID"]:
            self.config["SUMMER_IDS"].append(str(channel_id))
        elif category_id == self.config["WINTER_TERM"]["CATEGORY_ID"]:
            self.config["WINTER_IDS"].append(str(channel_id))
        else:
            await ctx.send("Invalid category ID.")
            return
        self.save_config()
        await ctx.send(f"Channel {channel_id} added to {category_id} category.")

    @commands.command()
    async def remove_channel(self, ctx, channel_id: int, category_id: str):
        if category_id == self.config["SUMMER_TERM"]["CATEGORY_ID"]:
            self.config["SUMMER_IDS"].remove(str(channel_id))
        elif category_id == self.config["WINTER_TERM"]["CATEGORY_ID"]:
            self.config["WINTER_IDS"].remove(str(channel_id))
        else:
            await ctx.send("Invalid category ID.")
            return
        self.save_config()
        await ctx.send(f"Channel {channel_id} removed from {category_id} category.")

    @commands.command()
    async def list_channels(self, ctx, category_id: str):
        if category_id == self.config["SUMMER_TERM"]["CATEGORY_ID"]:
            channels = self.config["SUMMER_IDS"]
        elif category_id == self.config["WINTER_TERM"]["CATEGORY_ID"]:
            channels = self.config["WINTER_IDS"]
        else:
            await ctx.send("Invalid category ID.")
            return
        await ctx.send(f"Channels in category {category_id}: {', '.join(channels)}")

    @commands.command()
    async def list_categories(self, ctx):
        categories = f"Summer Term: {self.config['SUMMER_TERM']['CATEGORY_ID']}\n"
        categories += f"Winter Term: {self.config['WINTER_TERM']['CATEGORY_ID']}"
        await ctx.send(categories)

    @commands.command()
    async def set_summer_term(self, ctx, start_date: str, end_date: str):
        self.config["SUMMER_TERM"]["start_date"] = start_date
        self.config["SUMMER_TERM"]["end_date"] = end_date
        self.save_config()
        await ctx.send(f"Summer term set to {start_date} - {end_date}")

    @commands.command()
    async def set_winter_term(self, ctx, start_date: str, end_date: str):
        self.config["WINTER_TERM"]["start_date"] = start_date
        self.config["WINTER_TERM"]["end_date"] = end_date
        self.save_config()
        await ctx.send(f"Winter term set to {start_date} - {end_date}")

    @commands.command()
    async def set_summer_category(self, ctx, category_id: str):
        self.config["SUMMER_TERM"]["CATEGORY_ID"] = category_id
        self.save_config()
        await ctx.send(f"Summer category set to {category_id}")

    @commands.command()
    async def set_winter_category(self, ctx, category_id: str):
        self.config["WINTER_TERM"]["CATEGORY_ID"] = category_id
        self.save_config()
        await ctx.send(f"Winter category set to {category_id}")

async def setup(bot):
    await bot.add_cog(CourseChange(bot))

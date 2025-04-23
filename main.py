import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import importlib
import glob

from lib.logger import Logger

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

owner_id = [int(os.getenv('OWNER_ID'))]
bot = commands.Bot(command_prefix='&', intents=intents, owner_ids=set(owner_id))


async def load_modules():
    modules_dir = 'modules'
    with open(os.path.join(modules_dir, 'active.txt'), 'r') as f:
        data = f.readlines()

    modules = []

    for module in data:
        module_name = (
            module
            .removesuffix('\n')
            )

        modules.append(
            (module_name, 'modules' + '.' + module_name)
        )


    for module, full_module_dir in modules:
        await bot.load_extension(full_module_dir)
        



    # for module_file in module_files:
    #     module_name = os.path.basename(module_file)[:-3]  # Remove '.py' extension
    #     full_module_name = f"{modules_dir}.{module_name}"
    #     spec = importlib.util.spec_from_file_location(full_module_name, module_file)
    #     module = importlib.util.module_from_spec(spec)
    #     spec.loader.exec_module(module)
    #     if hasattr(module, 'setup'):
    #         await bot.load_extension(full_module_name)
    #     else:
    #         logger.log(f'No setup function in {full_module_name}, skipping...')
    #     logger.log(f'Loaded module: {full_module_name}')
    
@bot.event
async def on_ready():
    logger.log(f'Logged in as {bot.user.name}')
    await load_modules()

@bot.command(name='sync', brief='Sync slash commands')
@commands.is_owner()
async def sync(ctx):
    synced = await bot.tree.sync()
    logger.log(f'Synced {len(synced)} commands')
    await ctx.send(f'Synced {len(synced)} commands')

@bot.command(name='test')
async def test(ctx):
    await ctx.send("Test command executed!")

if __name__ == "__main__":
    logger = Logger()
    logger.log("Starting bot...")
    
    bot.run(os.getenv('BOT_TOKEN'))

import os
import disnake
from disnake.ext import commands

#Bot prefix
client = commands.Bot(command_prefix = '.', intents=disnake.Intents.all())

@client.event
async def on_ready():
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1

    await client.change_presence(activity = disnake.Activity(
        type = disnake.ActivityType.watching,

        #Bot status
        name = f'ваши заявки' 

    ))
    print('''
===============================================================\n
    bot for applications, created by Pupsenn#0001 (Nykk3t_)\n
                    All rights reversed\n
==============================================================='''
    )

@client.command()
async def load(ctx, extension):
    if ctx.author.id == 760490109191323739:
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f'Cogs is loaded...')
    else:
        await ctx.send("Вы не разработчик бота...")

@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 760490109191323739:
        client.unload_extension(f"cogs.{extension}")
        await ctx.send(f'Cogs is unloaded...')
    else:
        await ctx.send("Вы не разработчик бота...")

@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 760490109191323739:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f'Cogs is reloaded...')
    else:
        await ctx.send("Вы не разработчик бота...")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        client.load_extension(f'cogs.{filename[:-3]}')
        
client.run("TOKEN")
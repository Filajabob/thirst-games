import time
import asyncio
import discord
from discord.ext import commands
from game import Game
import utils

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)


@bot.slash_command(description="Bitch")
async def ping(ctx):
    await ctx.respond("Starting")
    msg = await ctx.send("Welcome to the Thirst Games!")

    game = Game(utils.PlayerSet.load(input("Insert Player Set path: ")), 2024)
    game.start()

    while game.can_run():
        outcome = game.rotate()
        await msg.edit(outcome.combat_start_msg())

        await asyncio.sleep(1)

        await msg.edit(outcome.combat_result_msg())

        await asyncio.sleep(2)


@bot.slash_command(description="Starts a game")
async def start(ctx):
    pass


with open("assets/token.txt", 'r') as f:
    TOKEN = f.read()

bot.run(TOKEN)
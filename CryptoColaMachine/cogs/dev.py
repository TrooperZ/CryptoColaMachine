import asyncio
import os
import discord
from dotenv import load_dotenv
from random import randint, shuffle
from discord.ext import commands
from discord.ext import tasks
import aiohttp
import pymongo
import datetime
from time import gmtime, strftime
from web3 import Web3

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def say(self, ctx, *, msg):
        if ctx.author.id not in [390841378277425153, 514396597287911425]:
            return await ctx.send("You are not authorized to use this command.")
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx, cog: str):
        try:
            self.bot.reload_extension(cog)
        except Exception as e:
            await ctx.send(e)
        await ctx.send("done")

    @commands.command(hidden=True)
    @commands.has_guild_permissions(manage_guild=True)
    async def activeloyalconf(self, ctx, time1, time2, amt1, amt2):
        if ctx.server.id != 857763612361490482:
            return await ctx.send("Can only be used in Crypto Cola server.")
        configs.insert_one({"server":857763612361490482, "type": "activeloyalconf", "time1": time1, "time2": time2, "amt1": amt1, "amt2": amt2})
        await ctx.send("Configuration set.")

    @commands.command(hidden=True)
    async def shiller(self, ctx, user: discord.User):
        team = discord.utils.get(ctx.guild.roles, name="Crypto Cola Team")
        if team not in ctx.member.roles:
            return
        await ctx.send(f"$store gift {user.mention} shiller")

def setup(bot):
    bot.add_cog(Dev(bot))
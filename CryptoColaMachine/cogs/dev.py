import discord
from discord.ext import commands

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def say(self, ctx, msg):
        if ctx.author.id not in [390841378277425153, 514396597287911425]:
            return await ctx.send("You are not authorized to use this command.")
        await ctx.send(message)

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
    async def activeloyalconf(ctx, time1, time2, amt1, amt2):
        if ctx.server.id != 857763612361490482:
            return await ctx.send("Can only be used in Crypto Cola server.")
        configs.insert_one({"server":857763612361490482, "type": "activeloyalconf", "time1": time1, "time2": time2, "amt1": amt1, "amt2": amt2})
        await ctx.send("Configuration set.")

def setup(bot):
    bot.add_cog(Dev(bot))
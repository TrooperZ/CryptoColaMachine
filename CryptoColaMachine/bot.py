
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

load_dotenv()

mongoclient = pymongo.MongoClient(os.getenv("MONGODB"))
mongodb = mongoclient["data"]
configs = mongodb["configs"]

bot = commands.Bot(command_prefix="f!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    hodlloop.start()
    loop1.start()
    print("Bot is online.")

@bot.event
async def on_message(message):
    if message.channel.id in [857808852258783293]:
        if message.author.id not in [617037497574359050, 514396597287911425, 449995475303530507, 663393254284328973, 213967602911936512, 390841378277425153, 167397531196719116, 381927133334863872, 868157426199838720]:
            if not message.content.startswith('$airdrop'):
                await message.delete()
                return await message.channel.send(f"{message.author.mention}, only airdrops are allowed here.", delete_after=10)
    embeds = message.embeds
    if message.author.id == 617037497574359050:
        if message.channel.id in [864187144331198475]:
            return
        for embed in embeds:
            embed1 = embed.to_dict()
            try:
                if "airdrop" in embed1['title']:
                    await asyncio.sleep(5)
                    await message.add_reaction('🎉')
            except:
                print("Not an airdrop embed")
    await bot.process_commands(message)


intervals = (
    ("weeks", 604800),  # 60 * 60 * 24 * 7
    ("days", 86400),  # 60 * 60 * 24
    ("hours", 3600),  # 60 * 60
    ("minutes", 60),
    ("seconds", 1),
)


def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip("s")
            result.append("{} {}".format(value, name))
    return ", ".join(result[:granularity])

@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        if error.retry_after < 1:
            await ctx.send(f"This command is on a `{round(error.retry_after, 2)} second` cooldown, try again later.")
            await ctx.send(f"If you would like to have a reminder when it's time to claim, visit the $store and purchase the Faucet Ping role.")            
            return

        fixedRetry = int(error.retry_after)
        await ctx.send(f"This command is on a `{display_time(fixedRetry)}` cooldown, try again later.")
        await ctx.send(f"If you would like to have a reminder when it's time to claim, visit the $store and purchase the Faucet Ping role.")
        return

@tasks.loop(minutes=120)
async def loop1():
    await bot.wait_until_ready()

    data = configs.find({"$and": [{"server": 857763612361490482, "type": "activeloyalconf"}]})
    for x in data:
        dur = randint(int(x["time1"]), int(x["time2"]))
        amt = randint(int(x["amt1"]), int(x["amt2"]))

    channel = bot.get_channel(857808852258783293)
    await channel.send(f"$tip active {amt} colas each")
    await channel.send(f"**Thank you for being Active and Loyal to Crypto-Cola!**")

    loop1.change_interval(minutes=dur)


@tasks.loop(hours=4)
async def hodlloop():
    await bot.wait_until_ready()
    if datetime.datetime.today().weekday() != 4:
        return
    server = bot.get_guild(857763612361490482)

    five00list = []
    oneklist = []
    fiveklist = []
    tenklist = []

    noreward = discord.utils.get(server.roles, name="HODL Rewards Exempt")
    five00 = discord.utils.get(server.roles, name="CAP Holder 500")
    onek = discord.utils.get(server.roles, name="1k CAP Holder")
    fivek = discord.utils.get(server.roles, name="5k CAP Holder")
    tenk = discord.utils.get(server.roles, name="10k CAP God")

    for member in server.members:
        if noreward in member.roles:
            continue
        elif five00 in member.roles:
            five00list.append(member.mention)
        elif onek in member.roles:
            oneklist.append(member.mention)
        elif fivek in member.roles:
            fiveklist.append(member.mention)
        elif tenk in member.roles:
            tenklist.append(member.mention)

    channel = bot.get_channel(857807635432341504)
    capPrice = 0.0125
    await channel.send(f"$tip {','.join(five00list)} $0.01802884615 bnb each **500 CAP Holders**")
    await channel.send(f"$tip {','.join(oneklist)} $0.0360576923 bnb each **1000 CAP Holders**")
    await channel.send(f"$tip {','.join(fiveklist)} $0.18028846153 bnb each **5000 CAP Holders**")
    await channel.send(f"$tip {','.join(tenklist)} $0.36057692307 bnb each **10000 CAP Holders**")
    await channel.send(f"**Thank you for HODLing CAP!**")

@bot.command(name='claim')
@commands.cooldown(1, 1800, commands.BucketType.user)
async def claim(ctx, coin):
    if ctx.channel.id not in [864150180169121832, 868183998285885540]:
        return await ctx.send("Go to the faucet channel.")

    if coin.lower() not in ['eth', 'ltc', 'bch', 'wax', 'doge', 'vtc', 'ban', 'xmr', 'nano', 'rvn', 'trx', 'xlm', 'xrp', 'lotto', 'pussy', 'bnb', 'etc', '1mt', 'skill', 'comp', 'dai', 'arteon', 'r0ok', 'shx']:
        return await ctx.send(f"{ctx.author.mention}, invalid coin choice, check pins for valid coins.")

    admin = discord.utils.get(ctx.guild.roles, name="Administration Team")
    team = discord.utils.get(ctx.guild.roles, name="Crypto Cola Team")
    loyal = discord.utils.get(ctx.guild.roles, name="Loyal")
    supp = discord.utils.get(ctx.guild.roles, name="VIP Supporter")
    supp2 = discord.utils.get(ctx.guild.roles, name="Supporter")
    boost = discord.utils.get(ctx.guild.roles, name="Server Booster")
    shill = discord.utils.get(ctx.guild.roles, name="Shiller")
    ping = discord.utils.get(ctx.guild.roles, name="Faucet Ping")
    holder = discord.utils.get(ctx.guild.roles, name="1k CAP Holder")
    
    if admin in ctx.author.roles:
        await ctx.send(f"Administration Team Bonus!")
        amt = 0.0015
        await ctx.send(f"$tip {ctx.author.mention} ${amt} {coin.lower()}")

    elif team in ctx.author.roles:
        await ctx.send(f"Crypto Cola Team Bonus!")
        amt = 0.001
        await ctx.send(f"$tip {ctx.author.mention} ${amt} {coin.lower()}")       

    elif shill in ctx.author.roles:
        await ctx.send(f"Shiller Bonus!")
        amt = 0.001
        await ctx.send(f"$tip {ctx.author.mention} ${amt} {coin.lower()}")

    elif holder in ctx.author.roles:
        await ctx.send(f"CAP Holder Bonus!")
        amt = randint(3,8)/10000
        await ctx.send(f"$tip {ctx.author.mention} ${amt} {coin.lower()}")

    elif supp in ctx.author.roles:
        await ctx.send(f"Supporter Bonus!")
        amt = randint(3,8)/10000
        await ctx.send(f"$tip {ctx.author.mention} ${amt} {coin.lower()}")

    elif supp2 in ctx.author.roles:
        await ctx.send(f"Supporter Bonus!")
        amt = randint(3,8)/10000
        await ctx.send(f"$tip {ctx.author.mention} ${amt} {coin.lower()}")

    elif boost in ctx.author.roles:
        await ctx.send(f"Booster Bonus!")
        amt = randint(3,8)/10000
        await ctx.send(f"$tip {ctx.author.mention} ${amt} {coin.lower()}")

    else:
        amt = randint(1,3)/10000
        await ctx.send(f"$tip {ctx.author.mention} ${amt} {coin.lower()}")    

    if ping in ctx.author.roles:
        await asyncio.sleep(1800)
        await ctx.send(f"{ctx.author.mention} time to claim!")

@bot.command(name='bals')
async def bals(ctx, coin="none"):
    await ctx.send("$bals top noembed")

@bot.command(name='balances')
async def balances(ctx, coin="none"):
    await ctx.send("$bals top noembed")

@bot.command(name='bal')
async def bal(ctx, coin="none"):
    if coin != "none":
        return await ctx.send(f"$bal {coin}")
    await ctx.send("You need to include a cryptocurrency code (BTC, ETH, etc.).")

@bot.command(name='balance')
async def balance(ctx, coin="none"):
    if coin != "none":
        return await ctx.send(f"$bal {coin}")
    await ctx.send("You need to include a cryptocurrency code (BTC, ETH, etc.).")

@bot.command(name='say')
async def say(ctx, *, message):
    if ctx.author.id not in [390841378277425153, 514396597287911425]:
        return await ctx.send("You are not authorized to use this command.")
    await ctx.send(message)

@bot.command(name='activeloyalconf')
@commands.has_guild_permissions(manage_guild=True)
async def activeloyalconf(ctx, time1, time2, amt1, amt2):
    if ctx.server.id != 857763612361490482:
        return await ctx.send("Can only be used in Crypto Cola server.")
    configs.insert_one({"server":857763612361490482, "type": "activeloyalconf", "time1": time1, "time2": time2, "amt1": amt1, "amt2": amt2})
    await ctx.send("Configuration set.")

bot.run(os.getenv("DISCORD_TOKEN"))

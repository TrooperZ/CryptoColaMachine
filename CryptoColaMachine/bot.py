
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
load_dotenv()

mongoclient = pymongo.MongoClient(os.getenv("MONGODB"))
mongodb = mongoclient["data"]
configs = mongodb["configs"]

bot = commands.Bot(command_prefix="f!", intents=discord.Intents.all())

if __name__ == "__main__":
    for extension in [
        "cogs.commands",
        "cogs.dev"
    ]:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    hodlloop.start()
    loop1.start()
    priceloop.start()
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
            await ctx.send(f"If you would like to have a reminder when it's time to claim, visit the $store and purchase the Faucet Ping role (only for Crypto Cola server).")            
            return

        fixedRetry = int(error.retry_after)
        await ctx.send(f"This command is on a `{display_time(fixedRetry)}` cooldown, try again later.")
        await ctx.send(f"If you would like to have a reminder when it's time to claim, visit the $store and purchase the Faucet Ping role (only for Crypto Cola server).")
        return

@tasks.loop(hours=2)
async def priceloop():
    await bot.wait_until_ready()
    tokenABI = [
    {
        "constant":True,
        "inputs":[{"name":"_owner","type":"address"}],
        "name":"balanceOf",
        "outputs":[{"name":"balance","type":"uint256"}],
        "type":"function"
    },
    {
        "constant":True,
        "inputs":[
            
        ],
        "name":"totalSupply",
        "outputs":[
            {
                "name":"",
                "type":"uint256"
            }
        ],
        "payable":False,
        "stateMutability":"view",
        "type":"function"
   },
        {
        "constant":True,
        "inputs":[
            {
                "name":"",
                "type":"address"
            },
            {
                "name":"",
                "type":"address"
            }
        ],
        "name":"allowance",
        "outputs":[
            {
                "name":"",
                "type":"uint256"
            }
        ],
        "payable":False,
        "stateMutability":"view",
        "type":"function"
    }
]
    pool = Web3.toChecksumAddress("0x27dfd3d2b9bd25f8419ee77535d8a1a956b67d0c")
    capAddr = Web3.toChecksumAddress("0x2e1525c67bb5b001bce02ee88432f387b926d5bf")
    bnbAddr = Web3.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c") #wbnb
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
    cap = w3.eth.contract(abi=tokenABI, address=capAddr)
    bnb = w3.eth.contract(abi=tokenABI, address=bnbAddr)
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.coingecko.com/api/v3/simple/price?ids=binancecoin&vs_currencies=usd") as response:
            data1 = await response.json()
            bnbprice = data1["binancecoin"]["usd"]

    capbal = cap.functions.balanceOf(pool).call()
    bnbbal = bnb.functions.balanceOf(pool).call()
    price = (bnbbal / 1e18) / (capbal / 1e18) * bnbprice
    channel = bot.get_channel(877254173148717067)
    await channel.edit(name=f"$ {round(price, 5)} CAP")
    return price

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

@tasks.loop(hours=1)
async def hodlloop():
    await bot.wait_until_ready()
    if strftime("%H:%M:%S", gmtime()) != "12:00:00":
        return

    if datetime.datetime.today().weekday() != 4:
        return
    server = bot.get_guild(857763612361490482)

    oneklist = []
    fiveklist = []
    tenklist = []

    noreward = discord.utils.get(server.roles, name="HODL Rewards Exempt")
    onek = discord.utils.get(server.roles, name="1k CAP Holder")
    fivek = discord.utils.get(server.roles, name="5k CAP Holder")
    tenk = discord.utils.get(server.roles, name="10k CAP God")

    for member in server.members:
        if noreward in member.roles:
            continue
        elif tenk in member.roles:
            tenklist.append(member.mention)
            continue
        elif fivek in member.roles:
            fiveklist.append(member.mention)
            continue
        elif onek in member.roles:
            oneklist.append(member.mention)
            continue

    channel = bot.get_channel(857807635432341504)
    capPrice = await priceloop()
    a = capPrice * 1000 * 0.15 / 52
    b = capPrice * 5000 * 0.15 / 52
    c = capPrice * 10000 * 0.15 / 52
    if len(oneklist) != 0:
        await channel.send(f"$tip {','.join(oneklist)} ${a} bnb each {onek.mention}")
    if len(fiveklist) != 0:
        await channel.send(f"$tip {','.join(fiveklist)} ${b} bnb each {fivek.mention}")
    if len(tenklist) != 0:
        await channel.send(f"$tip {','.join(tenklist)} ${c} bnb each {tenk.mention}")
    
    
    await channel.send(f"**Thank you for HODLing CAP!**")



bot.run(os.getenv("DISCORD_TOKEN"))

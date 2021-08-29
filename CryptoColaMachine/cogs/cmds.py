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

class cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bals(self, ctx, coin="none"):
        await ctx.send("$bals top noembed")

    @commands.command()
    async def balances(self, ctx, coin="none"):
        await ctx.send("$bals top noembed")

    @commands.command()
    async def bal(self, ctx, coin="none"):
        if coin != "none":
            return await ctx.send(f"$bal {coin}")
        await ctx.send("You need to include a cryptocurrency code (BTC, ETH, etc.).")

    @commands.command()
    async def balance(self, ctx, coin="none"):
        if coin != "none":
            return await ctx.send(f"$bal {coin}")
        await ctx.send("You need to include a cryptocurrency code (BTC, ETH, etc.).")

    async def price(self):
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
        return price

    @commands.command()
    async def hodl(self, ctx):
        if ctx.author.id not in [514396597287911425, 390841378277425153]:
            return await ctx.send("Unauthorized usage.")
        server = self.bot.get_guild(857763612361490482)

        oneklist = []
        fiveklist = []
        tenklist = []
        tfklist = []

        noreward = discord.utils.get(server.roles, name="HODL Rewards Exempt")
        onek = discord.utils.get(server.roles, name="1k CAP Holder")
        fivek = discord.utils.get(server.roles, name="5k CAP Holder")
        tenk = discord.utils.get(server.roles, name="10k CAP God")
        tfk = discord.utils.get(server.roles, name="25k CAP God")

        for member in server.members:
            if noreward in member.roles:
                continue
            elif tfk in member.roles:
                tfk.append(member.mention)

            elif tenk in member.roles:
                tenklist.append(member.mention)
                continue
            elif fivek in member.roles:
                fiveklist.append(member.mention)
                continue
            elif onek in member.roles:
                oneklist.append(member.mention)
                continue

        channel = self.bot.get_channel(857807635432341504)
        capPrice = await self.price()
        a = capPrice * 1000 * 0.15 / 52
        b = capPrice * 5000 * 0.15 / 52
        c = capPrice * 10000 * 0.15 / 52
        d = capPrice * 25000 * 0.15 / 52
        if len(oneklist) != 0:
            await channel.send(f"$tip {','.join(oneklist)} ${a} bnb each {onek.mention}")
            await asyncio.sleep(5)
        if len(fiveklist) != 0:
            await channel.send(f"$tip {','.join(fiveklist)} ${b} bnb each {fivek.mention}")
            await asyncio.sleep(5)
        if len(tenklist) != 0:
            await channel.send(f"$tip {','.join(tenklist)} ${c} bnb each {tenk.mention}")
            await asyncio.sleep(5)
        if len(tfklist) != 0:
            await channel.send(f"$tip {','.join(tenklist)} ${d} bnb each {tfk.mention}")
            await asyncio.sleep(5)

        await channel.send(f"**Thank you for HODLing CAP!**")

    @commands.command()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def claim(self, ctx, coin):
        if ctx.guild.id == 854132705212891156:
            if ctx.channel.id not in [878038814369665034]:
                return await ctx.send("Go to the proper faucet channel.")
            if coin.lower() not in ["doge"]:
                return await ctx.send("This coin is not enabled. To access all coins visit the Crypto Cola Discord.")
            return await ctx.send(f"$tip {ctx.author.mention} $0.0001 doge **For more rewards, visit the Crypto Cola Discord.**")

        if ctx.channel.id not in [864150180169121832, 868183998285885540]:
            return await ctx.send("Go to the faucet channel.")

        if coin.lower() not in ['eth', 'ltc', 'bch', 'wax', 'doge', 'vtc', 'ban', 'xmr', 'nano', 'rvn', 'trx', 'xlm', 'xrp', 'xpr', 'lotto', 'pussy', 'etc', '1mt', 'skill', 'comp', 'dai', 'arteon', 'r0ok', 'shx']:
            return await ctx.send(f"{ctx.author.mention}, invalid coin choice, check pins for valid coins. CAP holders earn BNB weekly.")

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

    @commands.command()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def doge(self, ctx, coin):
        if ctx.guild.id == 854132705212891156:
            if ctx.channel.id not in [878038814369665034]:
                return await ctx.send("Go to the proper faucet channel.")
            if coin.lower() not in ["doge"]:
                return await ctx.send("This coin is not enabled. To access all coins visit the Crypto Cola Discord.")
            return await ctx.send(f"$tip {ctx.author.mention} $0.0001 doge **For more rewards, visit the Crypto Cola Discord.**")

def setup(bot):
    bot.add_cog(cmds(bot))
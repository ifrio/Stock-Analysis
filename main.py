from discord.ext.commands import Bot
import stockAnalysis

BOT_PREFIX = ("!")
client = Bot(command_prefix=BOT_PREFIX)
bot = stockAnalysis.StockAnalysis()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$SMATEST'):
        result = message.content.split()
        result = str(bot.backTestSMA(result[1]))
        await message.channel.send("Budget: $1,000 Backtesting Dictates: " + result)
    elif message.content.startswith('$ADD'):
        arguement = message.content.split()
        result = str(bot.addToList(arguement[1]))
        await message.channel.send(arguement[1]+" now in watchlist.")
    elif message.content.startswith('$WATCHLIST'):
        result = str(bot.getWatchList())
        await message.channel.send("Current Watchlist: " + result)

client.run('')
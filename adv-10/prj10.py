######################模組####################
import discord
import os
from dotenv import load_dotenv

#####################初始化###################
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)


####################事件###################
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await tree.sync()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello":
        await message.channel.send("Hey!")


##############指令###################
@tree.command(name="hello", description="Say hello to your bot!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hey!")


#####################啟動#####################
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()

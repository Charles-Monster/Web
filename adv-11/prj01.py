######################模組####################
import discord
import os
from dotenv import load_dotenv
from myfunction.myfunction import WeatherAPI

#####################初始化###################
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))


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


@tree.command(name="weather", description="取得天氣資訊")
async def weather(interaction: discord.Interaction, city: str, forrecast: bool = False):
    await interaction.response.defer()
    unit_symbol = "C" if weather_api.units == "metric" else "F"


    if not forrecast:
        info = weather_api.get_current_weather(city)
        if "weather" in info and "main" in info:
            current_temprature = info["main"]["temp"]
            weather_description = info["weather"][0]["description"]
            icon_code = info["weather"][0]["icon"]
            icon_url = weather_api.get_icon_url(icon_code)
            embed=discord.Embed(title=f"{city}的當前天氣",
            description=f"描述:{weather_description}"
            color=0x1E90FF,)
            embed.set_thumbnail(url=icon_url)
            embed.add_field(name="溫度", value=f"{current_temprature}度{unit_symbol}",inline=False)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"找不到**{city}**的天氣資訊。")
    else:
        info=weather_api.get_forecast(city)
        if "list" in info:
            forrecast_list = info["list"][:10]
            embeds=[]
            for forrecast in forrecast_list:
                dt_txt=forrecast["dt_txt"]
                temp=forrecast["main"]["temp"]
                description=forrecast["weather"][0]["description"]
                icon_code=forrecast["weather"][0]["icon"]
                icon_url=weather_api.get_icon_url(icon_code)
#####################啟動#####################
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()

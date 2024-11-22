######################模組####################
import discord
import os
from dotenv import load_dotenv
from myfunction.myfunction import WeatherAPI
import openai

#####################初始化###################
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

weather_api = WeatherAPI(os.getenv(""))
openai.api_key = os.getenv("")


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
async def weather(
    interaction: discord.Interaction,
    city: str,
    forrecast: bool = False,
    ai: bool = False,
):
    await interaction.response.defer()
    unit_symbol = "C" if weather_api.units == "metric" else "F"

    if not forrecast:
        info = weather_api.get_current_weather(city)
        if "weather" in info and "main" in info:
            current_temprature = info["main"]["temp"]
            weather_description = info["weather"][0]["description"]
            icon_code = info["weather"][0]["icon"]
            icon_url = weather_api.get_icon_url(icon_code)
            embed = discord.Embed(
                title=f"{city}的當前天氣",
                description=f"描述:{weather_description}",
                color=0x1E90FF,
            )
            embed.set_thumbnail(url=icon_url)
            embed.add_field(
                name="溫度", value=f"{current_temprature}度{unit_symbol}", inline=False
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"找不到**{city}**的天氣資訊。")

    else:
        info = weather_api.get_forecast(city)
        if "list" in info:
            if not ai:
                forrecast_list = info["list"][:10]
                embeds = []
                for forrecast in forrecast_list:
                    dt_txt = forrecast["dt_txt"]
                    temp = forrecast["main"]["temp"]
                    description = forrecast["weather"][0]["description"]
                    icon_code = forrecast["weather"][0]["icon"]
                    icon_url = weather_api.get_icon_url(icon_code)
                    embed = discord.Embed(
                        title=f"{city}天氣預報-{dt_txt}",
                        decription=f"描述{description},color=0x1E90FF",
                    )
                    embed.set_thumbnail(url=icon_url)
                    embed.add_field(
                        name="溫度", value=f"{temp}度{unit_symbol}", inline=False
                    )
                    embeds.append(embed)
                await interaction.followup.send(embeds=embeds)
            else:
                try:
                    reponse = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": "你是一個專業的氣象分析師，請根據用戶的輸入，回答用戶的問題。",
                            },
                            {
                                "role": "user",
                                "content": f"以下是{city}的未來天氣預報。請根據這些數據提供詳細的天氣預報。\n{info}",
                            },
                        ],
                        temperature=0.2,
                    )
                    analysis = reponse.choices[0].message.content
                    await interaction.followup.send(
                        "**{city}**的天氣分析:\n{analysis}。"
                    )
                except Exception as e:
                    await interaction.followup.send(f"發生錯誤：{e}")

        else:
            await interaction.followup.send(f"找不到**{city}**的天氣預報。")


#####################啟動#####################
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()

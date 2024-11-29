#######################模組#######################
import discord  # pip install -U discord.py
import os
from dotenv import load_dotenv  # pip install -U python-dotenv
from myfunction.myfunction import WeatherAPI  # 引入先前建立的 WeatherAPI 類別
import openai


#######################初始化#######################
load_dotenv()  # 載入環境變數
# 建立機器人，並設定 intents 以接收訊息內容
intents = discord.Intents.default()
intents.message_content = True  # 啟用訊息內容的 intents
bot = discord.Client(intents=intents)  # 建立一個 Discord 客戶端
tree = discord.app_commands.CommandTree(bot)  # 建立指令樹，用於管理 slash 指令
weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))  # 初始化 WeatherAPI 類別
openai.api_key = os.getenv("OPENAI_API_KEY")


#######################事件#######################
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")  # 當機器人準備好時，印出訊息
    await tree.sync()  # 同步指令至伺服器


channel_games = {}


@bot.event
async def on_message(message):
    channel_id = message.channel.id
    if message.author == bot.user:  # 避免機器人自己回應自己, 造成無限迴圈
        return  # 結束函式
    if message.content == "hello":  # 如果訊息內容為 hello
        await message.channel.send("Hey!")  # 回應 Hey!

    elif channel_id in channel_games:
        user_input = message.content.strip()
        if user_input == "結束遊戲":
            channel_games.pop(channel_id)
            await message.channel.send("遊戲結束！")
        else:
            game_data = channel_games[channel_id]["game data"]
            if "history" not in channel_games[channel_id]:
                channel_games[channel_id]["history"] = []
            history = channel_games[channel_id]["history"]
            history.append({"role": "user", "content": user_input})
            messages = (
                [
                    {
                        "role": "system",
                        "content": f"""你是一個海龜湯遊戲的主持人,根據以下的謎題回答玩家的提問。
                        你的回應只能是「是」、「不是」、「無可奉告」、「恭喜答對!」,並盡可能簡短。
                        謎題：{game_data["question"]}
                        解答：{game_data["answer"]}
                        """,
                    }
                ]
                + history
            )
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.5,
                )
                anwser = response.choices[0].message.content
                if anwser == "恭喜答對!":
                    game_data["solved"] = True
                    await message.send("恭喜答對!")
                    channel_games.pop(channel.id)
                else:
                    history.append({"role": "assistant", "content": anwser})
                    channel_games[channel.id][history] = history
                    await message.send(anwser)
                    print(messages)
            except Exception as e:
                await message.send(f"發生錯誤：{e}")
    else:
        await bot.process_commands(message)


#######################指令#######################
@tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    """輸入 hello, 會回傳 Hey!"""
    await interaction.response.send_message("Hey!")  # 回應 Hey!


# 天氣指令，可選擇當前天氣或未來預報
@tree.command(name="weather", description="取得天氣資訊")
async def weather(
    interaction: discord.Interaction,
    city: str,
    forecast: bool = False,
    ai: bool = False,
):
    await interaction.response.defer()  # 延遲回應，以防止超時
    unit_symbol = "C" if weather_api.units == "metric" else "F"
    if not forecast:
        # 獲取當前天氣
        info = weather_api.get_current_weather(city)
        if "weather" in info and "main" in info:
            current_temperature = info["main"]["temp"]
            weather_description = info["weather"][0]["description"]
            icon_code = info["weather"][0]["icon"]
            icon_url = weather_api.get_icon_url(icon_code)
            embed = discord.Embed(
                title=f"{city} 的當前天氣",
                description=f"描述：{weather_description}",
                color=0x1E90FF,
            )
            embed.set_thumbnail(url=icon_url)
            embed.add_field(
                name="溫度",
                value=f"{current_temperature}°{unit_symbol}",
                inline=False,
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"找不到 **{city}** 的天氣資訊。")
    else:
        # 獲取未來天氣預報
        info = weather_api.get_forecast(city)
        if "list" in info:
            if not ai:
                forecast_list = info["list"][:10]  # 取得未來 10 筆天氣預報
                embeds = []
                for forecast in forecast_list:
                    dt_txt = forecast["dt_txt"]
                    temp = forecast["main"]["temp"]
                    description = forecast["weather"][0]["description"]
                    icon_code = forecast["weather"][0]["icon"]
                    icon_url = weather_api.get_icon_url(icon_code)
                    embed = discord.Embed(
                        title=f"{city} 天氣預報 - {dt_txt}",
                        description=f"描述：{description}",
                        color=0x1E90FF,
                    )
                    embed.set_thumbnail(url=icon_url)
                    embed.add_field(
                        name="溫度",
                        value=f"{temp}°{unit_symbol}",
                        inline=False,
                    )
                    embeds.append(embed)
                    await interaction.followup.send(embeds=embeds)
            else:
                try:
                    response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": "你是一位專業的氣象分析師，為使用者提供詳細的天氣分析和建議。",
                            },
                            {
                                "role": "user",
                                "content": f"以下是 {city} 的未來天氣預報，請根據這些數據提供詳細的天氣分析和建議：\n{info}",
                            },
                        ],
                        temperature=0.2,
                    )
                    analysis = response.choices[0].message.content
                    # 發送分析結果給使用者
                    await interaction.followup.send(
                        f"**{city}** 的天氣分析：\n{analysis}"
                    )
                except Exception as e:
                    await interaction.followup.send(f"抱歉，在分析天氣時發生錯誤：{e}")
        else:
            await interaction.followup.send(f"找不到 **{city}** 的天氣預報資訊。")


@tree.command(name="turtle", description="開始海龜湯遊戲")
async def turtle_soup(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id in channel_games:
        await interaction.response.send_message(
            "這個頻道已經有正在進行的遊戲", ephemeral=True
        )
    else:
        channel_games[channel_id] = {
            "game data": {
                "question": "一個人在沙漠中發現了一具屍體，旁邊有一根燒過的火柴。發生了甚麼事？",
                "answer": "他參加了熱氣球比賽為了減重需要有人跳下去，他抽到了最短的火柴，只好跳下。",
                "solved": False,
            },
            "history": [],
        }
    await interaction.response.send_message(
        f"""
    遊戲開始！
    題目：{channel_games[channel_id]["game data"]["question"]}
    請大家開始提問，輸入 結束遊戲 可結束遊戲。
    我的回應只會是「是」、「不是」或「無可奉告」。"""
    )


#######################啟動#######################
def main():
    # 讀取環境變數, 並啟動機器人
    bot.run(os.getenv("DC_BOT_TOKEN"))  # 從環境變數中讀取機器人的 token 並啟動


# 主程式
if __name__ == "__main__":
    main()  # 執行主程式

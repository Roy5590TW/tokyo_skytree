import discord
from discord.ext import commands
import json
import os
import asyncio
import datetime

# 讀取設定檔
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 定義機器人的前綴並創建機器人實例
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.get('prefix'), intents=intents)


# Bot 啟動時的事件處理
@bot.event
async def on_ready():
    global log_channel, error_channel, owner_id, start_time
    await bot.wait_until_ready()  # 等待機器人完全啟動
    log_channel = bot.get_channel(int(config.get('log_channel_id')))
    error_channel = bot.get_channel(int(config.get('error_channel_id')))
    owner_id = int(config.get('owner_id'))
    try:
        await check_channel_null()
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        print(f">> Bot is online <<")
        print('------')
        # 在紀錄用的頻道發送消息
        await log_channel.send(f'Logged in as {bot.user} (ID: {bot.user.id})')
        await log_channel.send(f">> Bot is online <<")
        await log_channel.send('------')
        start_time = datetime.datetime.now()
    except Exception as e:
        # 如果在處理 on_ready 事件時發生錯誤，將錯誤信息發送到錯誤頻道
        print(f"An error occurred while handling the on_ready event: {e}")
        await error_channel.send(f"An error occurred while handling the on_ready event: {e}")

@bot.command(name='chelp', brief="Show available commands")
async def help(ctx):
    embed = discord.Embed(title="Command Help", color=discord.Color.blurple())
    for cog in ctx.bot.cogs.values():
        commands_list = [f"**{command.name}** - {command.brief}" for command in cog.get_commands()]
        embed.add_field(name=cog.qualified_name, value="\n".join(commands_list), inline=False)
    embed.set_footer(text="Type >help <command> for more info on a command. You can also type >help <category> for more info on a category.")
    await ctx.send(embed=embed)

# 載入指令程式檔案
@bot.command(name='load', brief='load extension')
async def load(ctx, extension):
    if not await check_permissions(ctx):
        return

    try:
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Loaded {extension} done.")
        await log_channel.send(f"{ctx.author} Loaded {extension} done.")
    except Exception as e:
        await ctx.send(f"Error loading {extension}: {e}")
        await error_channel.send(f"Error loading {extension}: {e}")

# 卸載指令檔案
@bot.command(name='unload', brief='unload extension')
async def unload(ctx, extension):
    if not await check_permissions(ctx):
        return

    try:
        await bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"UnLoaded {extension} done.")
        await log_channel.send(f"{ctx.author} UnLoaded {extension} done.")
    except Exception as e:
        await ctx.send(f"Error unloading {extension}: {e}")
        await error_channel.send(f"Error unloading {extension}: {e}")

# 重新載入程式檔案
@bot.command(name='reload', brief='reload extension')
async def reload(ctx, extension):
    if not await check_permissions(ctx):
        return

    try:
        await bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"ReLoaded {extension} done.")
        await log_channel.send(f"{ctx.author} ReLoaded {extension} done.")
    except Exception as e:
        await ctx.send(f"Error reloading {extension}: {e}")
        await error_channel.send(f"Error reloading {extension}: {e}")



# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")




@bot.command(name='uptime', brief='bot online time')
async def uptime(ctx):
    try:
        if ctx.author.id == owner_id:
            await check_channel_null()
            uptime_delta = datetime.datetime.now() - start_time
            total_seconds = uptime_delta.total_seconds()
            days = total_seconds // (24 * 3600)
            hours = (total_seconds % (24 * 3600)) // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            uptime_str = f"{int(days)} Days, {int(hours)} Hours, {int(minutes)} minutes, {int(seconds)} Seconds"
            await ctx.send(f"Online: {uptime_str}")
            await log_channel.send(f"{ctx.author} used the uptime command return Online: {uptime_str}")
        else:
            await ctx.send("Sorry, you don't have permission to use uptime.")
            await log_channel.send(f"{ctx.author} tried to use uptime but no permission")
    except Exception as e:
        await ctx.send(f"An error occurred while calculating uptime: {e}")
        await log_channel.send(f"Error occurred while calculating uptime: {e}")


async def check_channel_null():
    if log_channel is None or error_channel is None:
            raise ValueError("Could not find the specified channels.")
    return True

# 權限檢查函式
async def check_permissions(ctx):
    if ctx.author.id != owner_id:
        await ctx.send(f"You don't have permission to use this command.")
        await log_channel.send(f"{ctx.author} don't have permission to use {ctx.message.content} command.")
        return False
    return True





async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.get('bot_token'))

# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())

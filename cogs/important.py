import discord
from discord.ext import commands
import json

# 读取配置文件
with open('./config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 定义名为 important 的 Cog
class important(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel = None
        self.error_channel = None
        self.owner_id = None

    # 前缀指令
    @commands.command(name='shutdown', brief='Stop the bot')
    async def shutdown(self, ctx):
        global owner_id, log_channel, error_channel
        owner_id = int(config.get('owner_id'))
        log_channel = self.bot.get_channel(int(config.get('log_channel_id')))
        error_channel = self.bot.get_channel(int(config.get('error_channel_id')))
        # 检查指令使用者是否具有关闭机器人的权限，例如只允许机器人的拥有者使用这个指令
        if ctx.author.id == owner_id:
            await ctx.send("Stopping the bot...")
            await log_channel.send(f"{ctx.author} Stopping the bot... in {ctx.channel.mention}")
            await self.bot.close()
        else:
            await ctx.send("Sorry, you don't have permission to stop the bot")
            await log_channel.send(f"{ctx.author} Tried stop the bot in {ctx.channel.mention} but no permission")

# Cog 加载到 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(important(bot))

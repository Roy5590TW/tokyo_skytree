import discord
from discord.ext import commands
import json
# 讀取設定檔
with open('./config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
# 定義名為 basic 的 Cog
class basic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel = None
        self.error_channel = None

    


    @commands.command(name='ping', brief="Get bot ping")
    async def ping(self,ctx):
        try:
            global log_channel, error_channel
            log_channel = self.bot.get_channel(int(config.get('log_channel_id')))
            error_channel = self.bot.get_channel(int(config.get('error_channel_id')))
            if log_channel is None or error_channel is None:
                raise ValueError("Could not find the specified channels.")
            latency = round(self.bot.latency * 1000)
            await ctx.send(f'Ping: {latency}ms', reference=ctx.message)
            await log_channel.send(f'{ctx.author} used command >ping in {ctx.channel.mention}')
            print(f'{ctx.author} used command >ping in {ctx.channel.mention}')
        except Exception as e:
            await ctx.send(f'Error: {e}')
            await error_channel.send(f'{ctx.author.mention} Error: {e}')
    
    @commands.command(name='clear', brief="Delete messages from the channel")
    async def clear(self,ctx, num : int):
        if log_channel is None or error_channel is None:
            raise ValueError("Could not find the specified channels.")
        await ctx.message.delete()
        await ctx.channel.purge(limit=num)
        await ctx.send(f'Deleted {num} message.')
        if ctx.channel != log_channel:  # 如果命令不是在 log_channel 中使用的，才發送 log 訊息
            await log_channel.send(f'{ctx.author} used command >clear to Deleted {num} message in {ctx.channel.mention}.')
        print(f'Deleted {num} message.')
    
    @commands.command(name='avatar', brief="Get the avatar of a user")
    async def avatar(self,ctx, member: discord.Member):
        if log_channel is None or error_channel is None:
                raise ValueError("Could not find the specified channels.")
        await ctx.send(f'{ctx.author.mention}')
        await ctx.send(f'{member.display_avatar}')
        await log_channel.send(f'{ctx.author} used command >avatar to get avatar in {ctx.channel.mention}')
        await log_channel.send(f'{member.display_avatar}')
    
    @commands.command(name='invite', brief='Invite the bot to your server')
    async def invite(self, ctx):
        try:
            invite_embed = discord.Embed(title="Invite me to your server!")
            invite_button = discord.ui.Button(style=discord.ButtonStyle.link, label="Invite",
                                              url="https://discord.com/oauth2/authorize?client_id=1210241148002635807&permissions=0&scope=bot")
            action_row = discord.ui.ActionRow(invite_button)
            await ctx.send(embed=invite_embed, components=[action_row])
        except Exception as e:
            await ctx.send(f'Error: {e}')



# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(basic(bot))
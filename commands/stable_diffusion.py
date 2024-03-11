import discord
from discord.ext import commands
import json
import requests
import base64
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
# 讀取設定檔
with open('./config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 定義名為 important 的 Cog
class stable_diffusion(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel = None
        self.error_channel = None
        self.executor = ThreadPoolExecutor(max_workers=10)

    
    # 前綴指令
    #txt2img command
    @commands.command(name='txt2img', brief='Stable Diffusion txt2img')
    async def txt2img(self,ctx, *, prompt: str):  # 接收提示參數
        try:
            log_channel = self.bot.get_channel(int(config.get('log_channel_id')))
            error_channel = self.bot.get_channel(int(config.get('error_channel_id')))
            url = "http://192.168.10.165:7860"
            payload = {
                "prompt": f"(masterpiece:1.2),best quality,highres,extremely detailed CG,perfect lighting,8k wallpaper,anime,comic,game CG,{prompt}",
                "negative_prompt": "(worst quality:2),(low quality:2),(normal quality:2),lowres,normal quality,((monochrome)),((grayscale)),skin spots,acnes,skin blemishes,age spot,(ugly:1.331),(duplicate:1.331),(morbid:1.21),(mutilated:1.21),(tranny:1.331),mutated hands,(poorly drawn hands:1.5),blurry,(bad anatomy:1.21),(bad proportions:1.331),extra limbs,(disfigured:1.331),(missing arms:1.331),(extra legs:1.331),(fused fingers:1.5),(too many fingers:1.5),(unclear eyes:1.331),lowers,bad hands,missing fingers,extra digit,bad hands,missing fingers,(((extra arms and legs))),",
                "seed": -1,
                "steps": 30,
                "width": 768,
                "height": 1024,
                "cfg_scale": 7,
                "sampler_name": "DPM++ 2M SDE Karras",
                "batch_size": 1,
                "sd_model_checkpoint": "anything_v4.5_vae",
                "CLIP_stop_at_last_layers": 2,
            }
            await log_channel.send(f'{ctx.author} asked me to imagine {prompt}. Picture is being generated in {ctx.channel.mention}.')
            await ctx.send(f'{ctx.author.mention} asked me to imagine {prompt}. Picture is being generated.')
            # 透過 API 將 payload 發送到 URL
            t2i_r = await self.run_in_executor(self.generate_image, url, payload)
            

            json_info = json.loads(t2i_r['info'])
            seed = json_info.get('seed')
            cfg_scale = json_info.get('cfg_scale')
            steps = json_info.get('steps')
            sampler_name = json_info.get('sampler_name')
            CLIP_stop_at_last_layers = json_info.get('clip_skip')
            sd_version = json_info.get('version')
            model = 'anything_v4.5_vae'
            negative_prompt = json_info.get('negative_prompt')
            # 解碼並保存圖片
            with open(f'{seed}.png', 'wb') as f:
                f.write(base64.b64decode(t2i_r['images'][0]))

            # 組合嵌入式訊息和圖片
            embed = discord.Embed(title="Image generate completed", color=discord.Color.blurple())
            embed.add_field(name="User", value=f'{ctx.author.mention}', inline=False)
            embed.add_field(name="Prompt", value=prompt, inline=False)
            embed.add_field(name="Negative_Prompt", value=negative_prompt, inline=False)
            embed.add_field(name="Seed", value=seed, inline=False)
            embed.add_field(name="Steps", value=steps, inline=False)
            embed.add_field(name="Sampler_name", value=sampler_name, inline=False)
            embed.add_field(name="CFG_scale", value=cfg_scale, inline=False)
            embed.add_field(name="Clip skip", value=CLIP_stop_at_last_layers, inline=False)
            embed.add_field(name="Model", value=model, inline=False)
            embed.add_field(name="SD_version", value=sd_version, inline=False)

            with open(f'{seed}.png', 'rb') as f:
                file = discord.File(f, filename=f'{seed}.png')
                embed.set_image(url=f'attachment://{seed}.png')  # 設定嵌入式訊息中的圖片
                await ctx.send(embed=embed, file=file)
                await log_channel.send(embed=embed, file=file)
            
            await log_channel.send("t2i finish！")
            # 刪除圖片
            os.remove(f'{seed}.png')
            print('Picture Deleted.')
            await log_channel.send('picture deleted.')
        except requests.exceptions.RequestException as e:
            await ctx.send(f"在與 API 進行請求時發生錯誤: {e}")
            await error_channel.send(f"{ctx.author.mention} 在與 API 進行請求時發生錯誤: {e}")
        except (KeyError, json.JSONDecodeError) as e:
            await ctx.send(f"在處理 API 回應時發生錯誤: {e}")
            await error_channel.send(f"{ctx.author.mention} 在處理 API 回應時發生錯誤: {e}")
        except Exception as e:
            await ctx.send(f"發生意外錯誤: {e}")
            await error_channel.send(f"{ctx.author.mention} 發生意外錯誤: {e}")
    # 定義生成圖片的函數
    def generate_image(self, url, payload):
        txt2img_response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
        txt2img_response.raise_for_status()  # 如果回應不成功，則拋出錯誤
        return txt2img_response.json()

    # 在線程池中運行函數
    async def run_in_executor(self, func, *args):
        return await self.bot.loop.run_in_executor(self.executor, func, *args)


# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(stable_diffusion(bot))
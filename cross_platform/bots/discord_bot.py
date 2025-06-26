"""
CRUZ AI Discord Bot
使用統一 API Gateway 的 Discord 機器人
"""
import discord
from discord.ext import commands
import asyncio
import os
from typing import Optional
import logging

# 導入 SDK
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sdk.cruz_ai_sdk import create_cruz_ai, PersonaType

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 人格表情符號
PERSONA_EMOJIS = {
    "cruz-decisive": "🎯",
    "serena-supportive": "🌸",
    "wood-creative": "🌳",
    "fire-passionate": "🔥",
    "earth-stable": "🏔️",
    "metal-precise": "⚔️",
    "water-adaptive": "💧"
}

class CruzBot(commands.Bot):
    """CRUZ AI Discord Bot"""
    
    def __init__(self, api_key: str):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix='!cruz ',
            intents=intents,
            description="CRUZ AI - 你的多人格 AI 助手"
        )
        
        self.api_key = api_key
        self.sdk_instances = {}  # 每個用戶一個 SDK 實例
        self.user_personas = {}  # 記錄每個用戶的當前人格
        
    async def setup_hook(self):
        """設置 bot"""
        logger.info("🎯 CRUZ Discord Bot 啟動中...")
        
        # 添加 Cog
        await self.add_cog(PersonaCommands(self))
        await self.add_cog(ChatHandler(self))
        
    async def on_ready(self):
        """Bot 就緒"""
        logger.info(f'✅ {self.user} 已連接到 Discord!')
        logger.info(f'📊 在 {len(self.guilds)} 個伺服器中運行')
        
        # 設置狀態
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="!cruz help | 🎯 決斷模式"
            )
        )
    
    async def get_user_sdk(self, user_id: str) -> 'cruz_ai_sdk.CruzAISDK':
        """獲取或創建用戶的 SDK 實例"""
        if user_id not in self.sdk_instances:
            sdk = create_cruz_ai(
                api_key=self.api_key,
                platform="discord"
            )
            await sdk.initialize(user_id)
            
            # 註冊事件處理器
            sdk.on("persona_changed", lambda e: self.on_persona_changed(user_id, e))
            
            self.sdk_instances[user_id] = sdk
            
        return self.sdk_instances[user_id]
    
    def on_persona_changed(self, user_id: str, event: dict):
        """處理人格變更事件"""
        persona = event.get("persona", "cruz-decisive")
        self.user_personas[user_id] = persona
        logger.info(f"用戶 {user_id} 切換到 {persona}")

class PersonaCommands(commands.Cog):
    """人格相關指令"""
    
    def __init__(self, bot: CruzBot):
        self.bot = bot
    
    @commands.command(name='persona', aliases=['p'])
    async def switch_persona(self, ctx: commands.Context, persona: Optional[str] = None):
        """切換 AI 人格
        
        可用人格:
        - cruz: 決斷果敢 🎯
        - serena: 溫柔支持 🌸
        - wood: 創意創新 🌳
        - fire: 熱情實踐 🔥
        - earth: 穩固架構 🏔️
        - metal: 精準優化 ⚔️
        - water: 適應測試 💧
        """
        if not persona:
            # 顯示當前人格
            current = self.bot.user_personas.get(str(ctx.author.id), "cruz-decisive")
            emoji = PERSONA_EMOJIS.get(current, "🤖")
            
            embed = discord.Embed(
                title="當前人格",
                description=f"{emoji} {current}",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="可用人格",
                value="\n".join([
                    "🎯 `cruz` - 決斷果敢",
                    "🌸 `serena` - 溫柔支持",
                    "🌳 `wood` - 創意創新",
                    "🔥 `fire` - 熱情實踐",
                    "🏔️ `earth` - 穩固架構",
                    "⚔️ `metal` - 精準優化",
                    "💧 `water` - 適應測試"
                ])
            )
            await ctx.send(embed=embed)
            return
        
        # 人格映射
        persona_map = {
            "cruz": PersonaType.CRUZ_DECISIVE,
            "serena": PersonaType.SERENA_SUPPORTIVE,
            "wood": PersonaType.WOOD_CREATIVE,
            "fire": PersonaType.FIRE_PASSIONATE,
            "earth": PersonaType.EARTH_STABLE,
            "metal": PersonaType.METAL_PRECISE,
            "water": PersonaType.WATER_ADAPTIVE
        }
        
        if persona.lower() not in persona_map:
            await ctx.send("❌ 無效的人格！使用 `!cruz persona` 查看可用選項。")
            return
        
        # 切換人格
        sdk = await self.bot.get_user_sdk(str(ctx.author.id))
        selected_persona = persona_map[persona.lower()]
        await sdk.switch_persona(selected_persona)
        
        emoji = PERSONA_EMOJIS.get(selected_persona.value, "🤖")
        await ctx.send(f"{emoji} 已切換到 **{selected_persona.value}** 人格模式！")
        
        # 更新 bot 狀態
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"!cruz help | {emoji} {persona.capitalize()}"
            )
        )
    
    @commands.command(name='memory', aliases=['m'])
    async def toggle_memory(self, ctx: commands.Context, state: Optional[str] = None):
        """開關記憶功能
        
        用法:
        - !cruz memory on: 開啟記憶
        - !cruz memory off: 關閉記憶
        - !cruz memory: 查看狀態
        """
        sdk = await self.bot.get_user_sdk(str(ctx.author.id))
        
        if state is None:
            # 顯示當前狀態
            session = await sdk.get_session()
            status = "開啟 ✅" if session.memory_enabled else "關閉 ❌"
            await ctx.send(f"💾 記憶功能目前: **{status}**")
            return
        
        if state.lower() == "on":
            await sdk.toggle_memory(True)
            await ctx.send("💾 記憶功能已 **開啟** ✅")
        elif state.lower() == "off":
            await sdk.toggle_memory(False)
            await ctx.send("💾 記憶功能已 **關閉** ❌")
        else:
            await ctx.send("❌ 請使用 `on` 或 `off`")
    
    @commands.command(name='status', aliases=['s'])
    async def show_status(self, ctx: commands.Context):
        """顯示當前狀態"""
        sdk = await self.bot.get_user_sdk(str(ctx.author.id))
        session = await sdk.get_session()
        
        current_persona = session.current_persona
        emoji = PERSONA_EMOJIS.get(current_persona, "🤖")
        
        embed = discord.Embed(
            title="🎯 CRUZ AI 狀態",
            color=discord.Color.green()
        )
        embed.add_field(name="當前人格", value=f"{emoji} {current_persona}", inline=True)
        embed.add_field(name="記憶功能", value="✅ 開啟" if session.memory_enabled else "❌ 關閉", inline=True)
        embed.add_field(name="連接平台", value=", ".join(session.platforms), inline=True)
        embed.set_footer(text=f"用戶 ID: {ctx.author.id}")
        
        await ctx.send(embed=embed)

class ChatHandler(commands.Cog):
    """聊天處理"""
    
    def __init__(self, bot: CruzBot):
        self.bot = bot
        self.typing_tasks = {}
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """處理聊天消息"""
        # 忽略 bot 自己的消息
        if message.author.bot:
            return
        
        # 檢查是否被提及或在私訊中
        if not (self.bot.user in message.mentions or isinstance(message.channel, discord.DMChannel)):
            return
        
        # 忽略指令
        if message.content.startswith('!cruz'):
            return
        
        # 清理消息內容
        content = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
        if not content:
            return
        
        # 顯示輸入中狀態
        async with message.channel.typing():
            try:
                # 獲取 SDK
                sdk = await self.bot.get_user_sdk(str(message.author.id))
                
                # 發送消息
                response = await sdk.send_message(
                    message=content,
                    metadata={
                        "channel_id": str(message.channel.id),
                        "guild_id": str(message.guild.id) if message.guild else None,
                        "username": message.author.name
                    }
                )
                
                # 獲取人格表情
                emoji = PERSONA_EMOJIS.get(response.persona, "🤖")
                
                # 發送回應
                # 如果回應太長，分段發送
                if len(response.response) > 2000:
                    chunks = [response.response[i:i+1900] for i in range(0, len(response.response), 1900)]
                    for i, chunk in enumerate(chunks):
                        if i == 0:
                            await message.reply(f"{emoji} {chunk}")
                        else:
                            await message.channel.send(chunk)
                else:
                    await message.reply(f"{emoji} {response.response}")
                
                # 添加反應表情
                if response.emotion:
                    emotion_emojis = {
                        "determined": "💪",
                        "energized": "⚡",
                        "frustrated": "😤",
                        "intense": "🔥",
                        "intrigued": "🤔",
                        "cautious": "🤨"
                    }
                    if response.emotion in emotion_emojis:
                        await message.add_reaction(emotion_emojis[response.emotion])
                
            except Exception as e:
                logger.error(f"處理消息時發生錯誤: {e}")
                await message.reply("❌ 抱歉，處理您的消息時發生錯誤。")

async def main():
    """主函數"""
    # 從環境變數獲取配置
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    api_key = os.getenv("CRUZ_API_KEY", "test-api-key")
    
    if not discord_token:
        logger.error("請設置 DISCORD_BOT_TOKEN 環境變數")
        return
    
    # 創建並運行 bot
    bot = CruzBot(api_key=api_key)
    
    try:
        await bot.start(discord_token)
    except KeyboardInterrupt:
        logger.info("收到中斷信號，正在關閉...")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
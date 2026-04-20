import discord
from discord.ext import commands
import os
import asyncio

TOKEN = os.environ.get("TOKEN")
GUILD_ID = int(os.environ.get("GUILD_ID", 0))
CATEGORY_ID = int(os.environ.get("CATEGORY_ID", 0))
BOT_TICKET_ID = int(os.environ.get("BOT_TICKET_ID", 0))
MENSAGEM = os.environ.get("MENSAGEM", "Olá, como posso ajudar?")
DELAY = float(os.environ.get("DELAY_RESPOSTA", 0))

canais_processados = set()
tickets = 0

class SelfBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", self_bot=True)
    
    async def on_ready(self):
        print(f"✅ Selfbot online: {self.user}")
        print(f"⚡ Delay: {DELAY*1000:.0f}ms")
    
    async def on_message(self, message):
        global tickets, canais_processados
        
        if message.author == self.user:
            return
        if message.author.id != BOT_TICKET_ID:
            return
        if message.guild.id != GUILD_ID:
            return
        if message.channel.category_id != CATEGORY_ID:
            return
        if message.channel.id in canais_processados:
            return
        
        canais_processados.add(message.channel.id)
        tickets += 1
        print(f"🎯 Ticket: {message.channel.name} (Total: {tickets})")
        
        if DELAY > 0:
            await asyncio.sleep(DELAY)
        elif DELAY < 0:
            print(f"⚡ Delay negativo {DELAY*1000:.0f}ms - resposta prioritária")
            await asyncio.sleep(0)
        
        await message.channel.send(MENSAGEM)
        print(f"   ✅ Respondido!")

if __name__ == "__main__":
    bot = SelfBot()
    bot.run(TOKEN)

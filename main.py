import discord
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True
bot = commands.Bot(command_prefix='giveaway!', description="Giveaway Bot", intents=intents)

def convert_time(duration: int, time_unit: str) -> int:
    time_unit = time_unit.lower()
    if time_unit in ["s"]:
        return duration
    elif time_unit in ["m"]:
        return duration * 60
    elif time_unit in ["h"]:
        return duration * 3600
    else:
        raise discord.ext.commands.BadArgument(f"Invalid time unit '{time_unit}'. Use 'seconds', 'minutes', or 'hours'.")

@bot.event
async def on_ready():
    print('Bot is active now!')

@bot.command()
async def giveaway(ctx, duration: int, time_unit: str, winners: int, *, prize: str):
    embed = discord.Embed(title="Giveaway!", description=f"{prize}", color=discord.Color.random())
    embed.add_field(name="Hosted by:", value=ctx.author.mention)
    embed.add_field(name="React with 🎉 to enter!", value=f"Duration: {duration} {time_unit}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    duration_seconds = convert_time(duration, time_unit)
    await asyncio.sleep(duration_seconds)
    new_msg = await ctx.channel.fetch_message(msg.id)
    
    users = []
    async for user in new_msg.reactions[0].users():
        if user != bot.user:
            users.append(user)
            
    if winners < 1:
        winners = 1
    
    if len(users) <= winners:
        selected_winners = users
    else:
        selected_winners = random.sample(users, winners)

    winners_mention = ", ".join(user.mention for user in selected_winners)
    await ctx.send(f"Congratulations {winners_mention}! You won {prize}!")


bot.run(TOKEN)
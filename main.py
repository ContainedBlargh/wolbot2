#!/usr/bin/python3
from discord import Bot
from discord import ApplicationContext
import dotenv

from os import getenv

from subprocess import Popen, PIPE, STDOUT

dotenv.load_dotenv()

owner_id = int(getenv('API_OWN'))
token = getenv('API_TOK')
wol_bin = getenv('WOL_BIN')
wol_mac = getenv('WOL_MAC')

bot = Bot()

@bot.slash_command(name = "wol", description="Wake up your PC")
async def wol(ctx: ApplicationContext):
    if ctx.author.id != owner_id:
        await ctx.respond("Unauthorized.", ephemeral=True)
        return
    await ctx.send("Ok, waking up you computer...", ephemeral=True)
    await ctx.defer()
    wakeonlan = None
    for _ in range(2):
        wakeonlan = Popen([wol_bin, wol_mac], stdout=PIPE, stderr=PIPE)
        wakeonlan.wait()
    
    if wakeonlan.returncode != 0:
        error = '\n'.join(wakeonlan.stdout.readlines())
        await ctx.send_followup(f"An error occurred:\n{error}", ephemeral=True)
    else:
        await ctx.send_followup(f"You PC should be ready to work in a few moments...", ephemeral=True)
    pass

if __name__ == "__main__":
    bot.run(token)
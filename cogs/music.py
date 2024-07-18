from header import Cog_Extension

class music(Cog_Extension):
    pass

async def setup(bot):
    await bot.add_cog(music(bot))

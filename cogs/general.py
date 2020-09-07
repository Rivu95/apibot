from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="regex")
    async def regex(self, ctx):
        """Responds with the RegEx for player/clan tags"""
        await ctx.send("^#[PYLQGRJCUV0289]+$")

    @commands.command(name="rate_limit")
    async def rate_limit(self, ctx):
        """Responds with the rate limit information for the Clash API"""
        await ctx.send("We have found that the approximate rate limit is 30-40 requests per second. Staying "
                       "below this should be safe.")

    @commands.command(name="vps")
    async def vps(self, ctx):
        """Responds with a link to a Discord message on inexpensive VPS options"""
        await ctx.send("https://discordapp.com/channels/566451504332931073/566451504903618561/662484243808780309")

    @commands.command(name="links")
    async def links(self, ctx):
        """Responds with a link to a Discord message on the Discord Link API (by ReverendMike)"""
        await ctx.send("https://discordapp.com/channels/566451504332931073/681617252814159904/685533375280578610")

    @commands.command(name="js")
    async def js(self, ctx):
        """Responds with links of discord.js guide and coc api wrapper made by Suvajit"""
        await ctx.send("Discord js Guide: https://discordjs.guide/\nJS CoC Api Wrapper: https://www.npmjs.com/package/clashofclans.js")

    @commands.command(name="py")
    async def py(self, ctx):
        """Responds with links of discord.py guide and coc api wrapper made by Mathsman"""
        await ctx.send("Discord py Guide: https://pythondiscord.com/pages/resources/guides/\nPythion CoC Api Wrapper: https://cocpy.readthedocs.io/en/latest/")


def setup(bot):
    bot.add_cog(General(bot))

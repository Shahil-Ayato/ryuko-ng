import discord
import config
from discord.ext import commands
from discord.ext.commands import Cog


class Links(Cog):
    """
    Commands for easily linking to projects.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def pegaswitch(self, ctx):
        """Link to the Pegaswitch repo"""
        await ctx.send("https://github.com/reswitched/pegaswitch")

    @commands.command(hidden=True, aliases=["atmos"])
    async def atmosphere(self, ctx):
        """Link to the Atmosphere repo"""
        await ctx.send("https://github.com/atmosphere-nx/atmosphere")

    @commands.command(hidden=True, aliases=["xyproblem"])
    async def xy(self, ctx):
        """Link to the "What is the XY problem?" post from SE"""
        await ctx.send(
            "<https://meta.stackexchange.com/q/66377/285481>\n\n"
            "TL;DR: It's asking about your attempted solution "
            "rather than your actual problem.\n"
            "It's perfectly okay to want to learn about a "
            "solution, but please be clear about your intentions "
            "if you're not actually trying to solve a problem."
        )

    @commands.command(hidden=True, aliases=["guides", "link"])
    async def guide(self, ctx):
        """Link to the guides"""
        await ctx.send(config.links_guide_text)

    @commands.command()
    async def source(self, ctx):
        """Gives link to source code."""
        await ctx.send(
            f"You can find my source at {config.source_url}. "
            "Serious PRs and issues welcome!"
        )

    @commands.command()
    async def rules(self, ctx, *, targetuser: discord.Member = None):
        """Post a link to the Rules"""
        if not targetuser:
            targetuser = ctx.author
        await ctx.send(
            f"{targetuser.mention}: A link to the rules "
            f"can be found here: {config.rules_url}"
        )

    @commands.command()
    async def community(self, ctx, *, targetuser: discord.Member = None):
        """Post a link to the community section of the rules"""
        if not targetuser:
            targetuser = ctx.author
        await ctx.send(
            f"{targetuser.mention}: "
            "https://reswitched.github.io/discord/#member-roles-breakdown"
            "\n\n"
            "Community role allows access to the set of channels "
            "on the community category (#off-topic, "
            "#homebrew-development, #switch-hacking-general etc)."
            "\n\n"
            "What you need to get the role is to be around, "
            "be helpful and nice to people and "
            "show an understanding of rules."
        )


def setup(bot):
    bot.add_cog(Links(bot))

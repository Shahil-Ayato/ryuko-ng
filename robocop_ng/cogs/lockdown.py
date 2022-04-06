from discord.ext import commands
from discord.ext.commands import Cog
import config
import discord
from helpers.checks import check_if_staff


class Lockdown(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def set_sendmessage(
        self, channel: discord.TextChannel, role, allow_send, issuer
    ):
        try:
            roleobj = channel.guild.get_role(role)
            overrides = channel.overwrites_for(roleobj)
            overrides.send_messages = allow_send
            await channel.set_permissions(
                roleobj, overwrite=overrides, reason=str(issuer)
            )
        except:
            pass

    async def unlock_for_staff(self, channel: discord.TextChannel, issuer):
        for role in config.staff_role_ids:
            await self.set_sendmessage(channel, role, True, issuer)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def lock(self, ctx, channel: discord.TextChannel = None, soft: bool = False):
        """Prevents people from speaking in a channel, staff only.

        Defaults to current channel."""
        if not channel:
            channel = ctx.channel
        log_channel = self.bot.get_channel(config.modlog_channel)

        roles = None
        for key, lockdown_conf in config.lockdown_configs.items():
            if channel.id in lockdown_conf["channels"]:
                roles = lockdown_conf["roles"]

        if roles is None:
            roles = config.lockdown_configs["default"]["roles"]

        for role in roles:
            await self.set_sendmessage(channel, role, False, ctx.author)

        await self.unlock_for_staff(channel, ctx.author)

        public_msg = "🔒 Channel locked down. "
        if not soft:
            public_msg += (
                "Only staff members may speak. "
                "Do not bring the topic to other channels or risk "
                "disciplinary actions."
            )

        await ctx.send(public_msg)
        safe_name = await commands.clean_content(escape_markdown=True).convert(
            ctx, str(ctx.author)
        )
        msg = (
            f"🔒 **Lockdown**: {ctx.channel.mention} by {ctx.author.mention} "
            f"| {safe_name}"
        )
        await log_channel.send(msg)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Unlocks speaking in current channel, staff only."""
        if not channel:
            channel = ctx.channel
        log_channel = self.bot.get_channel(config.modlog_channel)

        roles = None
        for key, lockdown_conf in config.lockdown_configs.items():
            if channel.id in lockdown_conf["channels"]:
                roles = lockdown_conf["roles"]

        if roles is None:
            roles = config.lockdown_configs["default"]["roles"]

        await self.unlock_for_staff(channel, ctx.author)

        for role in roles:
            await self.set_sendmessage(channel, role, True, ctx.author)

        safe_name = await commands.clean_content(escape_markdown=True).convert(
            ctx, str(ctx.author)
        )
        await ctx.send("🔓 Channel unlocked.")
        msg = (
            f"🔓 **Unlock**: {ctx.channel.mention} by {ctx.author.mention} "
            f"| {safe_name}"
        )
        await log_channel.send(msg)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def move(context):

        # get the content of the message
        content = context.message.content.split(' ')
        # if the length is not three the command was used incorrectly
        if len(content) != 3 or not content[2].isnumeric():
        await context.message.channel.send("Incorrect usage of !move. Example: !move {channel to move to} {number of messages}.")
        return
        # channel that it is going to be posted to
        channelTo = content[1]
        # get the number of messages to be moved (including the command message)
        numberOfMessages = int(content[2]) + 1
        # get a list of the messages
        fetchedMessages = await context.channel.history(limit=numberOfMessages).flatten()
    
        # delete all of those messages from the channel
        for i in fetchedMessages:
            await i.delete()

        # invert the list and remove the last message (gets rid of the command message)
        fetchedMessages = fetchedMessages[::-1]
        fetchedMessages = fetchedMessages[:-1]

        # Loop over the messages fetched
        for messages in fetchedMessages:
            # get the channel object for the server to send to
            channelTo = discord.utils.get(messages.guild.channels, name=channelTo)

            # if the message is embeded already
            if messages.embeds:
                # set the embed message to the old embed object
                embedMessage = messages.embeds[0]
            # else
            else:
                # Create embed message object and set content to original
                embedMessage = discord.Embed(
                            description = messages.content
                            )
                # set the embed message author to original author
                embedMessage.set_author(name=messages.author, icon_url=messages.author.avatar_url)
                # if message has attachments add them
                if messages.attachments:
                    for i in messages.attachments:
                        embedMessage.set_image(url = i.proxy_url)

            # Send to the desired channel
            await channelTo.send(embed=embedMessage)        

def setup(bot):
    bot.add_cog(Lockdown(bot))

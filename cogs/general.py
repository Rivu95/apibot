import discord

from config import settings
from discord.ext import commands


JUNKIES_GUILD_ID = settings['guild']['junkies']
BOT_DEMO_CATEGORY_ID = settings['category']['bot_demo']
HOG_RIDER_ROLE_ID = settings['roles']['hog_rider']
BOTS_ROLE_ID = settings['roles']['bots']
BOT_MAKER_ROLE_ID = settings['roles']['bot_maker']
ADMIN_ROLE_ID = settings['roles']['admin']
GUEST_ROLE_ID = settings['roles']['vip_guest']


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
        await ctx.send("https://discordapp.com/channels/566451504332931073/681617252814159904/755489156146397311")
        
    @commands.command(name="role_stats")
    async def role_stats(self, ctx):
        """Responds with a formatted code block containing the number of members with each role excluding those in
        the exclude list"""
        # Local constants
        bot_maker_role = "Bot Maker"
        no_roles = "No Roles"
        include = [
            bot_maker_role,
            "Python",
            "JS",
            "Bots",
            "C#",
            "PHP",
            "C++",
            "Java",
        ]

        spacing = 0
        roles = []
        role_stats = {no_roles: 0}
        for member in ctx.guild.members:
            member: discord.Member

            # If user only has @everyone role, consider them as having no roles
            if len(member.roles) == 1:
                role_stats[no_roles] += 1
                continue

            # Iterate over all roles a member has in the guild and increment the counter
            for role in member.roles:
                # Ignore excluded roles
                if role.name not in include:
                    continue

                if role_stats.get(role.name) is None:
                    # Calculate the spacing for printing
                    if len(role.name) > spacing:
                        spacing = len(role.name)

                    role_stats[role.name] = 1
                    roles.append(role.name)
                else:
                    role_stats[role.name] += 1

        # Pop Bot Maker role from list
        if bot_maker_role in roles:
            roles.pop(roles.index(bot_maker_role))

        # Sort and prep for iteration
        roles.sort(key=lambda x: role_stats[x], reverse=True)
        spacing += 2
        panel = ""

        # Add header to the panel "Bot Maker" and "No Roles"
        if role_stats.get(bot_maker_role):
            panel += f"{bot_maker_role+':':<{spacing}} {role_stats.get(bot_maker_role)}\n"
        panel += f"{no_roles+':':<{spacing}} {role_stats.get(no_roles)}\n"
        panel += f"{'-' * (spacing + 4)}\n"

        # Build the rest of the panel
        for role in roles:
            count = role_stats.get(role)
            role += ":"
            panel += f"{role:<{spacing}} {count}\n"

        await ctx.send(f"```{panel}```")

    @commands.command(name="setup", aliases=["set_up", ], hidden=True)
    @commands.has_role("Admin")
    async def setup_bot(self, ctx, bot: discord.Member = None, owner: discord.Member = None):
        """Admin use only: For adding bot demo channels
        Creates channel (based on bot name)
        Alphabetizes channel within the Bot-Demos category
        Sets proper permissions
        Sets the channel topic to 'Maintained by [owner]'
        Pings owner so they see the channel and can demonstrate features
        Adds the "Bots" role to the bot.

        **Example:**
        /setup @bot @owner

        **Permissions:**
        Admin role required
        """
        if not bot or not owner:
            return await ctx.send("Please be sure to provide a Discord ID or mention both the bot and the owner. "
                                  "`/setup @bot @owner`")
        if not bot.bot:
            return await ctx.send(f"{bot.mention} does not appear to be a bot. Please try again with "
                                  f"`/setup @bot @owner`.")
        if owner.bot:
            return await ctx.send(f"{owner.mention} appears to be a bot, but should be the bot owner. Please try "
                                  f"again with `/setup @bot @owner`.")

        category = self.bot.get_channel(BOT_DEMO_CATEGORY_ID)
        guild = self.bot.get_guild(JUNKIES_GUILD_ID)
        guest_role = guild.get_role(GUEST_ROLE_ID)
        bot_maker_role = guild.get_role(BOT_MAKER_ROLE_ID)
        hog_rider_role = guild.get_role(HOG_RIDER_ROLE_ID)
        admin_role = guild.get_role(ADMIN_ROLE_ID)
        channel_name = f"{bot.name}-demo"
        topic = f"Maintained by {owner.display_name}"
        overwrites = {
            bot: discord.PermissionOverwrite(read_messages=True,
                                             send_messages=True,
                                             read_message_history=True,
                                             manage_messages=True,
                                             embed_links=True,
                                             attach_files=True,
                                             external_emojis=True,
                                             add_reactions=True),
            admin_role: discord.PermissionOverwrite(read_messages=True,
                                                    send_messages=True),
            hog_rider_role: discord.PermissionOverwrite(read_messages=True,
                                                        send_messages=True,
                                                        read_message_history=True,
                                                        manage_messages=True,
                                                        embed_links=True,
                                                        attach_files=True,
                                                        external_emojis=True,
                                                        add_reactions=True),
            bot_maker_role: discord.PermissionOverwrite(read_messages=True,
                                                        send_messages=True,
                                                        read_message_history=True,
                                                        manage_messages=False,
                                                        embed_links=True,
                                                        attach_files=True,
                                                        external_emojis=True,
                                                        add_reactions=True),
            guest_role: discord.PermissionOverwrite(read_messages=True,
                                                    send_messages=True,
                                                    read_message_history=True,
                                                    manage_messages=False,
                                                    embed_links=True,
                                                    attach_files=True,
                                                    external_emojis=False,
                                                    add_reactions=True),
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }
        try:
            position = category.channels[0].position + sorted(
                category.channels + [channel_name], key=lambda c: str(c)
            ).index(channel_name)

            channel = await ctx.guild.create_text_channel(channel_name,
                                                          overwrites=overwrites,
                                                          category=category,
                                                          position=position,
                                                          topic=topic,
                                                          reason=f"Created by the setup command of Hog Rider ({ctx.author})",
                                                          )
        except:
            self.bot.logger.exception("Failed creating channel")

        # ping owner
        await channel.send(f"{owner.mention} This channel has been set up for your use in demonstrating the features "
                           f"of **{bot.name}**. Limited troubleshooting with others is acceptable, but please do not "
                           f"allow this channel to become a testing platform.  Thanks!")

        # add the "Bots" role
        await bot.add_roles(ctx.guild.get_role(BOTS_ROLE_ID),
                            reason=f"Added by setup command of Hog Rider ({ctx.author})",
                            )

        # sort the Bot-Demo channels alphabetically
        for index, channel in enumerate(sorted(category.channels,
                                               key=lambda c: str(c)),
                                        start=category.channels[0].position):
            if channel.position != index:
                await channel.edit(position=index)

        # Provide user feedback on success
        await ctx.message.add_reaction("\u2705")
        await ctx.send(f"If {owner.display_name} would like bot monitoring, here's your command:\n"
                       f"`/bot add {bot.id}`")

    @commands.command(name="clear", hidden=True)
    @commands.is_owner()
    async def clear(self, ctx, msg_count: int = None):
        if msg_count:
            await ctx.channel.purge(limit=msg_count + 1)
        else:
            async for message in ctx.channel.history():
                await message.delete()


def setup(bot):
    bot.add_cog(General(bot))

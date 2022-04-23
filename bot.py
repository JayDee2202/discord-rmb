import discord
import asyncio
import os


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged on as', self.user)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Dinge verladen!"))

    async def on_member_update(self, before, after):
        if before.roles is not after.roles:
            role_source1 = int(os.getenv('DISCORD_ROLE_SOURCE1'))
            role_source2 = int(os.getenv('DISCORD_ROLE_SOURCE2'))
            role_dest = int(os.getenv('DISCORD_ROLE_DEST'))

            member_before_role_ids = [r.id for r in before.roles]
            member_after_role_ids = [r.id for r in after.roles]

            # Add dest role if member is in at least one source role
            if role_dest not in member_after_role_ids and (role_source1 not in member_before_role_ids or role_source2 not in member_before_role_ids) and (role_source1 in member_after_role_ids or role_source2 in member_after_role_ids):
                await after.add_roles(discord.utils.get(after.guild.roles, id=role_dest))

            # Remove dest role if member is in no source role
            if role_dest in member_after_role_ids and (role_source1 not in member_after_role_ids and role_source2 not in member_after_role_ids):
                await after.remove_roles(discord.utils.get(after.guild.roles, id=role_dest))

    async def my_background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            role_source1 = int(os.getenv('DISCORD_ROLE_SOURCE1'))
            role_source2 = int(os.getenv('DISCORD_ROLE_SOURCE2'))
            role_dest = int(os.getenv('DISCORD_ROLE_DEST'))
            guild = discord.utils.get(client.guilds, id=int(os.getenv('DISCORD_SERVER_ID')))

            for member in guild.members:
                member_roles = [r.id for r in member.roles]

                if role_dest not in member_roles and (role_source1 in member_roles or role_source2 in member_roles):
                    role = discord.utils.get(member.guild.roles, id=role_dest)
                    await member.add_roles(role)

                if role_dest in member_roles and (role_source1 not in member_roles and role_source2 not in member_roles):
                    role = discord.utils.get(member.guild.roles, id=role_dest)
                    await member.remove_roles(role)

            await asyncio.sleep(60 * 60)  # This asyncio task runs every hour


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))



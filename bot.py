import discord
import asyncio
import os
import sys


needed_envvars = ['DISCORD_ROLE_SOURCE1', 'DISCORD_ROLE_SOURCE2', 'DISCORD_ROLE_DEST', 'DISCORD_SERVER_ID', 'DISCORD_TOKEN']
optional_envvars = ['DISCORD_ROLE_SOURCE3']
missing_envvars = []
using_default = False

for envvar in needed_envvars:
    if os.getenv(envvar) is None or len(os.getenv(envvar)) == 0:
        missing_envvars.append(envvar)

    if os.getenv(envvar) == '1234123412341234':
        print(f"Warning: You are using the default value for {envvar}, please change it!")
        using_default = True

if len(missing_envvars) > 0:
    print("Error: Please add the environment variables: " + ", ".join(missing_envvars))
    sys.exit(1)

if using_default:
    sys.exit(1)


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
            role_source3_env = os.getenv('DISCORD_ROLE_SOURCE3')
            role_source3 = int(role_source3_env) if role_source3_env else None

            member_before_role_ids = [r.id for r in before.roles]
            member_after_role_ids = [r.id for r in after.roles]

            # If a third role is provided
            if os.getenv('DISCORD_ROLE_SOURCE3'):

                # Add dest role if member is in at least one source role
                if role_dest not in member_after_role_ids and (role_source1 not in member_before_role_ids or role_source2 not in member_before_role_ids or role_source3 not in member_before_role_ids) and (role_source1 in member_after_role_ids or role_source2 in member_after_role_ids or role_source3 in member_after_role_ids):
                    print('Adding userrole to', after.name)
                    await after.add_roles(discord.utils.get(after.guild.roles, id=role_dest))

                # Remove dest role if member is in no source role
                if role_dest in member_after_role_ids and (role_source1 not in member_after_role_ids and role_source2 not in member_after_role_ids and role_source3 not in member_after_role_ids):
                    print('Removing userrole from', after.name)
                    await after.remove_roles(discord.utils.get(after.guild.roles, id=role_dest))

            # Only two roles to merge
            else:
                # Add dest role if member is in at least one source role
                if role_dest not in member_after_role_ids and (role_source1 not in member_before_role_ids or role_source2 not in member_before_role_ids) and (role_source1 in member_after_role_ids or role_source2 in member_after_role_ids):
                    print('Adding userrole to', after.name)
                    await after.add_roles(discord.utils.get(after.guild.roles, id=role_dest))

                # Remove dest role if member is in no source role
                if role_dest in member_after_role_ids and (role_source1 not in member_after_role_ids and role_source2 not in member_after_role_ids):
                    print('Removing userrole from', after.name)
                    await after.remove_roles(discord.utils.get(after.guild.roles, id=role_dest))

    async def my_background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            role_source1 = int(os.getenv('DISCORD_ROLE_SOURCE1'))
            role_source2 = int(os.getenv('DISCORD_ROLE_SOURCE2'))
            role_dest = int(os.getenv('DISCORD_ROLE_DEST'))
            guild = discord.utils.get(client.guilds, id=int(os.getenv('DISCORD_SERVER_ID')))
            role_source3_env = os.getenv('DISCORD_ROLE_SOURCE3')
            role_source3 = int(role_source3_env) if role_source3_env else None

            for member in guild.members:
                member_roles = [r.id for r in member.roles]

                # If a third role is provided
                if role_source3 is not None:
                    if role_dest not in member_roles and (role_source1 in member_roles or role_source2 in member_roles or role_source3 in member_roles):
                        role = discord.utils.get(member.guild.roles, id=role_dest)
                        print('Adding userrole to', member.name)
                        await member.add_roles(role)

                    if role_dest in member_roles and (role_source1 not in member_roles and role_source2 not in member_roles and role_source3 not in member_roles):
                        role = discord.utils.get(member.guild.roles, id=role_dest)
                        print('Removing userrole from', member.name)
                        await member.remove_roles(role)

                # Only two roles to merge
                else:
                    if role_dest not in member_roles and (role_source1 in member_roles or role_source2 in member_roles):
                        role = discord.utils.get(member.guild.roles, id=role_dest)
                        print('Adding userrole to', member.name)
                        await member.add_roles(role)

                    if role_dest in member_roles and (role_source1 not in member_roles and role_source2 not in member_roles):
                        role = discord.utils.get(member.guild.roles, id=role_dest)
                        print('Removing userrole from', member.name)
                        await member.remove_roles(role)

            await asyncio.sleep(60 * 60)  # This asyncio task runs every hour


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))



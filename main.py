import discord
from discord.ext import commands
from discord.ext.commands import guild_only
import pandas as pd
import pytz
from datetime import datetime
import asyncio

bot_name = 'Patrol'
bot_token = 'your_bot_token'
vr = 'v1.0.0'
invite_link = 'your_invite_link'
now = datetime.now()
current_time = now.strftime("%I:%M %p")
# Client
client = commands.Bot(command_prefix= ':')
client.remove_command('help')


#help command
@client.command(name = 'help')
async def help(ctx):
    help_Embed = discord.Embed(title = f'**Server : **{ctx.guild.name}', description = 'The Bot prefix for this server is: `?`', color = 0xff0000)
    help_Embed.set_author(name = bot_name)
    help_Embed.add_field(name='**Public Commands: **', value='help \n ping \n version \n avatar \n afk \n invite', inline=False)
    help_Embed.add_field(name='**Mod/Admin Commands: **', value='setnick \n setrole \n purge \n warn \n kick \n ban \n unban \n mute \n unmute \n userinfo \n lock \n unlock')
    help_Embed.set_footer(text=f'{vr}')
    await ctx.send(embed= help_Embed)

# send invite link to the user
@client.command(name = 'invite')
async def invite(ctx):
    try:
        await ctx.author.send(invite_link)
    except:
        await ctx.send(invite_link)

#answers with the ms latency
@client.command()
async def ping(ctx):
    ping_Embed = discord.Embed(title = 'Latency', description = f'Pong! `{round (client.latency * 1000)} ms` ', color = 0xff0000)
    await ctx.send(embed = ping_Embed)


# clear messages
@client.command(name = 'purge')
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=2):
    await ctx.channel.purge(limit=amount + 1)



#returns version of Bot
@client.command(name = 'version')
async def version(context):
    myEmbed = discord.Embed(title = "Current Version", description = 'The Bot is in Version 1.0', color = 0xff0000)
    myEmbed.add_field(name = 'Version Code', value = vr, inline=False)
    myEmbed.add_field(name = 'Date of Release', value = 'January 06, 2021', inline=False)
    myEmbed.set_footer(text = 'Invite Patrol to your Server')
    myEmbed.set_author(name = bot_name)
    await context.message.channel.send(embed = myEmbed)

# sets an user afk
afkdict = {}
@client.command(name = "afk")
async def afk(ctx, *, message = "They didn't leave a message!"):
    global afkdict

    if ctx.message.author in afkdict:
        afkdict.pop(ctx.message.author)
        await ctx.send('Welcome back! You are no longer afk.')

    else:
        afkdict[ctx.message.author] = message
        await ctx.send("You are now afk.")


@client.event
async def on_message(message):
    global afkdict

    for member in message.mentions:  
        if member != message.author:  
            if member in afkdict:  
                afkmsg = afkdict[member]  
                await message.channel.send(f"{member.mention} is afk. {afkmsg}")
        elif member == message.author:
            await message.channel.send('Welcome back')
    await client.process_commands(message)


# set role to a user, Mod/Admin Only
@client.command(name = 'setrole')
@commands.has_permissions(manage_roles = True)
async def setrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"Roles changed for {member.name} : {role.name}")



#kicks a user from server, MOD/ADMIN only
@client.command(name = 'kick')
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason):
    reason = reason or None
    await member.send(f'You were kicked from the server for :{reason}')
    await member.kick(reason = reason)
    await ctx.send(f'user {member.name} has been kicked')




#bans a user from server, MOD/ADMIN only
@client.command(name = 'ban')
@commands.has_permissions(kick_members = True)
async def ban(ctx, member: discord.Member, *, reason):
    reason = reason or None
    await member.send(f'You were banned from the server for : {str(reason)}')
    await member.ban(reason = reason)
    await ctx.send(f'user {member.name} has been banned')

# unbans a user from server, Mod/Admin Only
@client.command(name = 'unban')
@commands.has_permissions(kick_members = True)
@guild_only()
async def unban(ctx, id: int):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(f'unbanned {user}' )




# mute and unmute
@client.command(name = 'mute')
@commands.has_permissions(manage_roles = True)
async def mute(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.add_roles(role)
    await ctx.send("User Was Muted")

@client.command(name = 'unmute')
@commands.has_permissions(manage_roles = True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role)
    await ctx.send("User Was Unmuted")

    

# warns a user, Mod/Admin only
@client.command(name='warn')
@commands.has_permissions(kick_members = True)
async def warn(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        wEr_Embed = discord.Embed(title = f':negative_squared_cross_mark: **Please Provide a Reason.**', color = 0xff0000)
        await ctx.send(embed = wEr_Embed)
    else:
        await member.send(f'You were warned in {ctx.guild.name} for : {reason} ')
        warn_Embed = discord.Embed(title=f':white_check_mark: **{member.name} has been warned.**', color = 0xff0000)
        await ctx.send(embed = warn_Embed)




# lock channel Mod/Admin Only
@client.command(name='lock')
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None, reason=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f'Channel locked for {reason} .')

# unlock channel Mod/Admin Only
@client.command(name='unlock')
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel Unlocked.')



# user info to Mods Only

@client.command(name = 'userinfo')
@commands.has_permissions(manage_guild=True)
async def userinfo(ctx, member: discord.Member):
    info_Embed = discord.Embed(
        title="User Info:",
        description=f"{member.name}",
        colour=0xff0000
    )
    info_Embed.set_image(url=member.avatar_url)
    info_Embed.add_field(name="**Discord Tag:**", value=member.mention, inline=False)
    info_Embed.add_field(name="**Joined Server On:**",
                        value=f'{member.joined_at.strftime("%d-%m-%Y - %I:%M %p")} ',
                        inline=False)
    info_Embed.add_field(name="**Account Created On:**",
                        value=f'{member.created_at.strftime("%d-%m-%Y - %I:%M %p")} ',
                        inline=False)
    roles = [role.mention for role in member.roles[1:]]
    info_Embed.add_field(name=f"**Roles({len(roles)}):**",value=",".join(roles), inline=False)
    perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
    info_Embed.add_field(name=f"**Permissions({len(perm_list)}):**",value=" , \n".join(perm_list), inline=False)
    info_Embed.set_footer(icon_url=ctx.author.avatar_url,
                        text=f"Requested by {ctx.author.name}  {current_time} • UTC")
    await ctx.send(embed=info_Embed)



# avatar of author or user mentioned
@client.command(name = 'avatar')
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    av_Embed = discord.Embed(title= f'**{member}**', description = '**Avatar :**', colour=0xff0000)
    av_Embed.set_image(url=member.avatar_url)
    await ctx.send(embed=av_Embed)



# change nickname Mod/Admin only
@client.command(name = 'setnick')
@commands.has_permissions(change_nickname = True)
async def setnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    nick_Embed = discord.Embed(title = f'Nickname changed for {member.name}', color = 0xff0000)
    await ctx.send(embed = nick_Embed)



@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity= discord.Activity(type = discord.ActivityType.listening, name = '?help'))


# run client on server
client.run(bot_token)

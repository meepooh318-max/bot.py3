import nextcord
import json
from nextcord.ext import commands
import datetime
from nextcord import Activity, ActivityType, Status
import asyncio
import os

with open("config.json", "r") as f:
    config = json.load(f)

def load_roles():
    return config.get("roles", [])


phakaphop = commands.Bot(command_prefix="/", intents=nextcord.Intents.all())

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@phakaphop.event
async def on_ready():
    clear_console()
    print(f"{TerminalColors.HEADER}Bot is ready: {phakaphop.user.name} by PhakaphopKUb#0{TerminalColors.ENDC}")
    print(f"{TerminalColors.OKBLUE}Connected to {len(phakaphop.guilds)} servers:{TerminalColors.ENDC}")
    for guild in phakaphop.guilds:
        print(f"{TerminalColors.OKGREEN}- {guild.name} {TerminalColors.WARNING}(ID: {guild.id}){TerminalColors.ENDC}")
    total_users = sum(len(guild.members) for guild in phakaphop.guilds)
    print(f"{TerminalColors.BOLD}Serving {total_users} users{TerminalColors.ENDC}")
    print(f"{TerminalColors.UNDERLINE}Ready to goll!{TerminalColors.ENDC}")

    
    activities = [
        Activity(type=ActivityType.playing, name="คำสั่ง /vfy"),
        Activity(type=ActivityType.listening, name="มีอะไรติดต่อ phakaphopkub#0"),
        Activity(type=ActivityType.watching, name="บอทรับยศ"),
        Activity(type=ActivityType.watching, name="Bot by: PhakaphopKUb#0")

    ]

    statuses = [Status.online, Status.dnd, Status.idle]


    for status in statuses:
        for activity in activities:
            await phakaphop.change_presence(status=status, activity=activity)
            await asyncio.sleep(10)  

@phakaphop.slash_command(description="กดที่นี่เพื่อรับยศ")
async def vfy(ctx):
    roles = load_roles()
    user = ctx.user

    if any(int(role_id) in [role.id for role in user.roles] for role_id in roles):
        await ctx.send("> **คุณมียศอยู่แล้ว** ❗", ephemeral=True)
        return

    valid_roles = []
    for role_id in roles:
        if role_id and role_id.strip():
            try:
                role = ctx.guild.get_role(int(role_id))
                if role:
                    if role.position >= user.top_role.position:
                        await ctx.send(f"บทบาท `{role.name}` มีลำดับชั้นสูงเกินกว่าที่คุณจะเพิ่มได้", ephemeral=True)
                    else:
                        valid_roles.append(role)
                else:
                    await ctx.send(f"บทบาทไอดี `{role_id}` ไม่มีอยู่ในเซิร์ฟเวอร์", ephemeral=True)
            except ValueError:
                await ctx.send(f"บทบาทไม่ถูกต้อง: `{role_id}`", ephemeral=True)

    if not valid_roles:
        if not roles:
            await ctx.send("ไม่ได้ถูกกําหนดบทบาท กรุณาติดต่อแอดมิน", ephemeral=True)
        await ctx.send("ไม่มีบทบาทที่ถูกต้องที่จะเพิ่ม", ephemeral=True)
        return

    for role in valid_roles:
        await user.add_roles(role)

        embed = nextcord.Embed(
            title="รับยศ แล้ว",
            description=f"{user.mention} ได้รับบทบาท {role.mention}",
            color=0x00ff00
        )
        embed.add_field(name="รับยศ :", value=user.mention, inline=True)
        embed.add_field(name="บทบาทที่ได้รับ:", value=role.mention, inline=True)

        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        else:
            embed.set_thumbnail(url=user.default_avatar.url if user.default_avatar else nextcord.Embed.Empty)

        await ctx.send(embed=embed, ephemeral=True)

    embed = nextcord.Embed(title="Verify", description=f"{user.mention}` ได้รับบทบาทแล้ว`", color=0x00ff00)
    embed.add_field(name="รับยศ :", value=user.mention, inline=True)
    embed.add_field(name="บทบาทที่ได้รับ:", value=role.mention, inline=True)

    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)
    else:
        embed.set_thumbnail(url=user.default_avatar.url if user.default_avatar else nextcord.Embed.Empty)


    channel_id = config.get("channel_id")
    channel = phakaphop.get_channel(int(channel_id))

    if channel:
        embed_log = nextcord.Embed(title="รับยศ ", description=f"{user.mention} `ได้รับบทบาท` {role.mention}", color=0xff0000)

        if user.avatar:
            embed_log.set_thumbnail(url=user.avatar.url)
        else:
            embed_log.set_thumbnail(url=user.default_avatar.url if user.default_avatar else nextcord.Embed.Empty)

        await channel.send(embed=embed_log)

phakaphop.run(config["TOKEN"])

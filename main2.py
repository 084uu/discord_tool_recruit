import discord
from discord.ext import commands
import re
import datetime
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.reactions = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN="MTExNzc4OTEwNzcyOTQ3NzY0Mg.GvmpeD.ZobrWWPEKcnLK2ygCZ2zeRI8QmauT9CI_GuCFg"

async def hand_up(user_id, embed, channel, message):
    user_mention = f"<@{user_id}>"
    new_description = embed.description
    footer_text = embed.footer.text
    footer_lines = footer_text.split("\n")
    if user_mention not in new_description:
        new_description += f"\n{user_mention}"
        line_count = len(new_description.split("\n")) - 1
        if line_count > 11:
            modified_first_line = "■"*11 + " over"
        elif line_count == 11:
            modified_first_line = "■"*line_count + " 集まった！"
            file_path = "image.jpg"
            with open(file_path, "rb") as file:
                image = discord.File(file)
            await channel.send(file=image, content="集まったよ～みんなありがと～")
            await message.add_reaction("🖼️")
        elif line_count == 0:
            modified_first_line = "□"*11
        else:
            modified_first_line = "■"*line_count + "□"*(11 - line_count) + f" あと{11 - line_count}人"
    else:
        new_description = embed.description.replace(f"\n{user_mention}", "")
        line_count = len(new_description.split("\n")) - 1
        if line_count > 11:
            modified_first_line = "■"*11 + " over"
        elif line_count == 0:
            modified_first_line = "□"*11
        else:
            modified_first_line = "■"*line_count + "□"*(11 - line_count) + f" あと{11 - line_count}人"
    embed.description = new_description
    footer_lines[0] = modified_first_line
    embed.set_footer(text="\n".join(footer_lines))
    embed.timestamp = datetime.datetime.today()
    await message.edit(embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    reac_group = {"✋","🔄","🔔","📢","ℹ️","🖼️","❌"}
    if payload.member.bot:
        return
    if payload.emoji.name not in reac_group:
        return
    guild = bot.get_guild(payload.guild_id)
    channel = discord.utils.get(guild.channels, id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if not message.embeds:
        if payload.emoji.name == "❌":
            await message.delete()
            return
    embed = message.embeds[0]
    await message.remove_reaction(payload.emoji, payload.member)
    if embed:
        if payload.emoji.name == "✋":
            user_id = payload.user_id
            await hand_up(user_id, embed, channel, message)

        elif payload.emoji.name == "🔄":
            await message.delete()
            embed.timestamp = datetime.datetime.today()
            new_message = await channel.send(embed=embed)
            await new_message.add_reaction("✋")
            await new_message.add_reaction("🔄")
            await new_message.add_reaction("🔔")
            await new_message.add_reaction("📢")
            await new_message.add_reaction("ℹ️")
            line_count = len(embed.description.split("\n")) - 1
            if line_count >= 11:
                await new_message.add_reaction("🖼️")

        elif payload.emoji.name == "🔔":
            line_count = len(embed.description.split("\n")) - 1
            if line_count >= 11:
                await channel.send("もー集まってる！")
            elif line_count < 4:
                await channel.send("募集してるよ！@everyone")
            else:
                await channel.send(f"あと{11 - line_count}人だよ！@everyone")

        elif payload.emoji.name == "📢":
            user_mentions = re.findall(r"@(\w+)", embed.description)
            if user_mentions:
                mention_text = " ".join([f"<@{mention}>" for mention in user_mentions])
                await channel.send(f"集合するんだぞ！ {mention_text}")

        elif payload.emoji.name == "ℹ️":
            if embed.fields:
                embed.clear_fields()
            else:
                embed.add_field(name="#コマンド一覧", value=">>>", inline=True)
                embed.add_field(name="埋め込み起動", value="`!amo`", inline=True)
                embed.add_field(name="タイトル付き起動", value="`!amo タイトル`", inline=True)
                embed.add_field(name="メンバー手動追加", value="`!ad @名前`", inline=True)
                embed.add_field(name="メンバー手動削除", value="`!rm @名前`", inline=True)
                embed.add_field(name="Botコメント削除", value="`!dbm`", inline=True)
                embed.add_field(name="埋め込みタイトル変更", value="`!title タイトル`", inline=True)
                embed.add_field(name="あふれたよ通知", value="`!ome @名前`", inline=True)
                embed.add_field(name="表示名確認", value="`!n`", inline=True)
            await message.edit(embed=embed)

        elif payload.emoji.name == "🖼️":
            file_path = "image3.jpg"
            with open(file_path, "rb") as file:
                image = discord.File(file)
            await channel.send(file=image, content="もう集まってるよ～ん！")


@bot.command(name="ad")
async def add_usernames(ctx: commands.Context,  *names):
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=30):
        if message.embeds:
            for embed in message.embeds:
                if embed.type == "rich":
                    break
            if embed:
                break
    if embed:
        dsc_txt = embed.description
        for name in names:
            if name not in dsc_txt:
                dsc_txt += "\n" + name
        line_count = len(dsc_txt.split("\n")) - 1
        embed.description = dsc_txt
        footer_lines = embed.footer.text.split("\n")
        if line_count > 11:
            modified_first_line = "■"*11 + " over"
        elif line_count == 11:
            modified_first_line = "■"*line_count + " 集まった！"
            file_path = "image.jpg"
            with open(file_path, "rb") as file:
                image = discord.File(file)
            await ctx.channel.send(file=image, content="集まったよ～みんなありがと～")
            await message.add_reaction("🖼️")
        else:
            modified_first_line = "■"*line_count + "□"*(11 - line_count) + f" あと{11 - line_count}人"
        footer_lines[0] = modified_first_line
        embed.set_footer(text="\n".join(footer_lines))
        embed.timestamp = datetime.datetime.today()
        await message.edit(embed=embed)

@bot.command(name="rm")
async def rem_username(ctx: commands.Context, username: str):
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=30):
        if message.embeds:
            for embed in message.embeds:
                if embed.type == "rich":
                    break
            if embed:
                break
    if embed:
        lines = embed.description.split("\n")
        new_description = ""
        deleted = False
        for line in lines:
            if line.strip() != username:
                new_description += line + "\n"
            elif not deleted:
                deleted = True
            else:
                new_description += line + "\n"
        embed.description = new_description.rstrip("\n")
        line_count = len(embed.description.split("\n")) - 1
        footer_text = embed.footer.text
        footer_lines = footer_text.split("\n")
        if line_count > 11:
            modified_first_line = "■"*11 + " over"
        elif line_count <= 0:
            modified_first_line = "□"*11
        elif line_count == 11:
            modified_first_line = "■"*line_count + " 集まった！"
        else:
            modified_first_line = "■"*line_count + "□"*(11 - line_count) + f" あと{11 - line_count}人"
        footer_lines[0] = modified_first_line
        embed.set_footer(text="\n".join(footer_lines))
        embed.timestamp = datetime.datetime.today()
        await message.edit(embed=embed)

@bot.command(name="amo")
async def create_embed_with_reaction(ctx: commands.Context, title_text: str = "nothing"):
    await ctx.message.delete()
    if title_text != "nothing":
        title = f"あもあす募集だよ：{title_text}"
    else:
        title = "あもあす募集だよ"
    embed = discord.Embed(title=title, color=0x738ADB, description="**めんばー**")
    embed.set_footer(text="□□□□□□□□□□□\n参加者は✋をクリック")
    embed.timestamp = datetime.datetime.today()
    message = await ctx.send(embed=embed)
    await message.add_reaction("✋")
    await message.add_reaction("🔄")
    await message.add_reaction("🔔")
    await message.add_reaction("📢")
    await message.add_reaction("ℹ️")

@bot.command(name="dbm")
async def del_bot_msg(ctx: commands.Context, num: int = 1):
    await ctx.message.delete()
    bot_msgs = []
    async for message in ctx.channel.history(limit=50):
        if message.author.bot:
            bot_msgs.append(message)
    num = min(num, len(bot_msgs))
    for message in bot_msgs[:num]:
        await message.delete()
        await asyncio.sleep(0.5)

@bot.command(name="title")
async def change_title(ctx: commands.Context, title_text: str):
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=30):
        if message.embeds:
            for embed in message.embeds:
                if embed.type == "rich":
                    break
            if embed:
                break
    if embed:
        embed.title = title_text
        await message.edit(embed=embed)

@bot.command(name="ome")
async def omenosekinekara(ctx: commands.Context, username: str):
    await ctx.message.delete()
    file_path = "image4.jpg"
    with open(file_path, "rb") as file:
        image = discord.File(file)
    await ctx.channel.send(file=image, content=username)

@bot.command(name="n")
async def name_viewer(ctx: commands.Context):
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=30):
        if message.embeds:
            for embed in message.embeds:
                if embed.type == "rich":
                    break
            if embed:
                break
    if embed:
        user_ids = re.findall(r'@[0-9]{18,20}', embed.description)
        user_ids = list(map(lambda x: int(x.replace('@', '')), user_ids))
        names = []
        if ctx.guild.id:
            guild = bot.get_guild(ctx.guild.id)
            for user_id in user_ids:
                member = await guild.fetch_member(user_id)
                if member.nick:
                    names.append(member.nick)
                elif member.display_name:
                    names.append(member.display_name)
                else:
                    names.append(member.name)
            name_txt = "\n".join(names)
            msg = await ctx.channel.send(f"```\n{name_txt}\n```")
            await msg.add_reaction('❌')

bot.run(TOKEN)
import discord
from discord.ext import commands
import re
import datetime

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_raw_reaction_add(payload):
  if payload.member.bot:
    return
  channel = bot.get_channel(payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  user = await bot.fetch_user(payload.user_id)
  member = payload.member
  if payload.emoji.name == '✋':
    await message.remove_reaction(payload.emoji, member)
    embed = message.embeds[0]
    if embed:
      user_mention = f'<@{user.id}>'
      new_description = embed.description
      footer_text = embed.footer.text
      footer_lines = footer_text.split('\n')
      if user_mention not in new_description:
        new_description += f'\n{user_mention}'
        line_count = len(new_description.split('\n')) - 1
        if line_count > 11:
          modified_first_line = '■' * 11 + ' over'
        elif line_count == 11:
          modified_first_line = '■' * line_count + ' 集まった！'
          file_path = "image.jpg"
          with open(file_path, "rb") as file:
            image = discord.File(file)
            await channel.send(file=image, content="集まったよ～みんなありがと～")
        else:
          modified_first_line = '■' * line_count + '□' * (11 - line_count) + f' あと{11 - line_count}人'
      else:
        new_description = embed.description.replace(f'\n{user_mention}', '')
        line_count = len(new_description.split('\n')) - 1
        if line_count > 11:
          modified_first_line = '■' * 11 + ' over'
        else:
          modified_first_line = '■' * line_count + '□' * (11 - line_count) + f' あと{11 - line_count}人'
      updated_embed = discord.Embed.from_dict(embed.to_dict())
      updated_embed.description = new_description
      footer_lines[0] = modified_first_line
      updated_embed.set_footer(text='\n'.join(footer_lines))
      updated_embed.timestamp = datetime.datetime.today()
      await message.edit(embed=updated_embed)

  elif payload.emoji.name == '🔄':
    await message.remove_reaction(payload.emoji, member)
    embed = message.embeds[0]
    if embed:
      new_embed = discord.Embed.from_dict(embed.to_dict())
      await message.delete()
      new_embed.timestamp = datetime.datetime.today()
      new_message = await channel.send(embed=new_embed)
      await new_message.add_reaction('✋')
      await new_message.add_reaction('🔄')
      await new_message.add_reaction('👥')
      await new_message.add_reaction('🔔')
      await new_message.add_reaction('📢')
      await new_message.add_reaction('ℹ️')

  elif payload.emoji.name == '👥':
    await message.remove_reaction(payload.emoji, member)
    embed = message.embeds[0]
    if embed:
      line_count = len(embed.description.split('\n')) - 1
      if line_count >= 11:
        await channel.send("もー集まってる！")
      else:
        await channel.send(f"あと{11 - line_count}人だよ！@everyone")

  elif payload.emoji.name == '🔔':
    await message.remove_reaction(payload.emoji, member)
    await channel.send("募集してるよ！@everyone")

  elif payload.emoji.name == '📢':
    await message.remove_reaction(payload.emoji, member)
    embed = message.embeds[0]
    if embed:
      user_mentions = re.findall(r'@(\w+)', embed.description)
      if user_mentions:
        mention_text = ' '.join([f"<@{mention}>" for mention in user_mentions])
        await channel.send(f"集合するんだぞ！ {mention_text}")

  elif payload.emoji.name == 'ℹ️':
    await message.remove_reaction(payload.emoji, member)
    embed = message.embeds[0]
    if embed:
      if embed.fields:
        embed.clear_fields()
      else:
        embed.add_field(name='###コマンド一覧###\n \n埋め込み起動',
                        value='`!amo`',
                        inline=False)
        embed.add_field(name='タイトル付き起動', value='`!amo タイトル`', inline=True)
        embed.add_field(name='メンバー手動追加', value='`!ad @名前`', inline=True)
        embed.add_field(name='メンバー手動削除', value='`!rm @名前`', inline=True)
        embed.add_field(name='一括削除', value='`!reset_all`', inline=True)
        embed.add_field(name='everyone通知', value='`!notif`', inline=True)
        embed.add_field(name='メンバーにメンション', value='`!shout`', inline=True)
        embed.add_field(name='あと何人通知', value='`!at`', inline=True)
        embed.add_field(name='次戦?人募集', value='`!jisen ?`', inline=True)
        embed.add_field(name='しめ', value='`!sime`', inline=True)
        embed.add_field(name='Botコメント削除', value='`!dbm`', inline=True)
        embed.add_field(name='埋め込み削除', value='`!delete_e`', inline=True)
        embed.add_field(name='埋め込みタイトル変更', value='`!title タイトル`', inline=True)
      await message.edit(embed=embed)

@bot.command(name='ad')
async def add_username(ctx: commands.Context, username: str):
  await ctx.message.delete()
  async for message in ctx.channel.history(limit=30):
    if message.embeds:
      for embedded in message.embeds:
        if embedded.type == 'rich':
          target_embed = embedded
          break
      if target_embed:
        break
  if target_embed:
    new_embed = target_embed.copy()
    new_embed.description = f'{new_embed.description}\n{username}'
    line_count = len(new_embed.description.split('\n')) - 1
    footer_text = new_embed.footer.text
    footer_lines = footer_text.split('\n')
    if line_count > 11:
      modified_first_line = '■' * 11 + ' over'
    elif line_count == 11:
      modified_first_line = '■' * line_count + f' 集まった！'
      file_path = "image.jpg"
      with open(file_path, "rb") as file:
        image = discord.File(file)
        await ctx.channel.send(file=image, content="集まったよ～みんなありがと～")
    else:
      modified_first_line = '■' * line_count + '□' * (11 - line_count) + f' あと{11 - line_count}人'
    footer_lines[0] = modified_first_line
    new_embed.set_footer(text='\n'.join(footer_lines))
    new_embed.timestamp = datetime.datetime.today()
    await message.edit(embed=new_embed)

@bot.command(name='ada')
async def add_usernames(ctx: commands.Context,  *names):
  await ctx.message.delete()
  async for message in ctx.channel.history(limit=30):
    if message.embeds:
      for embedded in message.embeds:
        if embedded.type == 'rich':
          target_embed = embedded
          break
      if target_embed:
        break
  if target_embed:
    new_embed = target_embed.copy()
    names_text = "\n".join(names)
    new_embed.description = f'{new_embed.description}\n{names_text}'
    line_count = len(new_embed.description.split('\n')) - 1
    footer_text = new_embed.footer.text
    footer_lines = footer_text.split('\n')
    if line_count > 11:
      modified_first_line = '■' * 11 + ' over'
    elif line_count == 11:
      modified_first_line = '■' * line_count + f' あと{11 - line_count}人'
      file_path = "image.jpg"
      with open(file_path, "rb") as file:
        image = discord.File(file)
        await ctx.channel.send(file=image, content="集まったよ～みんなありがと～")
    else:
      modified_first_line = '■' * line_count + '□' * (11 - line_count) + f' あと{11 - line_count}人'
    footer_lines[0] = modified_first_line
    new_embed.set_footer(text='\n'.join(footer_lines))
    new_embed.timestamp = datetime.datetime.today()
    await message.edit(embed=new_embed)

@bot.command(name='rm')
async def rem_username(ctx: commands.Context, username: str):
  await ctx.message.delete()
  async for message in ctx.channel.history(limit=30):
    if message.embeds:
      for embedded in message.embeds:
        if embedded.type == 'rich':
          target_embed = embedded
          break
      if target_embed:
        break
  if target_embed:
    new_embed = target_embed.copy()
    description_lines = new_embed.description.split('\n')
    updated_description = ''
    deleted = False
    for line in description_lines:
      if line.strip() != username:
        updated_description += line + '\n'
      elif not deleted:
        deleted = True
      else:
        updated_description += line + '\n'
    new_embed.description = updated_description.rstrip('\n')
    line_count = len(new_embed.description.split('\n')) - 1
    footer_text = new_embed.footer.text
    footer_lines = footer_text.split('\n')
    if line_count > 11:
      modified_first_line = '■' * 11 + ' over'
    else:
      modified_first_line = '■' * line_count + '□' * (11 - line_count) + f' あと{11 - line_count}人'
    footer_lines[0] = modified_first_line
    new_embed.set_footer(text='\n'.join(footer_lines))
    new_embed.timestamp = datetime.datetime.today()
    await message.edit(embed=new_embed)

@bot.command(name='amo')
async def create_embed_with_reaction(ctx: commands.Context,
                                     title_text: str = 'nothing'):
  await ctx.message.delete()
  if title_text != 'nothing':
    title = f'あもあす募集だよ：{title_text}'
  else:
    title = 'あもあす募集だよ'
  embed = discord.Embed(title=title, color=0x738ADB, description='**めんばー**')
  embed.set_footer(text='□□□□□□□□□□□\n参加者は✋をクリック')
  embed.timestamp = datetime.datetime.today()

  message = await ctx.send(embed=embed)
  await message.add_reaction('✋')
  await message.add_reaction('🔄')
  await message.add_reaction('👥')
  await message.add_reaction('🔔')
  await message.add_reaction('📢')
  await message.add_reaction('ℹ️')

@bot.command(name='reac')
async def handle_reaction(ctx: commands.Context):
  await ctx.message.delete()
  async for message in ctx.channel.history(limit=30):
    if message.embeds:
      for embedded in message.embeds:
        if embedded.type == 'rich':
          target_embed = embedded
          break
      if target_embed:
        break
  if target_embed:
    author = message.author
    reactions = message.reactions
    description_lines = target_embed.description.split('\n')
    new_embed = target_embed.copy()
    flg_jpg = 0
    for reaction in reactions:
      async for user in reaction.users():
        if author != user:
          await reaction.remove(user)
          if reaction.emoji == '✋':
            flg = 0
            for line in description_lines:
              if line.strip() == user:
                flg = 1
                break
            if flg != 1:
              new_embed.description = f'{new_embed.description}\n<@{user.id}>'
              line_count = len(new_embed.description.split('\n')) - 1
              if line_count == 11:
                flg_jpg = 1
    line_count = len(new_embed.description.split('\n')) - 1
    footer_text = new_embed.footer.text
    footer_lines = footer_text.split('\n')
    if line_count > 11:
      modified_first_line = '■' * 11 + ' over'
      if flg_jpg == 1:
        file_path = "image.jpg"
        with open(file_path, "rb") as file:
          image = discord.File(file)
          await ctx.channel.send(file=image, content="集まったよ～みんなありがと～")
    elif line_count == 11:
      modified_first_line = '■' * line_count + ' 集まった！'
      file_path = "image.jpg"
      with open(file_path, "rb") as file:
        image = discord.File(file)
        await ctx.channel.send(file=image, content="集まったよ～みんなありがと～")
    else:
      modified_first_line = '■' * line_count + '□' * (11 - line_count)  + f' あと{11 - line_count}人'
    footer_lines[0] = modified_first_line
    new_embed.set_footer(text='\n'.join(footer_lines))
    await message.edit(embed=new_embed)

@bot.command(name='at')
async def count_description_lines(ctx: commands.Context):
  await ctx.message.delete()
  async for message in ctx.channel.history(limit=30):
    if message.embeds:
      for embedded in message.embeds:
        if embedded.type == 'rich':
          target_embed = embedded
          break
      if target_embed:
        break
  if target_embed:
    line_count = len(target_embed.description.split('\n')) - 1
    if line_count >= 11:
      await ctx.channel.send("もー集まってる！")
    else:
      await ctx.channel.send(f"あと{11 - line_count}人だよ！@everyone")

@bot.command(name='delete_e')
async def delete_embed(ctx: commands.Context):
  await ctx.message.delete()
  async for message in ctx.channel.history(limit=30):
    if message.embeds:
      for embedded in message.embeds:
        if embedded.type == 'rich':
          await message.delete()
          return

@bot.command(name='dbm')
async def delete_bot_messages(ctx: commands.Context, num: int = 1):
  await ctx.message.delete()
  channel = ctx.channel
  bot_messages = []
  async for message in channel.history(limit=30):
    if message.author.bot:
      bot_messages.append(message)
  num = min(num, len(bot_messages))
  for message in bot_messages[:num]:
    await message.delete()

@bot.command(name='reset_all')
async def reset_username(ctx: commands.Context):
  await ctx.message.delete()
  async for message in ctx.channel.history(limit=30):
    if message.embeds:
      for embedded in message.embeds:
        if embedded.type == 'rich':
          target_embed = embedded
          break
      if target_embed:
        break
  if target_embed:
    new_embed = target_embed.copy()
    new_embed.description = '**めんばー**'
    new_embed.set_footer(text='□' * 11 + '\n参加者は✋をクリック')
    new_embed.timestamp = datetime.datetime.today()
    await message.edit(embed=new_embed)

@bot.command(name='notif')
async def notification(ctx: commands.Context):
  await ctx.message.delete()
  await ctx.channel.send("募集してるよ！@everyone")

@bot.command(name='jisen')
async def next_recruit(ctx: commands.Context, num: int):
  await ctx.message.delete()
  await ctx.channel.send(f"次戦@{num} @everyone")

@bot.command(name='sime')
async def rec_stop(ctx: commands.Context):
  await ctx.message.delete()
  await ctx.channel.send("〆")

@bot.command(name='shout')
async def mention_member(ctx: commands.Context):
  await ctx.message.delete()
  async for message in ctx.channel.history(limit=30):
    if message.embeds:
      for embedded in message.embeds:
        if embedded.type == 'rich':
          target_embed = embedded
          break
      if target_embed:
        break
  if target_embed:
    user_mentions = re.findall(r'@(\w+)', target_embed.description)
    if user_mentions:
      mention_text = ' '.join([f"<@{mention}>" for mention in user_mentions])
      await ctx.channel.send(f"集合するんだぞ！ {mention_text}")

@bot.command(name='title')
async def change_title(ctx: commands.Context, title_text: str):
  await ctx.message.delete()
  async for message in ctx.channel.history(limit=30):
    if message.embeds:
      for embedded in message.embeds:
        if embedded.type == 'rich':
          target_embed = embedded
          break
      if target_embed:
        break
  if target_embed:
    target_embed.title = title_text
    await message.edit(embed=target_embed)

async def on_ready():
  print('Bot is ready.')

bot.run('****')

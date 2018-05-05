import discord
import os
import asyncio

client = discord.Client()
version = "0.1"

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    token = os.environ.get('TOKEN')
else:
    import secreto
    token = secreto.token

def toint(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

@client.event
async def on_ready():
    print("=================================")
    print("Bot iniciado com sucesso!")
    print (client.user.name)
    print(f"Bot Version: {version}")
    print("=================================")
    await client.change_presence(game=discord.Game(name='no mc-perfect.com.br'), status=discord.Status.dnd)

@client.event
async def on_message(message):
#SAY
    if message.content.lower().startswith("!say"):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        msg = message.content[5:2000]
        await client.send_message(message.channel, msg)
        await client.delete_message(message)
#AVISO
    if message.content.startswith('!aviso'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        await client.delete_message(message)
        try:
            user = message.author
            msg = message.content[7:]

            embed = discord.Embed(
                title=" 📢 AVISO 📢",
                description="{}".format(msg),
                color=0xe67e22
            )
            embed.set_footer(
                text="Enviado por: " + user.name,
                icon_url=user.avatar_url
            )

            await client.send_message(message.channel, "@everyone")
            await client.send_message(message.channel, embed=embed)
        finally:
            pass

    if message.content.lower().startswith('!apagar'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        qntdd = message.content.strip('!apagar ')
        qntdd = toint(qntdd)
        if qntdd <= 100:
            msg_author = message.author.mention
            await client.delete_message(message)
            await asyncio.sleep(1)
            deleted = await client.purge_from(message.channel, limit=qntdd)
            botmsgdelete = await client.send_message(message.channel, 'Deletei {} mensagens de um pedido de {} para {}'.format(len(deleted), qntdd, msg_author))
            await asyncio.sleep(5)
            await client.delete_message(botmsgdelete)
        else:
            botmsgdelete = await client.send_message(message.channel, 'Utilize o comando digitando /apagar <numero de 1 a 100>')
            await asyncio.sleep(5)
            await client.delete_message(message)
            await client.delete_message(botmsgdelete)

#AVATAR
    elif message.content.lower().startswith('!avatar'):
        try:
            membro = message.mentions[0]
            avatarembed = discord.Embed(
                title="",
                color=0xe7002f,
                description="**[Clique aqui](" + membro.avatar_url + ") para acessar o link do avatar!**"
            )
            avatarembed.set_author(name=membro.name)
            avatarembed.set_image(url=membro.avatar_url)
            await client.send_message(message.channel, embed=avatarembed)
        except:
            avatarembed2 = discord.Embed(
                title="",
                color=0xe7002f,
                description="**[Clique aqui](" + message.author.avatar_url + ") para acessar o link do avatar!**"
            )
            avatarembed2.set_author(name=message.author.name)
            avatarembed2.set_image(url=message.author.avatar_url)
            await client.send_message(message.channel, embed=avatarembed2)


@client.event
async def on_member_join(member):

      grupo = discord.utils.find(lambda g: g.name == "⏰ AGUARDE", member.server.roles)
      await client.add_roles(member, grupo)

      channel = client.get_channel('441239463855783937')
      serverchannel = member.server.default_channel
      embedmsg = discord.Embed(
          title="Olá {}!".format(member.name),
          description="Bem vindo ao discord da rede de servidores Perfect Network!\n"
                      "\n"
                      "Aguarde um superior para sua tag ser setada.",
          color=0xe7002f,
      )
      embedmsg.set_thumbnail(url=member.avatar_url)

      await client.send_message(channel, embed=embedmsg)
client.run(token)
import discord
from discord.ext import commands
from discord.ui import Button

import qrcode


PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
ticket_counter = 1



@bot.event
async def on_message(message):

    await bot.process_commands(message)

    if message.channel.id == 1198779037796012152:

        await message.delete()

@bot.event
async def on_ready():
    print(f'Logando com {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command(name='botvenda')
async def send_fixed_message(ctx):
    fixed_message_content = (
        "Prezados Clientes da 2G Store,\n\n"
        "Infelizmente, para adquirir um bot personalizado, não \n\n"
        "há um preço fixo. Basta abrir um ticket e marcar o @DEV"
        "para que possamos responder o mais rápido possível. "
        "Para criar um ticket, digite **!**__***ticket***__ "
        "neste chat."
        "Agradecemos pela confiança contínua em nossos serviços e produtos.\n\n"

        "Atenciosamente,"
        "2G Store"

     
    )
    await ctx.send(fixed_message_content)

@bot.command(name='fix')
async def send_fixed_message(ctx):
    fixed_message_content = (
        "Prezados Clientes da 2G Store,\n\n"
        "Esperamos que estejam todos bem. Gostaríamos de informar que agora tornamos mais fácil para vocês solicitar suporte ou assistência técnica.\n\n"
        "Para criar um ticket, basta digitar **!**__***ticket***__ neste chat. Estamos aqui para ajudar e resolver qualquer questão que possa surgir. "
        "Agradecemos pela confiança contínua em nossos serviços e produtos.\n\n"
        "Fiquem à vontade para nos contatar sempre que necessário. Estamos comprometidos em oferecer o melhor atendimento possível."
    )
    await ctx.send(fixed_message_content)



@bot.command(name='qrcode')
async def gerar_qrcode_pix(ctx):
    email_pix = 'eliseuvasconcellos@gmail.com'

    url_pagamento_pix = f'pix:nubank.com.br/p/{email_pix}'


    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(url_pagamento_pix)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save("pix_qrcode.png")

    await ctx.send(f"Aqui está o seu QR Code Pix para pagamento no Nubank:")
    await ctx.send(file=discord.File("pix_qrcode.png"))

@bot.command(name='ticket')
async def open_ticket(ctx):
    global ticket_counter
    ticket_channel_name = f'ticket-{ctx.author.name}-{ticket_counter}'

    guild = ctx.guild
    ticket_channel = await guild.create_text_channel(ticket_channel_name)

    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
    for role in guild.roles:
        if role.permissions.administrator:
            await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)

   
    products_available = {
        "Bot Para Discord Personalizado": "💳",
        "Produto B": "🎮",
        "Produto C": "📷",
        # Adicione mais produtos conforme necessário
    }


    product_list = "Lista de Produtos Disponíveis:\n\n"
    for product, emoji in products_available.items():
        product_list += f"{emoji} {product}\n"

 
    message = await ticket_channel.send(f'Bem-vindo ao seu ticket, {ctx.author.mention}!\n'
                                        f'O que você gostaria de comprar?\n\n{product_list}')

    
    for emoji in products_available.values():
        await message.add_reaction(emoji)

    await ctx.message.delete()
    ticket_counter += 1


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return 
    if isinstance(reaction.message.channel, discord.TextChannel) and reaction.message.channel.name.startswith('ticket-'):

        products_available = {
            "Produto A": "💳",
            "Produto B": "🎮",
            "Produto C": "📷",

        }
        for product, emoji in products_available.items():
            if str(reaction.emoji) == emoji:
                await generate_and_send_qrcode(reaction.message.channel, user, product)
                break

async def generate_and_send_qrcode(channel, user, product):
    email_pix = 'eliseuvasconcellos@gmail.com'
    url_pagamento_pix = f'pix:nubank.com.br/p/{email_pix}'

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(url_pagamento_pix)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save(f"{product}_qrcode.png")

    await channel.send(f"{user.mention}, aqui está o QR Code para comprar {product}:")
    await channel.send(file=discord.File(f"{product}_qrcode.png"))


bot.run('MTE5ODQ0MTc1Njc3NDExMzI5MA.Gxnn06.PI5H3jAFc-rFKdiwr4zxWYjc32da5uB9jPy4EY')

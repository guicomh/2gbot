import discord
from discord.ext import commands
from discord.ui import Button
import qrcode
import asyncio

PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
ticket_counter = 1


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.channel.id == 119877903779601215:  # ID do primeiro canal
        await message.delete()

    if message.channel.id == 1199461061477290054:  # ID do segundo canal
        await message.delete()


@bot.event
async def on_ready():
    print(f'Logando com {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command(name='rockstar')
async def send_fixed_message(ctx):
    # Criar mensagem
    fixed_message_content = (
        "Prezados Clientes da 2G Store,\n\n"
        "Para adquirir uma Conta Rockstar,\n"
        f"crie um ticket em {ctx.author.mention}.\n "
        "Agradecemos pela confiança contínua em nossos serviços e produtos.\n\n"
        "Atenciosamente,\n\n"
        "**2G Store**"
    )

    # Criar embed
    embed = discord.Embed(title="Abrir Ticket de Compras", description=fixed_message_content, color=discord.Color.blue())

    # Adicionar botão
    button = Button(style=discord.ButtonStyle.green, label="Abrir Ticket")
    view = discord.ui.View()
    view.add_item(button)

    # Enviar mensagem com botão
    await ctx.send(embed=embed, view=view)


@bot.command(name='botvenda')
async def send_fixed_message(ctx):
    ticket_channel_name = '📝-ticket'
    ticket_channel = discord.utils.get(ctx.guild.channels, name=ticket_channel_name)

    if ticket_channel:
        fixed_message_content = (
            f"Prezados Clientes da 2G Store,\n\n"
            "Infelizmente, para adquirir um *bot personalizado*, não \n"
            "há um preço fixo.\n"
            "Para que possamos responder o mais rápido possível, crie um ticket em {ticket_channel.mention}.\n "
            "Agradecemos pela confiança contínua em nossos serviços e produtos.\n\n"
            "Atenciosamente,\n\n"
            "**2G Store**"
        )
        await ctx.send(fixed_message_content, allowed_mentions=discord.AllowedMentions.none())
    else:
        await ctx.send(f"Canal de ticket não encontrado.")

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

    for role in guild.roles:
        if role.permissions.administrator:
            await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)

    products_available = {
        "Bot Para Discord Personalizado",
        "Produto B",
        "Produto C",
        # Adicione mais produtos conforme necessário
    }

    product_list = "Lista de Produtos Disponíveis:\n\n"
    for product in products_available:
        product_list += f"{product}\n"

    message = await ticket_channel.send(f'Bem-vindo ao seu ticket, {ctx.author.mention}!\n'
                                        f'O que você gostaria de comprar?\n\n{product_list}')

    await ctx.message.delete()
    ticket_counter += 1

bot.run('MTE5ODQ0MTc1Njc3NDExMzI5MA.GMFSyc.JwR4YD9x3QXi9dXit90tXjAxiT8ocjRIwxhnyY')

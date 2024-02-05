import discord
from discord.ext import commands
from discord.ui import Button, View
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

    if message.channel.id == 1198779037796012152 :  # ID do primeiro canal
        await message.delete()

    if message.channel.id == 119946106147729005:  # ID do segundo canal
        await message.delete()


@bot.event
async def on_ready():
    print(f'Logando com {bot.user.name} ({bot.user.id})')
    print('------')


@bot.event
async def on_ready():
    print(f'Bot está online como {bot.user.name}')


@bot.command(name='rockstar')
async def send_fixed_message(ctx):
    # Informações de preço e estoque
    rockstar_price = "R$ 3,00"
    rockstar_stock = 2  # Quantidade disponível em estoque

    # Criar mensagem
    fixed_message_content = (
        f"```\n"
        f"Prezados Clientes da 2G Store,\n\n"
        f"Para adquirir uma Conta Rockstar\n\n"
        f"Preço = {rockstar_price}\n"
        f"Estoque disponível: {rockstar_stock} unidades.\n\n"
        "Agradecemos pela confiança contínua em nossos serviços e produtos.\n\n"
        "Atenciosamente,\n\n"
        "2G Store"
        "```\n"
    )

    # Criar embed
    embed = discord.Embed(title="Abrir Ticket de Compras", description=fixed_message_content, color=discord.Color.blue())

    # Criar botão
    button = Button(style=discord.ButtonStyle.green, label="Comprar")

    # Adicionar botão à view
    view = discord.ui.View()
    view.add_item(button)

    # Enviar mensagem com embed e botão
    message = await ctx.send(embed=embed, view=view)


@bot.event
async def on_button_click(interaction):
    if interaction.component.label == "Comprar":
        # Criar um novo canal de compra
        new_channel_name = f'compra-{interaction.user.name}'
        guild = interaction.guild
        new_channel = await guild.create_text_channel(new_channel_name)

        # Configurar permissões para o autor e roles relevantes
        await new_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        for role in guild.roles:
            if role.permissions.administrator:
                await new_channel.set_permissions(role, read_messages=True, send_messages=True)

        # Enviar uma mensagem inicial no novo canal
        await new_channel.send(f'Bem-vindo ao canal de compra, {interaction.user.mention}!')

        # Responder ao botão
        await interaction.response.send_message("Canal de compra criado com sucesso!")


@bot.command(name='botvenda')
async def send_fixed_message(ctx):
    ticket_channel_name = '📝-ticket'
    ticket_channel = discord.utils.get(ctx.guild.channels, name=ticket_channel_name)

    if ticket_channel:
        fixed_message_content = (
            "```\n"
            "Prezados Clientes da 2G Store,\n\n"
            "Infelizmente, para adquirir um bot personalizado, não \n"
            "há um preço fixo.\n"
            f"Para que possamos responder o mais rápido possível, crie um ticket em {ticket_channel.mention}.\n"
            "Agradecemos pela confiança contínua em nossos serviços e produtos.\n\n"
            "Atenciosamente,\n\n"
            "2G Store"
            "```\n"
        )
        await ctx.send(fixed_message_content, allowed_mentions=discord.AllowedMentions.none())
    else:
        await ctx.send("Canal de ticket não encontrado.")



@bot.command(name='fix')
async def send_fixed_message(ctx):
    fixed_message_content = (
        "```\n"
        "Prezados Clientes da 2G Store,\n\n"
        "Esperamos que estejam todos bem.\n"
        "Gostaríamos de informar que agora tornamos mais fácil\n" 
        "para vocês solicitar suporte ou assistência técnica.\n\n"
        "Para criar um ticket, basta digitar\n"
        "!ticket \n" 
        "neste chat. \n"
        "Agradecemos pela confiança contínua em nossos"
        "serviços e produtos.\n\n"
        "```\n"
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
        "Conta Rockstar",
        # Adicione mais produtos conforme necessário
    }

    product_list = "Lista de Produtos Disponíveis:\n\n"
    for product in products_available:
        product_list += f"{product}\n"

    dono_role = discord.utils.get(guild.roles, name="Dono")
    if dono_role:
        await ticket_channel.set_permissions(dono_role, read_messages=True, send_messages=True)

    message = await ticket_channel.send(f'Bem-vindo ao seu ticket, {ctx.author.mention}!\n'
                                        f'O que você gostaria de comprar?\n\n{product_list}'
                                        f'\n\n{dono_role.mention if dono_role else "Cargo de dono não encontrado!"}')
    

    await ctx.message.delete()
    ticket_counter += 1


@bot.command(name='criar_canal')
async def criar_canal(ctx):

    button = Button(style=discord.ButtonStyle.green, label="Criar Canal", custom_id="criar_canal_button")
    view = discord.ui.View()
    view.add_item(button)

    await ctx.send("Clique no botão para criar um novo canal de texto:", view=view)


@bot.event
async def on_button_click(interaction):
    if interaction.custom_id == "criar_canal_button":

        new_channel_name = f'canal-{interaction.user.name}'
        guild = interaction.guild
        new_channel = await guild.create_text_channel(new_channel_name)


        await new_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        for role in guild.roles:
            if role.permissions.administrator:
                await new_channel.set_permissions(role, read_messages=True, send_messages=True)

     
        await new_channel.send(f'Bem-vindo ao seu novo canal, {interaction.user.mention}!')

        await interaction.response.send_message("Canal criado com sucesso!")

bot.run('TOKEN DO BOT AQUI')

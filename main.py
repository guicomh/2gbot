import discord
from discord.ext import commands
import qrcode


PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
ticket_counter = 1

@bot.event
async def on_ready():
    print(f'Logando com {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command(name='fix')
async def send_fixed_message(ctx):
    fixed_message_content = (
        "Prezados Clientes da 2G Store,\n\n"
        "Esperamos que estejam todos bem. Gostaríamos de informar que agora tornamos mais fácil para vocês solicitar suporte ou assistência técnica.\n\n"
        "Para criar um ticket, basta digitar **!ticket** neste chat. Estamos aqui para ajudar e resolver qualquer questão que possa surgir. "
        "Agradecemos pela confiança contínua em nossos serviços e produtos.\n\n"
        "Fiquem à vontade para nos contatar sempre que necessário. Estamos comprometidos em oferecer o melhor atendimento possível."
    )
    await ctx.send(fixed_message_content)


@bot.command(name='qrcode')
async def gerar_qrcode_pix(ctx):
    # Substitua 'eliseuvasconcellos@gmail.com' pelo seu e-mail Pix
    email_pix = 'eliseuvasconcellos@gmail.com'

    # Gere a URL de pagamento Pix usando o e-mail como chave para o Nubank
    url_pagamento_pix = f'pix:nubank.com.br/p/{email_pix}'

    # Crie um QR code a partir da URL de pagamento
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(url_pagamento_pix)
    qr.make(fit=True)

    # Crie uma imagem a partir dos dados do QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Salve a imagem do QR code localmente (opcional)
    img.save("pix_qrcode.png")

    # Envie a imagem do QR code para o canal do Discord
    await ctx.send(f"Aqui está o seu QR Code Pix para pagamento no Nubank:")
    await ctx.send(file=discord.File("pix_qrcode.png"))


@bot.command(name='ticket')
async def open_ticket(ctx):
    global ticket_counter
    ticket_channel_name = f'ticket-{ctx.author.name}-{ticket_counter}'

    guild = ctx.guild
    ticket_channel = await guild.create_text_channel(ticket_channel_name)

    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

    await ticket_channel.send(f'Bem-vindo ao seu ticket, {ctx.author.mention}!\nO que você gostaria de comprar?')

    await ctx.message.delete()

    ticket_counter += 1



bot.run('MTE5ODQ0MTc1Njc3NDExMzI5MA.Gxnn06.PI5H3jAFc-rFKdiwr4zxWYjc32da5uB9jPy4EY')

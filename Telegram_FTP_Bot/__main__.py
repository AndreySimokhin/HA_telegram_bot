from twisted.internet import reactor

from options import Options
from ftp_server import FTPServer
from telegram_bot import Telegram_Bot


Options.load()
Options.init_folder()

Telegram_Bot.initialize(Options.token)
FTPServer().makeListener()

reactor.run()

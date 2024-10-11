from pathlib import Path
from twisted.protocols.ftp import FTPFactory, FTP, IFTPShell, FTPShell
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess
from twisted.internet import reactor
from twisted.python import filepath

from options import Options
from telegram_bot import Telegram_Bot


class FTPServerRealm():
    def __init__(self, ftp_directory, *args):
        self._ftp_directory = filepath.FilePath(ftp_directory)

    def requestAvatar(self, avatarId, mind, *interfaces):
        for iface in interfaces:
            if iface is IFTPShell:
                avatar = self.make_ftp_shell(avatarId, self._ftp_directory)
                return (
                    IFTPShell,
                    avatar,
                    getattr(avatar, "logout", lambda: None)
                )
        raise NotImplementedError()

    def make_ftp_shell(self, avatar_id, ftp_directory):
        return FTPShell(ftp_directory)


class FTPProtocol(FTP):
    def ftp_STOR(self, path: str):
        d = super(FTPProtocol, self).ftp_STOR(path)

        def _onStorComplete(d):
            self.onSTORComplete(path)
            return d

        d.addCallback(_onStorComplete)
        Options.logger.info(f'Loaded file: {path}')
        return d

    def onSTORComplete(self, path):
        path = Path(Options.folder).joinpath(path)
        Options.logger.info(f'Sending \"{path}\" file over telegram...')
        try:
            Telegram_Bot.send_file(path, Options.chat_id)
            Options.logger.info(f'Successfully delivered file "{path}" over telegram...')
        except Exception as exc:
            Options.logger.error(exc)

        try:
            Options.logger.info(f'Deleting file "{path}"...')
            path.unlink()
            Options.logger.info(f'File "{path}" deleted successfully!')
        except Exception as exc:
            Options.logger.error(f'Failed to delete file: {exc}')


class FTPServer():
    def __init__(
        self,
        ftp_directory: str = Options.folder,
        host: str = Options.host,
        port: int = Options.port,
    ):
        factory = FTPFactory()
        realm = FTPServerRealm(ftp_directory)
        portal = Portal(realm)
        portal.registerChecker(
            AllowAnonymousAccess()
        )

        factory.tld = ftp_directory
        factory.allowAnonymous = True
        factory.portal = portal
        factory.protocol = FTPProtocol
        self._factory = factory
        self._host = host
        self._port = port

    def makeListener(self):
        return reactor.listenTCP(
            self._port,
            self._factory,
            interface=self._host
        )

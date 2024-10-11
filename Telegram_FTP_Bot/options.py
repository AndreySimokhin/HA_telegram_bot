import pathlib
import json
import logging

CONFIG_PATH = "./data/options.json"

logger = logging.getLogger('Telegram FTP Bot')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%d.%m.%Y %HH:%MM:%SS',
)
channel = logging.StreamHandler()
channel.setFormatter(formatter)
logger.addHandler(channel)


class Options:
    folder: str = "./data/files"
    host: str = "127.0.0.1"
    port: int = 21

    token: str = None
    chat_id: str = None

    logger = logger

    @staticmethod
    def load():
        assert pathlib.Path(CONFIG_PATH).exists(), f"Configuration file \"{CONFIG_PATH}\" not found"
        with open(CONFIG_PATH, "r+") as fp:
            data: dict[str, str] = json.load(fp)

        Options.token = data.get('token', None)
        Options.chat_id = data.get('chat_id', None)
        Options.logger.info(f'Running with options: {Options.to_str()}')

    @staticmethod
    def init_folder():
        if not (path := pathlib.Path(Options.folder)).exists():
            path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def to_str() -> str:
        return json.dumps(
            Options.to_dict(),
            sort_keys=True,
            indent=4
        )

    @staticmethod
    def to_dict() -> dict[str, str | int]:
        return {
            'folder': Options.folder,
            'host': Options.host,
            'port': Options.port,
            'token': Options.token,
            'chat_id': Options.chat_id,
        }

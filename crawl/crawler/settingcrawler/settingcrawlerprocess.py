from crawler.db.MysqlActions import MysqlActions
from messages.messenger import DiscordMessenger
import threading
import queue



if __name__ == "__main__":
    message_queue: queue.Queue = queue.Queue(maxsize=10)
    messenger: DiscordMessenger = DiscordMessenger(message_queue=message_queue)
    setting_thread: threading.Thread = threading.Thread(daemon=True,)


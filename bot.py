from discord.ext import commands


class Skycord(commands.AutoShardedBot):
    """Skycord"""

    def __init__(self):
        super().__init__(self.get_prefix)


from internetAbstractScrapper.Publication import Publication


class TelegramPublication(Publication):
    def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.telegramId = ""
            self.telegramChannel = ""
            self.telegramChannelId = ""

    def setData(self, **kwargs):
        super().setData(**kwargs)
        self.telegramId = kwargs.get("telegramId", "")
        self.telegramChannel = kwargs.get("telegramChannel", "")
        self.telegramChannelId = kwargs.get("telegramChannelId", "")
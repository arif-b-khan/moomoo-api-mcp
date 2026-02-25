class _LoggerWrapper:
    def __init__(self):
        # Mimic structure used in server.py
        class _Console:
            def __init__(self):
                self.handlers = []

        self.console_logger = _Console()
        self.consoleHandler = None


class ft_logger:
    logger = _LoggerWrapper()

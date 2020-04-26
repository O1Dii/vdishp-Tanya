import abc


# Command

class Command(abc.ABC):
    def __init__(self, handler) -> None:
        self.handler = handler

    @abc.abstractmethod
    def __call__(self, target):
        pass


class ClickCommand(Command):
    def __call__(self, button) -> None:
        self.handler(button)


class NotifyCommand(Command):
    def __call__(self, event) -> None:
        if isinstance(event, dict):
            self.handler(event)


# Factory method

class CommandFactory:

    @staticmethod
    def construct(event_type: str, *args, **kwargs) -> Command:
        if event_type == 'click':
            cls = ClickCommand
        else:
            cls = NotifyCommand

        return cls(*args, **kwargs)


# Observer

class Publisher:
    def __init__(self) -> None:
        self.observers = dict()

    def __call__(self, event) -> None:
        if isinstance(event, dict):
            self.observers[event['owner'], event['type']](event)
        else:
            self.observers[(event, 'click')](event)

    def register(self, subscriber) -> None:
        cmd = CommandFactory.construct(subscriber[2], subscriber[1])

        self.observers.update({(subscriber[0], subscriber[2]): cmd})

    def unregister(self, observer) -> None:
        self.observers.pop((observer[0], observer[2]))

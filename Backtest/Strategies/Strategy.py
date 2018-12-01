
class Strategy(object):

    def enter(self, signals):
        raise NotImplementedError("Implement strategy enter function")

    def exit(self, signals):
        raise NotImplementedError("Implement strategy exit function")

    def get_data(self):
        raise NotImplementedError("Implement strategy get_data function")

    def get_signals(self):
        raise NotImplementedError("Implement strategy get_signals function")

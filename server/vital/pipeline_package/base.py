class SignalProcessingStep:
    def __init__(self, **kwargs):
        self.params = kwargs

    def apply(self, sig):
        raise NotImplementedError("Each processing step must implement the 'apply' method.")

    def description(self):
        return f"{self.__class__.__name__}()"

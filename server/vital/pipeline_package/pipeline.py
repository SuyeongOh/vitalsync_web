class Pipeline:
    def __init__(self, steps=None):
        if steps is None:
            steps = []
        self.steps = steps

    def add_step(self, step):
        self.steps.append(step)

    def apply(self, signal):
        for i, step in enumerate(self.steps):
            signal = step.apply(signal)
        return signal

    def get_processing_steps(self):
        descriptions = [step.description() for step in self.steps]
        return " -> ".join(descriptions)

    def get_steps_for_filename(self):
        descriptions = [step.description().replace(',', '_') for step in self.steps]
        return "_".join(descriptions)

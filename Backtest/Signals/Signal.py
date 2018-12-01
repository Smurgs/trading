
class Signal(object):

    def get_min_data_points(self):
        raise NotImplementedError("Implement indicator get_min_data_points function")

    def calculate(self, data_frames):
        raise NotImplementedError("Implement indicator calculate function")

    def _verify_size(self, data_frames):
        if len(data_frames) != self.get_min_data_points():
            raise AssertionError('Number of frames does not match number of data points required for indicator')
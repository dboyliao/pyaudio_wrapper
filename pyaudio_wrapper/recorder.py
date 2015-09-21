import pyaudio, io

class MicrophoeRecorder(object):

    def __init__(self, device_index = None, sample_rate = 16000, chunck_size =1024, bit_width = pyaudio.paInt16, channels = 1):
        assert device_index is None or isinstance(device_index, int), "`device_index` must be integer."
        if device_index is not None:
            audio = pyaudio.PyAudio()
            count = audio.get_device_count()
            audio.terminate()
            assert 0 <= device_index < count, "`device_index` out of range: {} out of {}".format(device_index, count)
        assert isinstance(sample_rate, int) and sample_rate > 0, "`sample_rate` must be positive."
        assert isinstance(chunck_size, int) and chunck_size > 0, "`chunck_size` must be positive."

        self.device_index = device_index
        self.sample_rate = sample_rate
        self.__chunck_size = chunck_size
        self.__bit_width = pyaudio.paInt16
        self.__sample_rate = sample_rate
        self.channels = channels

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @property
    def input_stream(self):
        audio_client = pyaudio.PyAudio()
        stream = audio_client.open(
                input_device_index = self.device_index,
                channels = self.channels,
                rate = self.SAMPLE_RATE,
                format = self.BIT_WIDTH,
                frames_per_buffer = self.CHUNCK_SIZE,
                input = True
                )
        return stream

    @property
    def CHUNCK_SIZE(self):
        return self.__chunck_size

    @property
    def BIT_WIDTH(self):
        return self.__bit_width

    @property
    def SAMPLE_RATE(self):
        return self.__sample_rate

    @CHUNCK_SIZE.setter
    def CHUNCK_SIZE(self, value):
        if not self.__chunck_size is None:
            raise RuntimeError("Can not modify the `CHUNCK_SIZE`.")
        else:
            self.__chunck_size = value

    @BIT_WIDTH.setter
    def BIT_WIDTH(self, value):
        if not self.__bit_width is None:
            raise RuntimeError("Can not modify the `BIT_WIDTH`.")
        else:
            self.__bit_width = value

    @SAMPLE_RATE.setter
    def SAMPLE_RATE(self, value):
        if not self.__sample_rate is None:
            raise RuntimeError("Can not modify the `SAMPLE_RATE`.")
        else:
            self.__sample_rate = value

    def listen(self):
        pass

    def plot(self):
        pass

    def play(self, start, end):
        pass

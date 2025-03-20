import os
import numpy as np
from gnuradio import gr

class segment_threshold_recorder(gr.sync_block):
    """
    This block processes the incoming IQ stream by:
      - Splitting the data into 0.5-second segments.
      - If any sample in a segment exceeds a certain (linear) threshold,
        that segment is considered part of a message.
      - If no sample in the segment is above the threshold, and there was an ongoing recording,
        that segment marks the end of the message. The message is then saved to disk with a dynamic filename
        (e.g., msg_0.dat, msg_1.dat, …).
      - After that, it resumes searching for a new message.
    """
    def __init__(self, threshold=0.300, samp_rate=2.4e6, output_dir=r"C:\Users\hakan\Documents\lora_recordings"):
        gr.sync_block.__init__(
            self,
            name="segment_threshold_recorder",
            in_sig=[np.complex64],
            out_sig=[]
        )
        self.threshold = threshold
        self.samp_rate = int(samp_rate)
        self.segment_duration = 0.5
        self.chunk_size = int(self.samp_rate * self.segment_duration)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.recording = False
        self.current_message = []
        self.segment_buffer = []
        self.msg_count = 0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        self.segment_buffer.extend(in0)

        while len(self.segment_buffer) >= self.chunk_size:
            segment = np.array(self.segment_buffer[:self.chunk_size], dtype=np.complex64)
            self.segment_buffer = self.segment_buffer[self.chunk_size:]

            if np.any(np.abs(segment) > self.threshold):
                if not self.recording:
                    self.recording = True
                    self.current_message = []
                self.current_message.append(segment)
            else:
                if self.recording:
                    full_message = np.concatenate(self.current_message)
                    filename = os.path.join(self.output_dir, f"msg_{self.msg_count}.dat")
                    self.msg_count += 1
                    with open(filename, "wb", buffering=0) as f:
                        full_message.tofile(f)
                    self.recording = False
                    self.current_message = []

        return len(in0)

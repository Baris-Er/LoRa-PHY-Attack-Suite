# Selective Replay Attack

This folder contains all the source files related to the implementation of the selective replay attack on LoRa physical layer data. It includes GNU Radio flowgraphs and generated Python scripts.

---

![Replay Flowchart](../docs/images/replay.PNG "Replay Flowchart")

## Contents

- **SelectiveReplayAttack.grc**  
  The GNU Radio Companion flowgraph file that implements the selective replay attack. It segments incoming IQ data, applies threshold detection, and enables interactive selection and replay of LoRa messages.

- **Selective_replay_attack_epy_block_0.py**  
  Contains the `segment_threshold_recorder` class. This block processes the incoming IQ stream by:
  - Splitting the data into 0.5-second segments.
  - Considering any segment as part of a message if any sample exceeds a specified (linear) threshold.
  - Finalizing a message and saving it to disk with a dynamic filename (e.g., `msg_0.dat`, `msg_1.dat`, …) when a segment without threshold exceedance is encountered after an ongoing recording.
  - Resetting to begin capturing a new message.

- **Selective_replay_attack_epy_block_1.py**  
  Contains the `gui_file_source` class. This block creates a GUI with a combo box, a refresh button, and a send button that lists message files (msg_*.dat or msg_*.bin) from a specified directory (e.g., "C:\Users\hakan\Documents\lora_recordings"). When a file is selected and the "Send" button is clicked, the block reads the file using `np.fromfile()` and replays it as an IQ stream (`np.complex64`). Once the file is completely replayed, it outputs zero samples and waits for a new selection.

## Notes

- **Threshold Configuration:**  
  The threshold level is critical for determining which segments are recorded as part of a message. Users must adjust this value based on their specific signal environment to avoid missing valid segments (if set too high) or recording excessive noise (if set too low).

- **Output Directory Configuration:**  
  The directory where the messages are saved is configurable. Ensure the specified directory exists and that the application has write permissions.

- **Reusability:**  
  The threshold-based segmentation method used in `segment_threshold_recorder` is versatile and can be adapted for other applications within the project that require selective processing based on signal amplitude.


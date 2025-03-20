# LoRa-PHY-Attack-Suite

**LoRa-PHY-Attack-Suite** is an open-source toolkit for analyzing and exploiting security vulnerabilities in the LoRa physical layer. The project currently implements selective replay functionality using a threshold method and an interactive interface to capture, segment, and replay LoRa messages. Ongoing efforts are now focused on analyzing the LoRa PHY layer to further understand and exploit its security vulnerabilities.

---

## Overview

1. **Codes Folder**  
   - Contains GNU Radio flowgraphs and Python scripts that demonstrate how ESP32 microcontrollers and SDR devices are used in this research.  
   - See the `codes/` folder’s dedicated README for detailed instructions on setup, usage, and file structure.

2. **Documentation**  
   - **`docs/report/Preliminary Report`**  
     - An early-stage (preliminary) report providing background and initial findings. Note that this report is somewhat outdated and does not reflect the most recent progress or planned features.  
   - **`docs/datasheets/`**  
     - Datasheets for the hardware components (e.g., LoRa modules, ESP32 boards) used in this project. Refer to these documents for specifications, operating ranges, and other technical details.

3. **Future Work**  
   - **Message Decryption & Analysis:**  
     Further research into decrypting LoRa payloads to assess vulnerabilities in various encryption schemes.  
   - **Spoofing & MITM Attacks:**  
     Developing capabilities to inject spoofed data and perform Man-in-the-Middle attacks, expanding the scope of security testing.
     
---




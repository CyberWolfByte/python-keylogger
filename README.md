# **Python Keylogger**

A keylogger is a software tool or a hardware device that records keystrokes made by a user on a keyboard, typically without the user's knowledge or consent. The primary function of a keylogger is to capture and log the input from the keyboard as it is typed, which can include sensitive information such as passwords, credit card numbers, personal messages, and other confidential data.

### Use Cases:

- **Security Research and Ethical Hacking:** Security professionals and ethical hackers use keyloggers to test the vulnerability of systems to such surveillance methods. It helps in understanding potential security flaws and strengthening defenses against malicious keylogging.
- **Parental Control and Monitoring:** Parents may use keyloggers to monitor their children's online activities, ensuring they are safe from inappropriate content or interactions.
- **Company Monitoring:** Employers might deploy keyloggers to monitor employee activities on company-owned devices to ensure compliance with company policies and prevent unauthorized disclosure of confidential information.
- **Malicious Activities:** Unethically, keyloggers are used by cybercriminals to steal personal, financial, or business information for fraudulent purposes or identity theft.

## Disclaimer

The tools and scripts provided in this repository are made available for educational purposes only and are intended to be used for testing and protecting systems with the consent of the owners. The author does not take any responsibility for the misuse of these tools. It is the end user's responsibility to obey all applicable local, state, national, and international laws. The developers assume no liability and are not responsible for any misuse or damage caused by this program. Under no circumstances should this tool be used for malicious purposes. The author of this tool advocates for the responsible and ethical use of security tools. Please use this tool responsibly and ethically, ensuring that you have proper authorization before engaging any system with the techniques demonstrated by this project.

## Features

This program uses Python to create a software keylogger with ctypes and the Win32 API to monitor and log keystrokes on a Windows system. It's designed for educational purposes, showcasing how keyloggers can be built and how they operate at a technical level.

## Prerequisites

- **Operating System**: Tested on Windows 10 x64, version  22H2.
- **Python Version**: Python 3.6+

## Installation

1. **Python Environment Setup**: Ensure Python and pip are installed. Install the required libraries using:
    
    ```bash
    pip install ctypes
    ```
    
2. **Download Scripts**: Clone or download the scripts from the project repository to your local machine.

## Usage

- **Run the Script**: Run the Script: Run the script and test by typing characters in an open application such as text editor, word processor, browser, IDE or new command line instance to capture keystrokes.
    
    ```bash
    python3 win_keylogger.py
    ```
    
## How It Works

- **Import Statements:** The script starts by importing necessary modules from ctypes for calling Win32 API functions and defining custom data types.
- **Constants and Custom Types:** Defines various constants used in the Win32 API (e.g., `WH_KEYBOARD_LL`, `WM_KEYDOWN`,`WM_SHIFT`) and custom types like `ULONG_PTR` to ensure compatibility across different system architectures.
- **Structure Definitions:** Structures such as `KBDLLHOOKSTRUCT`, `SECURITY_ATTRIBUTES`, `STARTUPINFO`, and `PROCESS_INFORMATION` are defined to match their Win32 API counterparts. These structures are essential for the correct operation of the API functions used.
- **Win32 API Function Prototypes:** Specifies argument and result types for the Win32 API functions that will be used. This includes functions for setting up a low-level keyboard hook (`SetWindowsHookExA`), processing messages (`GetMessageA`), and others necessary for capturing keystrokes.
- **Keylogger Logic:**
    - The script includes a function to retrieve the name of the foreground window (`get_foreground_window_name`), providing context for the captured keystrokes.
    - The `hook_function` is the core callback that processes keyboard events. It checks for `WM_KEYDOWN` events and uses `ToAscii` to translate virtual key codes into ASCII characters. This function also handles the logging of keystrokes, distinguishing special keys like Return and Shift.
    - A low-level keyboard hook is installed using `SetWindowsHookExA`, specifying `hook_function` as the callback. This allows the keylogger to capture keystrokes regardless of which application is active.
    - The script enters a message loop (`GetMessageA`) to keep the hook active, effectively logging keystrokes until the script is terminated.

## Contributing

If you have an idea for an improvement or if you're interested in collaborating, you are welcome to contribute. Please feel free to open an issue or submit a pull request.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

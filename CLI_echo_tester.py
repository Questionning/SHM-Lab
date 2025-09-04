import usb.core
import usb.util
import threading
import sys


VENDOR_ID = 0xC0DE
PRODUCT_ID = 0xCAFE
INTERFACE_NUMBER = 0
ENDPOINT_OUT = 0x01
ENDPOINT_IN = 0x81

# ---- Device Discovery & Connection Check ----
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    print("Error: USB device not found.")
    sys.exit(1)

try:
    dev.set_configuration()
    cfg = dev.get_active_configuration()
    intf = usb.util.find_descriptor(cfg, bInterfaceNumber=INTERFACE_NUMBER)
    usb.util.claim_interface(dev, INTERFACE_NUMBER)
except usb.core.USBError as e:
    print(f"Error initializing device: {e}")
    sys.exit(1)


def safe_print(msg):
    """Ensures print doesn't interfere with input prompt."""
    sys.stdout.write('\r')              # Return to start of line
    sys.stdout.write(' ' * 80 + '\r')   # Clear the line
    print(msg)
    sys.stdout.write("> ")
    sys.stdout.flush()


def read_from_device():
    while True:
        try:
            data = dev.read(ENDPOINT_IN, 64, timeout=1000)
            message = data.tobytes().decode(errors='replace').strip()
            safe_print(f"[DEVICE]: {message}")
        except usb.core.USBError as e:
            if hasattr(e, 'errno') and e.errno in (110, 10060):
                continue
            elif 'timed out' in str(e).lower():
                continue
            else:
                safe_print(f"[Read Error]: {e}")
                break


threading.Thread(target=read_from_device, daemon=True).start()

# Main input loop
print("Enter commands to send to the RP2040 (Ctrl+C to exit):")
try:
    while True:
        command = input("> ")
        dev.write(ENDPOINT_OUT, command.encode())
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    usb.util.release_interface(dev, INTERFACE_NUMBER)

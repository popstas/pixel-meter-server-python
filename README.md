Server for send signals to [arduino pixel_meter](https://github.com/popstas/arduino-pixel-meter).

Tested on Windows, Ubuntu, MacOS, Asus RT-N56 router.

If you interesting this, use [popstas/pixel-server](https://github.com/popstas/pixel-server) instead.

# Requirements
- python 2.7
- wxPython (for tray icon)
- pubsub
- pyserial

# Install
You need know path to your pixel meter port.

# Usage
For change pixel state use URL like `http://localhost:8035/health?val=100&msg=message&bright=100`

For watch log visit `http://localhost:8035/log`

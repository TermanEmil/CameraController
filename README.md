# Camera controller
A web application to control cameras connected through usb.

## Main features
- Live preview
- Capture image and download
- Change camera settings
- Favourite settings (available in live preview)
- Manage timelapses
- Logs

## Setup
`./setup.sh` - should setup everything.

### In case setup.sh fails
Requirements:
- python3.7 python3.7-dev
- gphoto2
- *[Yepkit/ykush](https://github.com/Yepkit/ykush.git) (if you want to use ykush3 board)

Install the python packages from `./requiremenets.txt`


## How to run
`./run.sh` - it should start the web app at the port 5000.

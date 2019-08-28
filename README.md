# Camera controller
A web application to control cameras connected through usb.

For supported cameras, please visit [this](http://www.gphoto.org/proj/libgphoto2/support.php) link.

*Was tested on Ubuntu 18.04*

## Main features
- Live preview
- Capture image and download (chrome only for now)
- Change camera settings
- Favourite settings (available in live preview)
- Manage timelapses
- Logs

## Setup
`$ source ./setup.sh` - should setup everything.

`source` - to directly source into the python virtualenv.

Otherwise, it's possible to run `$ source .venv/bin/activate` after `./setup.sh`

### In case setup.sh fails
Requirements:
- python3.7 python3.7-dev
- gphoto2
- *[Yepkit/ykush](https://github.com/Yepkit/ykush.git) (if you want to use ykush3 board)

Install the python packages from `./requiremenets.txt`

## How to run
`$ ./run.sh` - it should start the web app at the port 5000.


## Timelapse file transfer
1. Mount the nfs server
2. Watch for any changes in `./Timelapses` and transfer all any files inside to the nfs server

#### Requirements
- nfs-common
- inotify-tools


- **Setup**: `./scripts/setup_timelapse_file_transfer.sh`
- **Run**: `./scripts/run_timelapse_file_transfer.sh`

By default, it will wait for any changes in `./Timelapses` and move the files to `/Mounted/Cern/Timelapse/Software/Timelapses`.

The file transfer will work even if the nfs server was not mounted. It will simply move the files to a different directory.


## Max

#### Web app
Run the web app as sudo in background:
~~~bash
sudo bash -c 'source .venv/bin/activate && ./run.sh 2>&1 1>> out.log &'
~~~

You will need `sudo` for ykush thing.

The output will be written in out.log.


#### NFS file transfer

Mount the nfs server. It will mount the nfs server to `/Mounted/Cern/`
~~~bash
sudo ./scripts/mount_nfs.sh
~~~

To make sure it has been successfully mounted, run a quick check:
~~~bash
ls /Mounted/Cern/
~~~
You should see a list with all the files/directories in the nfs server

To continuously transfer the files, run:
~~~bash
sudo ./scripts/run_timelapse_file_transfer.sh 2>&1 1>> sync.log
~~~

The output will be written in sync.log.

# Screenshots
**Index:**
![](./imgs/index.png)

**Camera settings:**
![](./imgs/all_settings.png)

**Live preview:**
![](./imgs/single_preview.png)

**Multipreview:**
![](./imgs/multipreview.png)

**Schedule:**
![](./imgs/schedule.png)

**Timelapse:**
![](./imgs/timelapse.png)

**Settings:**
![](./imgs/general_settings.png)

**Favourite fields settings:**
![](./imgs/fav_fields_settings.png)

**Logs:**
![](./imgs/logs.png)

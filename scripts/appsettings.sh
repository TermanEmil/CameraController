PORT=5000

#MOUNT_REMOTE_NODE - Required secret (host:dir)
MOUNT_POINT='/mnt/eco_its_cern_nfs'

TIMELAPSE_DIR='./Timelapses'
TIMELAPSE_DEST='Timelapse/Software/Timelapses'

# For local settings
LOCAL_SETTINGS="./scripts/appsettings.local.sh"
if test -f "$LOCAL_SETTINGS"; then
    . "$LOCAL_SETTINGS";
fi

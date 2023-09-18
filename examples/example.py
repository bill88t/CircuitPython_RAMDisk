import storage
from ramdisk import RAMDisk

# Create the vfs object
vfs = storage.VfsFat(RAMDisk(64))

"""
It's a 128kb drive, as default block size is 2048.
disk size = blocks (64) * block size (2048)

To override the block size:
`vfs = storage.VfsFat(RAMDisk(64), 1024)`
"""

# Mount it to /ramdisk
storage.mount(vfs, "/ramdisk")

# Example write
with open("/ramdisk/test.txt", "w") as f:
    f.write("Hello world!")

# Files are stored across remounts
storage.umount("/ramdisk")
storage.mount(vfs, "/ramdisk")

# Read back the previously stored file
with open("/ramdisk/test.txt") as f:
    print(f.read())

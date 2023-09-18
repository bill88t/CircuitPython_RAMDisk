from storage import VfsFat

class RAMDisk:
    def __init__(self: RAMDisk, blocks: int, block_size: int = 2048) -> None:
        if block_size < 512:
            raise ValueError(
                "Block size must be at least 512."
            )
        if blocks < 64:
            raise ValueError(
                "Cannot be less than 64 blocks."
            )
        self._block_size = block_size
        self._blocks = blocks
        self._deinited = False
        self._array = bytearray(block_size * blocks)
        VfsFat.mkfs(self)

    @property
    def blocks(self: RAMDisk):
        self._deinit_check()
        return self._blocks

    @property
    def block_size(self: RAMDisk):
        self._deinit_check()
        return self._block_size

    def readblocks(self: RAMDisk, block_num: int, buf: bytearray) -> None:
        self._deinit_check()
        mvd = memoryview(self._array)
        for i in range(len(buf)):
            buf[i] = mvd[block_num * self._block_size + i]

    def writeblocks(self: RAMDisk, block_num: int, buf: bytearray) -> None:
        self._deinit_check()
        for i in range(len(buf)):
            self._array[block_num * self._block_size + i] = buf[i]
        # Inexplicably slower.
        #area = block_num*self._block_size
        #self._array[area:area+len(buf)] = buf

    def ioctl(self: RAMDisk, op: int, arg: int) -> int:
        self._deinit_check()
        if op == 4: # get block num
            return self._blocks
        if op == 5: # get block size
            return self._block_size

    def _deinit_check(self: RAMDisk) -> None:
        if self._deinited:
            raise ValueError(
                "Object has been deinitialized and can no longer be used. Create a new object."
            )

    def deinit(self: RAMDisk) -> None:
        self._deinit_check()
        del (
            self._block_size,
            self._blocks,
            self._array,
        )
        self._deinited = True

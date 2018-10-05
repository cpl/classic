
import pprint


HEAP_START = 0x000FFFF0

FREE = [None for _ in range(0xFF)]
ORIG = None


# align 8
class mem_allocation():
    def __init__(self, size, addr, nmal):
        self.size = size # u32
        self.nmal = nmal # u32
        self.addr = addr # u32

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[ %6s | %8s ] -> %s" % (hex(self.size), hex(self.addr), self.nmal)


def free(addr):
    global ORIG
    global FREE

    current = ORIG
    while current.nmal != None:
        if current.addr == addr:
            current.addr += 1
        current = current.nmal


def malloc(size):
    global ORIG
    global FREE

    addr = 0x0
    size += (4 - (size & 3)) & 3

    FREE[0].size = size
    FREE[0].nmal = mem_allocation(0, FREE[0].addr - size, None)
    FREE[0].addr -= 1
    addr = FREE[0].addr
    FREE[0] = FREE[0].nmal

    return addr



if __name__ == "__main__":
    ORIG = mem_allocation(0, HEAP_START + 1, None)
    FREE[0] = ORIG

    malloc(0x50)
    malloc(0x20)
    p = malloc(0x40)
    malloc(0x60)

    free(p)

    print(ORIG)
    print(FREE[0])

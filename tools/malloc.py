
import pprint


class mem_allocation():
    def __init__(self, size, addr, nmal):
        self.size = size
        self.addr = addr
        self.nmal = nmal

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[ %6s | %8s ]\n -> %s" % (hex(self.size), hex(self.addr), self.nmal)


HEAP_END   = 0x000F0000
HEAP_START = 0x000FFFF0

FD_MALLOC = mem_allocation(0, HEAP_START, None)
FF_MALLOC = FD_MALLOC.nmal


def free(ptr):
    global FF_MALLOC
    global FD_MALLOC

    current = FD_MALLOC
    while hex(current.addr) != ptr:
        if current.nmal is None:
            print("free(" + ptr + ") SEGFAULT")
            return
        current = current.nmal
    current.addr += 1
    FF_MALLOC = current



def malloc(size):
    global FF_MALLOC
    global FD_MALLOC

    size+=(8 - (size & 7)) & 7
    addr = 0

    if FF_MALLOC is None:
        FD_MALLOC.nmal = mem_allocation(0, FD_MALLOC.addr - size, None)
        FF_MALLOC = FD_MALLOC.nmal

        FD_MALLOC.size = size
        addr = FD_MALLOC.addr
    else:
        if FF_MALLOC.size == 0:
            FF_MALLOC.nmal = mem_allocation(0, FF_MALLOC.addr - size, None)
            FF_MALLOC.size = size
            addr = FF_MALLOC.addr
            FF_MALLOC = FF_MALLOC.nmal
        elif FF_MALLOC.size == size:
            FF_MALLOC.addr -= 1
        elif FF_MALLOC.size > size:
            FF_MALLOC.nmal = mem_allocation(FF_MALLOC.size - size, FF_MALLOC.addr - size, FF_MALLOC.nmal)
            FF_MALLOC.size = size
            FF_MALLOC.addr -= 1
            addr = FF_MALLOC.addr
            FF_MALLOC = FF_MALLOC.nmal
        else:
            current = FF_MALLOC
            while current.nmal != None:
                current = current.nmal
            current.size = size
            current.nmal = mem_allocation(0, current.addr - size, None)
            addr = current.addr
    return hex(addr)


if __name__ == "__main__":

    malloc(0x29)
    p = malloc(0x1A)
    malloc(0x90)

    free(p)

    malloc(0x30)
    malloc(0x5)
    malloc(0x400)

    pprint.pprint(FD_MALLOC)
    print("")
    pprint.pprint(FF_MALLOC)

import simuvex

######################################
# recv
######################################

class recv(simuvex.SimProcedure):
    def __init__(self): # pylint: disable=W0231
        # TODO: Symbolic fd
        fd = self.arg(0)
        dst = self.arg(1)
        length = self.arg(2)
        plugin = self.state['posix']

        old_pos = plugin.pos(fd)

        data = plugin.read(fd, self.state.se.any_int(length))
        self.add_refs(simuvex.SimFileRead(self.addr, self.stmt_from, fd, old_pos, data, length))
        self.state.store_mem(dst, data)
        self.add_refs(simuvex.SimMemWrite(self.addr, self.stmt_from, dst, data, length))
        self.ret(length)

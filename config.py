APTLOG = [
    "read",
    "readv",
    "write",
    "writev",
    "fcntl",
    "rmdir",
    "rename",
    "chmod",
    "execve",
    "clone",
    "pipe",
    "fork",
    "accept",
    "sendmsg",
    "recvmsg",
    "recvfrom",
    "send",
    "sendto",
]

class APTLOG_TYPE:
    FILE_OP = ["read", "readv", "write", "writev", "fcntl", "rmdir", "rename", "chmod"]
    PROCESS_OP = ["clone", "pipe", "fork",'execve']
    NET_OP = ["sendmsg", "recvmsg", "recvfrom", "send", "sendto"]


class APTLOG_ARTRIBUTE:
    FILE_ARTRIBUTE = ['proc.cmdline', 'fd.name', 'is_warn', 'evt.time', 'evt.type', 'proc.name', 'tech_num', 'anomaly_socre']
    PROCESS_ARTRIBUTE = ['proc.ppcmdline', 'proc.cmdline', 'is_warn', 'evt.time', 'evt.type', 'proc.name', 'tech_num', 'anomaly_socre']
    NET_ARTRIBUTE = ['proc.cmdline', 'fd.name', 'is_warn', 'evt.time', 'evt.type', 'proc.name', 'tech_num', 'anomaly_socre']
    # EXECVE_ARTRIBUTE = ['proc.cmdline', 'evt.args', 'is_warn']


class APTLOG_KEY:
    FILE = "FILE"
    PROCESS = "PROCESS"
    NET = "NET"
    # EXECVE = "EXECVE"

class APTLOG_NODE_TYPE:
    PROCESS = 0
    FILE = 1
    NET = 2

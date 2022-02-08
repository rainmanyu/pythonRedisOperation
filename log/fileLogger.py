f = open("log.txt", "a")


def write(log):
    f.write(log)
    f.flush()

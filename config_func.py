import os

def config_func(prj, model, run):
    cfg = {}
    rootDir = "/home/utsumi/mnt/well.share/WS"
    baseDir = os.path.join(rootDir, prj, model, run)

    cfg["rootDir"] = rootDir
    cfg["baseDir"] = baseDir

    return cfg
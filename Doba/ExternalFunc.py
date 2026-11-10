from . import source
from . import Core

def ExitLib():
    source.Exit = True
    print("REQUEST: STOPLIB")

def GetNowTime():
    return Core.OldTime if Core.OldTime else None
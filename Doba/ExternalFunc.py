import threading

from . import source
from . import Core

def ExitLib():
    source.Exit = True
    print("REQUEST: STOPLIB")

def GetNowTime():
    return Core.OldTime if Core.OldTime else None

def WaitTime(sec, func=None):
    HOURS, MINUTES, SECONDS = map(int, Core.OldTime.split(":"))

    SECONDS += sec

    if SECONDS >= 60:
        SECONDS -= 60
        MINUTES += 1
    if MINUTES >= 60:
        MINUTES -= 60
        HOURS += 1
    if HOURS >= 24:
        HOURS -= 24

    NewTime = str(HOURS) + ":" + str(MINUTES) + ":" + str(SECONDS)

    while Core.OldTime != NewTime:
        pass

    if func is not None:
        func()
    return 0
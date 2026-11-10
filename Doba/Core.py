from concurrent.futures import ThreadPoolExecutor
import aiohttp
import asyncio
import threading
from bs4 import BeautifulSoup

from . import source
from . import InternalFunc
from . import ExternalFunc

OldTime = ""
Started = threading.Event()

async def Check(session):
    global OldTime
    url = "https://time100.ru/"

    async with session.get(url) as response:
        response.raise_for_status()
        html = await response.text()

    soup = BeautifulSoup(html, "html.parser")

    moscow_time = soup.select_one('.display-time .time')

    if OldTime != moscow_time.text:
        if source.DeBug == True:
            print(moscow_time.text)
        OldTime = moscow_time.text

async def CheckLOOP():
    print("MAINLOOP: RUN")

    resolver = aiohttp.AsyncResolver()
    connector = aiohttp.TCPConnector(resolver=resolver)

    async with aiohttp.ClientSession(connector=connector) as session:
        await Check(session)

        Started.set()

        while not source.Exit:
            await asyncio.sleep(0.5)
            if not source.Exit:
                await Check(session)

    print("MAINLOOP: STOP")

async def Start():
    await CheckLOOP()

def InitLib():
    print("REQUEST: RUNLIB")

    def Run():
        asyncio.run(Start())

    thread = threading.Thread(target=Run, daemon=False)
    thread.start()

    Started.wait()
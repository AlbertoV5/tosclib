from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path
import asyncio
import aiohttp
import time


def hashSha1(actionPath: Path):
    """Reaper current hashing as of 6.57. Ask Justin.
    https://askjf.com/index.php?q=6075s"""
    fix = str(actionPath).upper().replace("\\", "/")
    return f"_RS{sha1(fix.encode()).hexdigest()}"


@dataclass
class REAPER:
    """Reaper config values. Change them to fit your setup."""

    lisztPath: Path = Path("AlbertoV5-ReaperTools") / "liszt"
    host: str = "127.0.0.1"
    port: str = "8080"


@dataclass
class Actions:
    pull: str = hashSha1(REAPER.lisztPath / "liszt-pull.py")
    generate: str = hashSha1(REAPER.lisztPath / "liszt-generate.py")
    openProjPath: str = (
        "_S&M_OPEN_PRJ_PATH"  #: Optional, in case you have SWS Extensions
    )


async def pingReaper(*args):
    """Ask Reaper to execute commands by name or hash"""
    async with aiohttp.ClientSession() as session:
        for arg in args:
            async with session.get(
                f"http://{REAPER.host}:{REAPER.port}/_/{arg}"
            ) as resp:
                _ = await resp.text(encoding="UTF-8")


def main():

    asyncio.run(pingReaper(Actions.pull, Actions.generate, Actions.openProjPath))


if __name__ == "__main__":

    start = time.process_time()
    main()
    end = time.process_time()
    print("Hey Reaper!", end - start)

from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path
import asyncio
import aiohttp
import time


def hashSha1(actionPath: Path):
    """Reaper current hashing as of 6.57. Ask Justin."""
    trim = str(actionPath).upper().replace("\\", "/")
    return f"_RS{sha1(trim.encode()).hexdigest()}"


@dataclass
class REAPER:
    """Reaper config values. Change them to fit your setup."""

    lisztPath: Path = Path("AlbertoV5-ReaperTools") / "liszt"
    host: str = "127.0.0.1"
    port: str = "8080"


@dataclass
class Actions:
    """List of actions you wanna call"""

    pull: str = hashSha1(REAPER.lisztPath / "liszt-pull.py")
    generate: str = hashSha1(REAPER.lisztPath / "liszt-generate.py")
    openProjPath: str = "_S&M_OPEN_PRJ_PATH"


async def pingReaper(*args):
    """Ask Reaper to execute commands by name or hash"""
    async with aiohttp.ClientSession() as session:
        for arg in args:
            async with session.get(
                f"http://{REAPER.host}:{REAPER.port}/_/{arg}"
            ) as resp:
                _ = await resp.text(encoding="UTF-8")


def main():

    start = time.time()
    asyncio.run(pingReaper(Actions.pull, Actions.generate, Actions.openProjPath))
    print("Hey Reaper!", time.time() - start)


if __name__ == "__main__":
    main()

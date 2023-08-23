from os import path

from yt_dlp import YoutubeDL

from Nistha.config import DURATION_LIMIT
from Nistha.Modules.helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)
    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"🛑 𝑉𝐼𝐷𝐸𝑂𝑆 𝐿𝑂𝑁𝐺𝐸𝑅 𝑇𝐻𝐴𝑁 {DURATION_LIMIT} 𝑀𝐼𝑁𝑈𝑇𝐸(s) 𝐴𝑅𝐸'𝑇 𝐴𝐿𝐿𝑂𝑊 𝑇𝐻𝐸 𝑃𝑅𝑂𝑉𝐼𝐷𝐸𝐷 𝐼𝑆 {duration} 𝑀𝐼𝑁𝑈𝑇𝐸(s)",
        )
    try:
        ydl.download([url])
    except:
        raise DurationLimitError(
            f"🛑 𝑉𝐼𝐷𝐸𝑂𝑆 𝐿𝑂𝑁𝐺𝐸𝑅 𝑇𝐻𝐴𝑁 {DURATION_LIMIT} 𝑀𝐼𝑁𝑈𝑇𝐸(s) 𝐴𝑅𝐸'𝑇 𝐴𝐿𝐿𝑂𝑊 𝑇𝐻𝐸 𝑃𝑅𝑂𝑉𝐼𝐷𝐸𝐷 𝐼𝑆 {duration} 𝑀𝐼𝑁𝑈𝑇𝐸(s)",
        )
    return path.join("downloads", f"{info['id']}.{info['ext']}")

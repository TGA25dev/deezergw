from typing import Dict, Literal, TypedDict

QualityType = Literal["MP3_320", "MP3_128", "FLAC"]
FormatType = Literal["mp3", "flac"]


class QualityEntry(TypedDict):
    n_quality: str
    f_format: FormatType
    s_quality: str


Qualities: Dict[QualityType, QualityEntry] = {
    "MP3_128": {"n_quality": "1", "f_format": "mp3", "s_quality": "128"},
    "MP3_320": {"n_quality": "3", "f_format": "mp3", "s_quality": "320"},
    "FLAC": {"n_quality": "9", "f_format": "flac", "s_quality": "FLAC"},
}


StockQuality: QualityType = "MP3_320"

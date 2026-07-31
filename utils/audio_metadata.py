import os

from mutagen.mp3 import MP3


class AudioMetadata:

    @staticmethod
    def get_metadata(audio_path):

        try:

            audio = MP3(audio_path)

            return {

                "filename": os.path.basename(audio_path),

                "duration": round(audio.info.length, 2),

                "bitrate": int(audio.info.bitrate / 1000),

                "sample_rate": audio.info.sample_rate,

                "channels": audio.info.channels,

                "size_mb": round(
                    os.path.getsize(audio_path) /
                    (1024 * 1024),
                    2
                )

            }

        except Exception:

            return None
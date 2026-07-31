import os
import math
import uuid

from pydub import AudioSegment


class AudioSplitter:

    TEMP_FOLDER = "audio_chunks"

    @classmethod
    def split_audio(
        cls,
        audio_path,
        chunk_minutes=5
    ):

        os.makedirs(
            cls.TEMP_FOLDER,
            exist_ok=True
        )

        print("=" * 60)
        print("Audio Splitter Started")
        print("Audio File :", audio_path)

        audio = AudioSegment.from_file(audio_path)

        print("Audio Length (ms):", len(audio))
        print("Chunk Minutes:", chunk_minutes)

        chunk_length = chunk_minutes * 60 * 1000

        total_chunks = math.ceil(
            len(audio) / chunk_length
        )

        print("Total Chunks:", total_chunks)

        chunk_paths = []

        for i in range(total_chunks):

            start = i * chunk_length

            end = min(
                (i + 1) * chunk_length,
                len(audio)
            )

            chunk = audio[start:end]

            filename = (
                f"chunk_{i+1}_"
                f"{uuid.uuid4().hex[:8]}.wav"
            )

            chunk_path = os.path.join(
                cls.TEMP_FOLDER,
                filename
            )

            print(
                f"Creating Chunk {i+1}/{total_chunks}"
            )

            chunk.export(
                chunk_path,
                format="wav"
            )

            chunk_paths.append(
                chunk_path
            )

        print("Splitting Completed")
        print("=" * 60)

        return chunk_paths

    @classmethod
    def cleanup(
        cls,
        chunk_paths
    ):

        print("Cleaning Temporary Chunks...")

        for path in chunk_paths:

            try:

                if os.path.exists(path):

                    os.remove(path)

            except Exception as e:

                print(e)

        print("Cleanup Finished")
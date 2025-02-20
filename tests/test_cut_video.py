import os
import sys
import unittest

# Asegúrate de que el directorio del módulo esté en el sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sliceffmpeg.cut_video import generate_ffmpeg_command, parse_time


class TestCutVideo(unittest.TestCase):
    def test_parse_time(self):
        self.assertEqual(parse_time("00:00:00"), 0)
        self.assertEqual(parse_time("00:00:54"), 54)
        self.assertEqual(parse_time("00:04:30"), 270)
        self.assertEqual(parse_time("00:30:15"), 1815)
        self.assertEqual(parse_time("01:05:10"), 3910)

    def test_generate_ffmpeg_command(self):
        input_video = "input_video.mp4"
        time_init = 0
        time_final = 54
        output_video = "input_video-001.mp4"
        expected_command = [
            "ffmpeg",
            "-i",
            input_video,
            "-map",
            "0",
            "-c",
            "copy",
            "-ss",
            str(time_init),
            "-t",
            str(time_final - time_init),
            "-map_metadata",
            "0",
            output_video,
        ]
        self.assertEqual(
            generate_ffmpeg_command(input_video, time_init, time_final, output_video),
            expected_command,
        )


if __name__ == "__main__":
    unittest.main()

from aspose_compressor import AsposeCompressor

ac = AsposeCompressor()
file = ac.compress_video("D:\\Ventures\\Projects\\VAS\\VASweek2.mp4")
file.save("D:\\Ventures\\Projects\\VAS\\VASweek2Comp.mp4")
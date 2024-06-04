from moviepy.editor import VideoFileClip

def convert_video(input_file, output_file):
    clip = VideoFileClip(input_file)
    clip.write_videofile(output_file, codec='libx264')

# 使用方法
convert_video("演示视频2k60.mkv", "演示视频2k60.mp4")
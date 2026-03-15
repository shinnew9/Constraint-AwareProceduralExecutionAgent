from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def combine_videos():
    video_folder = "./output_videos"
    clips = []
    
    # Bring numbers in ascending order
    video_files = sorted([f for f in os.listdir(video_folder) if f.endswith('.mp4')])
    
    for filename in video_files:
        path = os.path.join(video_folder, filename)
        clips.append(VideoFileClip(path))
    
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile("final_cooking_simulation.mp4", fps=24)

if __name__ == "__main__":
    combine_videos()
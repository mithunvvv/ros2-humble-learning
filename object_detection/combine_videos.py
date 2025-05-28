#!/usr/bin/env python3

from moviepy import VideoFileClip, clips_array

if __name__ == '__main__':

    # Load video clips
    top_clip = VideoFileClip("/home/user/ros2-humble-learning/object_detection/detections_NIR.mp4")
    bottom_clip = VideoFileClip("/home/user/ros2-humble-learning/object_detection/detections_reflec.mp4")

    # Resize clips to the same width (recommended)
    min_width = min(top_clip.w, bottom_clip.w)
    top_resized = top_clip.resized(width=min_width)
    bottom_resized = bottom_clip.resized(width=min_width)

    # Stack the videos vertically
    final_clip = clips_array([[top_resized], [bottom_resized]])

    # Set duration to the shortest clip
    final_clip = final_clip.with_duration(min(top_clip.duration, bottom_clip.duration))

    # Export the final video
    final_clip.write_videofile("top_bottom_output.mp4", codec="libx264", audio_codec="aac")

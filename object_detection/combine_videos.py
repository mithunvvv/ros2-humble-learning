#!/usr/bin/env python3

from moviepy import VideoFileClip, clips_array, TextClip, CompositeVideoClip

if __name__ == '__main__':

    # Load video clips
    top_clip = VideoFileClip("/home/user/ros2-humble-learning/object_detection/detections_nearir_slow_sunny.mp4")
    middle_clip = VideoFileClip("/home/user/ros2-humble-learning/object_detection/detections_signal_slow_sunny.mp4")
    bottom_clip = VideoFileClip("/home/user/ros2-humble-learning/object_detection/detections_reflec_slow_sunny.mp4")

    # Resize clips to the same width (recommended)
    min_width = min(top_clip.w, bottom_clip.w)
    top_resized = top_clip.resized(width=min_width)
    middle_resized = middle_clip.resized(width=min_width)
    bottom_resized = bottom_clip.resized(width=min_width)

    # Create subtitles
    top_text = TextClip(text="NIR", font_size=40, color='white', bg_color='black').with_duration(top_resized.duration).with_position(("center", "top"))
    middle_text = TextClip(text="Signal", font_size=40, color='white', bg_color='black').with_duration(top_resized.duration).with_position(("center", "top"))
    bottom_text = TextClip(text="Reflec", font_size=40, color='white', bg_color='black').with_duration(bottom_resized.duration).with_position(("center", "top"))

    # Overlay text on each video
    top_labeled = CompositeVideoClip([top_resized, top_text])
    bottom_labeled = CompositeVideoClip([bottom_resized, bottom_text])
    middle_labeled = CompositeVideoClip([middle_resized, middle_text])

    # Stack vertically
    # final_clip = clips_array([[top_labeled], [bottom_labeled]])
    final_clip = clips_array([[top_labeled], [middle_labeled], [bottom_labeled]])

    # Set duration to the shortest clip
    final_clip = final_clip.with_duration(min(top_clip.duration, bottom_clip.duration))

    # Export the final video
    final_clip.write_videofile("large_model_sunny.mp4", codec="libx264", audio_codec="aac")

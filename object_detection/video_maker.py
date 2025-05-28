import os
import torch
from mmengine.runner import Runner
from mmengine.config import Config
from mmdet.apis import init_detector, inference_detector
from mmcv.visualization import imshow_det_bboxes


import argparse
import os
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
from cv_bridge import CvBridge
from mmengine.config import Config
from mmengine.runner import Runner  # noqa: F401  #  keeps your original import
from mmdet.apis import init_detector, inference_detector


import rosbag2_py
from rclpy.serialization import deserialize_message
from sensor_msgs.msg import Image as ImageMsg

# -----------------------------------------------------------------------------


def open_bag(bag_uri: str) -> rosbag2_py.SequentialReader:
    storage_options = rosbag2_py.StorageOptions(uri=bag_uri, storage_id="sqlite3")
    converter_options = rosbag2_py.ConverterOptions("", "")
    reader = rosbag2_py.SequentialReader()
    reader.open(storage_options, converter_options)
    return reader


def write_video_writer(path: Path, fps: float, wh: Tuple[int, int]) -> cv2.VideoWriter:
    fourcc = cv2.VideoWriter_fourcc(*"MP4V")  # H.264
    writer = cv2.VideoWriter(str(path), fourcc, fps, wh)
    if not writer.isOpened():
        raise RuntimeError(f"Could not open video file {path} for writing")
    return writer


# -----------------------------------------------------------------------------


def main(args):
    bag_uri = Path(args.bag).expanduser().resolve().as_posix()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---------------- MMDetection model --------------------------------------
    model = init_detector(args.config, args.checkpoint, device=args.device)

    # ---------------- Rosbag reader -----------------------------------------
    reader = open_bag(bag_uri)

    # Map the topic name to its ID so we can cheaply skip irrelevant topics
    bridge = CvBridge()
    png_template = out_dir / "frame_{:06d}.png"

    video_writer = None
    frame_idx = 0
    print("Processing bag …")

    while reader.has_next():
        topic_name, data, t = reader.read_next()

        if topic_name != "/ouster/reflec_image":
            continue

        # Deserialize and convert to cv2 image
        img_msg = deserialize_message(data, ImageMsg)
        cv_img = bridge.imgmsg_to_cv2(img_msg, 'bgr8')[:,:,0]
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)

        # Inference & visualization
        print(cv_img.shape)
        # raise NotImplementedError
        # breakpoint()
        result = inference_detector(model, cv_img)


        # vis_frame = model.show_result(
        #     cv_img,
        #     result,
        #     score_thr=0.3,
        #     draw_bbox=True,
        #     draw_mask=False,
        #     out_file=None,
        #     show=False,
        # )

        # print(result)
        # breakpoint()
        scores = result.pred_instances.scores
        bboxes= result.pred_instances.bboxes

        bboxes_with_scores = torch.cat((bboxes, scores[:, None]), dim=-1).cpu().numpy()

        vis_frame = imshow_det_bboxes(
            cv_img,
            bboxes_with_scores,  # result is usually a tuple like (bboxes, labels)
            score_thr=0.3,
            labels = result.pred_instances.labels,
            show=False,
            out_file=None,
        )

        # Initialise video writer once we know resolution
        if video_writer is None:
            height, width = vis_frame.shape[:2]
            video_writer = write_video_writer(Path(args.video), fps=10.0, wh=(width, height))

        # Save PNG and append to video
        png_path = png_template.as_posix().format(frame_idx)
        cv2.imwrite(png_path, vis_frame)
        video_writer.write(vis_frame)

        frame_idx += 1
        if frame_idx % 100 == 0:
            print(f"  {frame_idx} frames processed")

        if frame_idx == 1000:
            break
    # --------------- Cleanup -------------------------------------------------
    if video_writer:
        video_writer.release()
    print(f"Finished! {frame_idx} frames ⇒ {out_dir} and {args.video}")


# -----------------------------------------------------------------------------


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bag", default="/home/user/rosbag2_2025_05_20-12_00_56")
    parser.add_argument("--config", default="/home/user/mmdetection/configs/yolox/yolox_s_8xb8-300e_coco.py")
    parser.add_argument("--checkpoint", default="https://download.openmmlab.com/mmdetection/v2.0/yolox/yolox_s_8x8_300e_coco/yolox_s_8x8_300e_coco_20211121_095711-4592a793.pth")
    parser.add_argument("--device", default="cuda:0", help='e.g. "cuda:0" or "cpu"')
    parser.add_argument("--out_dir", default="./detections", help="Folder for PNG frames")
    parser.add_argument("--video", default="detections_NIR.mp4", help="Output video path")
    main(parser.parse_args())

    # /home/user/mmdetection/configs/yolox/yolox_s_8xb8-300e_coco.py
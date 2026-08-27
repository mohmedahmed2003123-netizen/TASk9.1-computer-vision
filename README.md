# 🚗 Task 9.1 - Eyes on the Road, Depth in the Code

**Stereo Vision & 3D Point Cloud Reconstruction**  
*Electrical Team Training 26/27 – Individual Task*

---

## 📌 Overview
This project implements a basic stereo vision pipeline using Python and OpenCV.  
Given a pair of pre-rectified left and right images (`im0.png`, `im1.png`), the script:
1. Computes a **disparity map** using `cv2.StereoBM`.
2. Estimates **real-world depth** at a specific pixel.
3. (Bonus) Generates a **3D point cloud** and saves it as a `.ply` file.

---

## 🧰 Requirements
- Python 3.12+
- OpenCV (`opencv-python`)
- NumPy
- Open3D (for viewing the point cloud)

Install dependencies:
bash
pip install opencv-python numpy open3d

---

---

 How to Run

1. Activate Virtual Environment

bash
cd ~/Task9_Environment
source task9_env/bin/activate

2. Generate Disparity Map & Point Cloud

bash
cd src
python3 stereo_task.py

This will produce:

· disparity_grayscale.png
· disparity_heatmap.png
· pointcloud.ply (raw, uncompressed) – if you have enough disk space

3. View the 3D Point Cloud

Note: The uploaded pointcloud.ply is compressed to pointcloud.ply.gz to bypass GitHub's file size limits.

To decompress it:

bash
cd ../outputs
gunzip pointcloud.ply.gz   # Creates pointcloud.ply

Then view it:

bash
cd ../src
python3 view_pointcloud.py

· Use Left-click + drag to rotate.
· Use Right-click + drag to pan.
· Use Scroll wheel to zoom.

---

Results

· Depth at center pixel (1482, 1000): 3.915 meters
· Disparity Map: Saved as grayscale and heatmap.
· Point Cloud: Contains 856,971 points.

---

video link:
https://drive.google.com/file/d/1FwZTtLV9Qbb83Rv51t5tcp7M3SPrMPLP/view?usp=drivesdk

---

📦 Notes on Compressed File

The original pointcloud.ply is ~XX MB (too large for GitHub's 100 MB limit).
It has been compressed using gzip to pointcloud.ply.gz.
To regenerate the uncompressed file, either:

· Run stereo_task.py again (it will create a fresh pointcloud.ply).
· Or decompress the provided .gz file using gunzip.

---

🛠️ Challenges Faced

· Large image size (2964×2000): Required careful tuning of numDisparities and blockSize.
· Hardware limitations: Older GPU (Intel HD 3000) caused issues with OpenGL; solved by using LIBGL_ALWAYS_SOFTWARE=1 or switching to Xorg session.
· GitHub size limits: Resolved by compressing the .ply file and providing clear instructions.

---

Author

Mohmed Ahmed 


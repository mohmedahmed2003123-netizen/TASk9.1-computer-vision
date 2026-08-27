import cv2
import numpy as np
import os
import re

def read_calibration(calib_path):
    with open(calib_path, 'r') as f:
        data = f.read()

    match_cam0 = re.search(r'cam0\s*=\s*\[([\d.\-eE\s]+)\]', data)
    if not match_cam0:
        raise ValueError("i don't find cam0 ")
    
    vals = list(map(float, match_cam0.group(1).split()))

    fx = vals[0]   
    cx = vals[2]  
    fy = vals[4]   
    cy = vals[5]   

    # ecstract the baselin and transefer to mlie meter
    match_base = re.search(r'baseline\s*=\s*([\d.]+)', data)
    if not match_base:
        raise ValueError("baseline not ex")
    baseline_mm = float(match_base.group(1))
    baseline = baseline_mm / 1000.0  # تحويل إلى متر

    # photo dimention 
    match_w = re.search(r'width\s*=\s*(\d+)', data)
    match_h = re.search(r'height\s*=\s*(\d+)', data)
    if match_w and match_h:
        w = int(match_w.group(1))
        h = int(match_h.group(1))
        print(f" photo dimention: {w} x {h}")
    else:
        w, h = None, None

    print(f": fx={fx:.2f}, fy={fy:.2f}, cx={cx:.2f}, cy={cy:.2f}, baseline={baseline:.4f} meter")
    return fx, fy, cx, cy, baseline, w, h


base_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(base_dir, '..', 'dataset')
output_dir = os.path.join(base_dir, '..', 'outputs')
os.makedirs(output_dir, exist_ok=True)

left_path = os.path.join(dataset_dir, 'im0.png')
right_path = os.path.join(dataset_dir, 'im1.png')
calib_path = os.path.join(dataset_dir, 'calib.txt')

#read the calibrtion
if not os.path.exists(calib_path):
    print(f"not ex: {calib_path}")
    exit(1)

fx, fy, cx, cy, baseline, calib_w, calib_h = read_calibration(calib_path)

#upload photo in gray 
left_img = cv2.imread(left_path, cv2.IMREAD_GRAYSCALE)
right_img = cv2.imread(right_path, cv2.IMREAD_GRAYSCALE)

if left_img is None or right_img is None:
    print("the photos not ex in dataset")
    exit(1)

h, w = left_img.shape
print(f"photo dimention uploaded secsfully: {w} x {h}")


numDisparities = 288   
blockSize = 21        

stereo = cv2.StereoBM_create(numDisparities=numDisparities, blockSize=blockSize)
disparity_raw = stereo.compute(left_img, right_img).astype(np.float32)
disparity = disparity_raw / 16.0   # real value


disparity_norm = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
disparity_norm = np.uint8(disparity_norm)
cv2.imwrite(os.path.join(output_dir, 'disparity_grayscale.png'), disparity_norm)
disparity_heatmap = cv2.applyColorMap(disparity_norm, cv2.COLORMAP_JET)
cv2.imwrite(os.path.join(output_dir, 'disparity_heatmap.png'), disparity_heatmap)
print("done")

px, py = w // 2, h // 2
d_val = disparity[py, px]
if d_val > 0:
    depth = (fx * baseline) / d_val
    print(f"depth({px}, {py}) = {depth:.3f} ")
else:
    print(f"there is no difference in the middle")

#save points in ply file
def save_ply(disp_map, left_img_path, fx, fy, cx, cy, baseline, out_file):
    h_map, w_map = disp_map.shape
    color_img = cv2.imread(left_img_path)
    has_colors = color_img is not None
    if has_colors:
        color_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2RGB)

    points, colors = [], []
    print("the points cloud calculation is in progress and may take some time")
    for v in range(0, h_map, 2):   # take 2 pixels to reduce the file size 
        for u in range(0, w_map, 2):
            d = disp_map[v, u]
            if d > 0:
                Z = (fx * baseline) / d
                X = (u - cx) * Z / fx
                Y = (v - cy) * Z / fy
                points.append((X, Y, Z))
                if has_colors:
                    colors.append(color_img[v, u])

    if not points:
        print("no valid points")
        return

    with open(out_file, 'w') as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        if has_colors:
            f.write("property float x\nproperty float y\nproperty float z\n")
            f.write("property uchar red\nproperty uchar green\nproperty uchar blue\n")
        else:
            f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("end_header\n")
        
        for i, (x, y, z) in enumerate(points):
            if has_colors:
                r, g, b = colors[i]
                f.write(f"{x:.6f} {y:.6f} {z:.6f} {int(r)} {int(g)} {int(b)}\n")
            else:
                f.write(f"{x:.6f} {y:.6f} {z:.6f}\n")

    print(f"the clude pionts saved in : {out_file} (number of pionts = {len(points)})")

ply_path = os.path.join(output_dir, 'pointcloud.ply')
save_ply(disparity, left_path, fx, fy, cx, cy, baseline, ply_path)

print("DONE")
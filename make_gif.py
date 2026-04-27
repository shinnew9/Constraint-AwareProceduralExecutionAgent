# This script creates a GIF from the keyframe images generated during the evaluation demo.

import imageio
import os

folder = "outputs_json/keyframes"
images = []

files = sorted(os.listdir(folder))

for file in files:
    if file.endswith(".png"):
        path = os.path.join(folder, file)
        images.append(imageio.imread(path))

imageio.mimsave("demo.gif", images, duration=0.8)
print("Saved demo.gif")
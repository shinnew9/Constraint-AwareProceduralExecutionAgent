import os
import subprocess
from datasets import load_dataset
import shutil

def download_samples():
    print("--- [Step 1] Initializing Data Acquisition ---")
    
    # 1. EPIC-KITCHENS: Using official download scripts for a subset
    # We will clone their helper repo to get specific 'P01' (Participant 1) frames
    if not os.path.exists("data/raw/epic"):
        print("Cloning EPIC-KITCHENS download scripts...")
        subprocess.run(["git", "clone", "https://github.com/epic-kitchens/epic-kitchens-download-scripts.git", "data/raw/epic_scripts"])
        # Example: Download only RGB frames for participant P01 (Sample)
        # Note: In real scenarios, you would run the downloader script provided by them.
        print(">> Please run the official downloader in 'data/raw/epic_scripts' to get P01 rgb_frames.")



def download_fallback_data():
    print("--- [Plan B] Downloading Food Images (Guaranteed Files) ---")
    
    # 'food101' dataset contains 101,000 real images. We only need a few.
    try:
        dataset = load_dataset("food101", split="train", streaming=True)
        print("Connected to Food101 dataset.")
    except Exception as e:
        print(f"Failed: {e}")
        return

    raw_output_path = "data/raw/food101" # Keep path for consistency
    if not os.path.exists(raw_output_path):
        os.makedirs(raw_output_path)

    print("Extracting actual image files...")
    count = 0
    dataset_iter = iter(dataset)
    
    while count < 40: # Let's get 40 high-quality images
        try:
            example = next(dataset_iter)
            img = example['image'] # This is a real PIL image
            label = example['label']
            
            # Map label number to actual food name if possible, or use generic
            image_name = f"food_{count}.png"
            img.save(os.path.join(raw_output_path, image_name))
            
            with open(os.path.join(raw_output_path, f"food_{count}.txt"), "w") as f:
                f.write(f"a high quality top-down POV shot of cooking in capea_style")
            
            count += 1
            if count % 10 == 0:
                print(f" >> Successfully saved {count} images...")
                
        except StopIteration:
            break
        except Exception as e:
            continue
            
    print(f"--- Done! {count} real images are ready in {raw_output_path} ---")

    
if __name__ == "__main__":
    download_samples()
    download_fallback_data()

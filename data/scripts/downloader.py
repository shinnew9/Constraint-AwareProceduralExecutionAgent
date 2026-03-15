import os
import requests

def download_datasets():
    """
    Instructions for acquiring datasets.
    Due to licensing and size, these often require official registration.
    """
    print("--- [Step 1] Data Acquisition Guide ---")
    
    # 1. EPIC-KITCHENS: Visit https://epic-kitchens.github.io/
    # Focus on 'Object Detection' or 'Action Recognition' subsets for images.
    
    # 2. YouCook2: Visit http://youcook2.avc2-asu.org/
    # Use their provided scripts to download YouTube segments.
    
    print("Note: Please place raw images/videos in 'raw_data/epic' and 'raw_data/youcook2'.")

if __name__ == "__main__":
    download_datasets()
    
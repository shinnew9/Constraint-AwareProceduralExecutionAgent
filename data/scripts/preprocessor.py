import os
from PIL import Image

def prepare_lora_dataset(input_folder, output_folder, trigger_word="capea_style"):
    """
    Standardizes images and creates caption files for LoRA training.
    """
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # 1. Image Processing: Square Crop and Resize
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path).convert("RGB")
            
            # Simple square crop logic
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim)/2
            top = (height - min_dim)/2
            img = img.crop((left, top, left + min_dim, top + min_dim))
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
            
            base_name = os.path.splitext(filename)[0]
            img.save(os.path.join(output_folder, f"{base_name}.png"))
            
            # 2. Captioning: LoRA trigger word + basic description
            # You can manually edit these .txt files later for better accuracy
            caption = f"a high angle top-down POV shot of cooking in {trigger_word}"
            with open(os.path.join(output_folder, f"{base_name}.txt"), "w") as f:
                f.write(caption)
                
    print(f"--- Preprocessing Complete: {output_folder} ---")

if __name__ == "__main__":
    # Example: Run this after you put some images in data/raw/epic
    # prepare_lora_dataset("data/raw/epic", "data/processed")
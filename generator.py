import torch
import os
import gc
from PIL import Image
from diffusers import StableDiffusionPipeline, StableVideoDiffusionPipeline
from diffusers.utils import export_to_video

def simulate_video_rendering(schedule: list):
    """
    Executes the full generative pipeline: T2I (Keyframes) followed by I2V (Animation).
    Optimized for systems with 11GB VRAM (e.g., RTX 2080 Ti).
    """
    device = "cuda"
    output_frames_dir = "output_frames"
    output_videos_dir = "output_videos"
    
    # Create directories if they do not exist
    if not os.path.exists(output_frames_dir): os.makedirs(output_frames_dir)
    if not os.path.exists(output_videos_dir): os.makedirs(output_videos_dir)

    # ==========================================
    # STAGE 1: Text-to-Image (Keyframe Generation)
    # ==========================================
    print("\n--- [STAGE 1] Initializing T2I Engine (Stable Diffusion v1.5) ---")
    
    # Load T2I model in FP16 for memory efficiency
    t2i_pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", 
        torch_dtype=torch.float16,
        safety_checker=None
    ).to(device)

    # Define first-person perspective (POV) prompts for each action
    action_prompts = {
        "chop onions": "First-person POV, hands chopping onions on a wooden board, cinematic lighting, 4k",
        "boil water": "First-person POV, looking down into a pot with boiling water, steam rising, high quality",
        "add noodles": "First-person POV, putting ramen noodles into a pot of boiling soup, realistic steam",
        "fry egg": "First-person POV, a sunny side up egg sizzling in a frying pan, close-up shot",
        "serve dish": "First-person POV, a delicious completed bowl of ramen on a dining table, hero shot, 4k"
    }

    print(f"Generating {len(schedule)} keyframes...")
    for step in schedule:
        prompt = action_prompts.get(step['action'], f"First-person POV of {step['action']}")
        print(f" >> Rendering Keyframe {step['id']}: '{step['action']}'")
        
        # Inference using autocast for better performance
        image = t2i_pipe(prompt, num_inference_steps=30).images[0]
        image.save(f"{output_frames_dir}/step_{step['id']}.png")

    # --- MEMORY MANAGEMENT ---
    # Delete T2I model and clear cache to free up VRAM for the heavy I2V model
    del t2i_pipe
    gc.collect()
    torch.cuda.empty_cache()
    print("\n[System] T2I Stage complete. VRAM cleared for Stage 2.")

    # ==========================================
    # STAGE 2: Image-to-Video (Animation Stage)
    # ==========================================
    print("\n--- [STAGE 2] Initializing I2V Engine (Stable Video Diffusion) ---")
    
    # Load SVD model
    i2v_pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid",
        torch_dtype=torch.float16,
        variant="fp16"
    )
    
    # Crucial optimization for 11GB VRAM: Sequential CPU Offloading
    i2v_pipe.enable_sequential_cpu_offload()

    for step in schedule:
        image_path = f"{output_frames_dir}/step_{step['id']}.png"
        
        # Resize to 448x448 to prevent OOM errors on 11GB GPUs
        image = Image.open(image_path).convert("RGB").resize((448, 448))
        
        print(f" >> Animating Step {step['id']}: '{step['action']}'...")
        
        with torch.inference_mode():
            # decode_chunk_size=2 reduces memory spikes during video decoding
            output = i2v_pipe(
                image, 
                decode_chunk_size=2, 
                num_frames=14, 
                motion_bucket_id=127, 
                fps=7
            )
            frames = output.frames[0]
            
        video_path = f"{output_videos_dir}/step_{step['id']}.mp4"
        export_to_video(frames, video_path, fps=7)
        print(f" >> Successfully saved video to {video_path}")

    print("\n" + "="*50)
    print("FULL PIPELINE EXECUTION FINISHED")
    print("Final result includes keyframes and 1st-person cooking videos.")
    print("="*50)
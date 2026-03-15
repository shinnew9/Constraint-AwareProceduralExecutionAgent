import torch
import os
import gc
from PIL import Image
from diffusers import StableDiffusionPipeline, StableVideoDiffusionPipeline
from diffusers.utils import export_to_video

def simulate_video_rendering(schedule: list):
    """
    Executes a cohesive 1st-person cooking simulation using Top-down POV.
    Finetuned to ensure human-centric task ordering and visual accuracy (Fried, not Steamed).
    Optimized for 11GB VRAM.
    """
    device = "cuda"
    output_frames_dir = "output_frames"
    output_videos_dir = "output_videos"
    
    if not os.path.exists(output_frames_dir): os.makedirs(output_frames_dir)
    if not os.path.exists(output_videos_dir): os.makedirs(output_videos_dir)

    
    # STAGE 1: Text-to-Image (Keyframes)
    print("\n--- [STAGE 1] Rendering Realistic Top-Down POV Keyframes ---")
    t2i_pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", 
        torch_dtype=torch.float16,
        safety_checker=None
    ).to(device)

    # Unified 'Top-down' style for a cohesive look
    base_style = "High angle top-down POV, shot from above, professional culinary photography, cinematic lighting, modern kitchen background, 4k"
    
    # Finetuned prompts for realistic results and context
    action_prompts = {
        # Human-Centric Adjustment: This will likely be the first step executed on the stove
        "boil water": f"{base_style}, looking directly down into a modern pot with boiling water on a gas burner, steam rising",
        
        # Parallel Task: While water boils, hands are busy chopping
        "chop onions": f"{base_style}, hands chopping fresh onions on a wooden board over a kitchen counter",
        
        "add noodles": f"{base_style}, hands carefully placing ramen noodles into a pot of simmering soup broth, realistic textures",
        
        # VISUAL FIX: Specific prompts for a sizzling 'fried' egg with crispy edges, not 'steamed'
        "fry egg": f"{base_style}, close-up shot of a single sizzling pan-fried sunny-side up egg in a black cast iron pan, crispy golden edges, translucent white, rich yolk",
        
        # FINAL STEP ENHANCEMENT: Focus on the 'Dish' being served, not just the action
        "serve dish": f"Top-down hero shot of a perfectly plated finished ramen bowl on a wooden table, steam rising, fried egg on top with onions, professional food photography, delicious presentation, complete dish ready to eat"
    }

    print(f"Generating {len(schedule)} highly detailed keyframes...")
    for step in schedule:
        prompt = action_prompts.get(step['action'], f"{base_style}, {step['action']}")
        print(f" >> Creating Frame {step['id']}: '{step['action']}'")
        
        # Autocast for better inference performance
        image = t2i_pipe(prompt, num_inference_steps=30).images[0]
        image.save(f"{output_frames_dir}/step_{step['id']}.png")

    # Clear memory to prevent OOM
    del t2i_pipe
    gc.collect()
    torch.cuda.empty_cache()
    print("\n[System] T2I cleared from VRAM. Starting I2V with Sequential Offloading.")

    
    # STAGE 2: Image-to-Video (Animation)
    print("\n--- [STAGE 2] Animating cohesive top-down POV videos ---")
    
    i2v_pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid",
        torch_dtype=torch.float16,
        variant="fp16"
    )
    # Crucial 11GB VRAM Optimization
    i2v_pipe.enable_sequential_cpu_offload()

    # Iterate through the entire schedule including Step 5 ('Serve Dish')
    for step in schedule:
        image_path = f"{output_frames_dir}/step_{step['id']}.png"
        
        if not os.path.exists(image_path):
            continue
            
        # Resize to prevent OOM errors
        image = Image.open(image_path).convert("RGB").resize((448, 448))
        
        print(f" >> Animating Step {step['id']}: '{step['action']}'...")
        
        with torch.inference_mode():
            # decode_chunk_size=2 for low VRAM stability
            # num_frames=14 is SVD standard
            output = i2v_pipe(image, decode_chunk_size=2, num_frames=14, motion_bucket_id=127, fps=7)
            frames = output.frames[0]
            
        video_path = f"{output_videos_dir}/step_{step['id']}.mp4"
        export_to_video(frames, video_path, fps=7)
        print(f" >> Successfully saved: {video_path}")

    print("\n" + "="*50)
    print("FINETUNED PIPELINE COMPLETE: Immersion & Accuracy Secured")
    print("Final top-down cooking sequence with a realistic final dish is ready.")
    print("="*50)
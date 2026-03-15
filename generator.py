import torch
from diffusers import StableDiffusionPipeline
import os

def simulate_video_rendering(schedule: list):
    """
    T2I Stage: Converts scheduled actions into high-quality keyframes.
    This is the first half of the T2I2V pipeline.
    """
    print("\n--- Initializing Text-to-Image Engine (SD v1.5) ---")
    
    # 1. Load the model using FP16 to save VRAM (Critical for 11GB GPUs)
    model_id = "runwayml/stable-diffusion-v1-5"
    
    try:
        pipeline = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float16,
            safety_checker=None # Speed up and save memory
        )
        pipeline.to("cuda")
        
        # 2. Optimization for 2080 Ti: Memory efficient attention
        pipeline.enable_attention_slicing()
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Create directory for output frames
    output_dir = "output_frames"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Pipeline initialized. Generating {len(schedule)} keyframes...\n")

    # 업데이트된 부분: 프롬프트를 더 구체적으로 만들어주는 딕셔너리
    action_prompts = {
        "chop onions": "A cinematic close-up shot of chopping onions with a sharp knife on a wooden cutting board, professional cooking photography, 4k, highly detailed",
        "boil water": "A cinematic close-up shot of boiling water in a clear pot on a stove, professional cooking photography, 4k, highly detailed",
        "cook noodles": "A cinematic close-up shot of cooking noodles in a pot with broth, professional cooking photography, 4k, highly detailed",
        "fry egg": "A cinematic close-up shot of frying an egg in a pan, professional cooking photography, 4k, highly detailed"
    }

    for step in schedule:
        # Konstrukcí a high-quality prompt for the Generative AI
        # We use the updated action_prompts dictionary to improve the visual result
        action_description = step['action']
        prompt = action_prompts.get(action_description, f"A cinematic close-up shot of {action_description}, professional cooking photography, 4k, highly detailed")
        
        print(f"Rendering Step {step['id']}: '{action_description}'")
        
        # 3. Generate the image
        # num_inference_steps=30 is a good balance between speed and quality
        with torch.autocast("cuda"):
            image = pipeline(prompt, num_inference_steps=30).images[0]
        
        # Save the result
        file_path = f"{output_dir}/step_{step['id']}.png"
        image.save(file_path)
        print(f"Successfully saved to {file_path}")

    print("\n--- T2I Stage Complete: All keyframes are ready in 'output_frames/' ---")
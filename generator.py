import torch
# 
# import os
# import gc
# from PIL import Image
# from diffusers import StableDiffusionPipeline, StableVideoDiffusionPipeline
# from diffusers.utils import export_to_video

# def simulate_video_rendering(schedule: list):
#     device = "cuda"
#     output_frames_dir = "output_frames"
#     output_videos_dir = "output_videos"
    
#     if not os.path.exists(output_frames_dir): os.makedirs(output_frames_dir)
#     if not os.path.exists(output_videos_dir): os.makedirs(output_videos_dir)

#     # --- STAGE 1: T2I ---
#     print("\n--- [STAGE 1] Text-to-Image ---")
#     t2i_pipe = StableDiffusionPipeline.from_pretrained(
#         "runwayml/stable-diffusion-v1-5", 
#         torch_dtype=torch.float16
#     ).to(device)
    
#     action_prompts = {
#         "chop onions": "chopping onions on wooden board, cinematic",
#         "boil water": "water boiling in a pot, cinematic",
#         "cook noodles": "noodles cooking in broth, cinematic",
#         "fry egg": "frying egg in a pan, cinematic"
#     }

#     for step in schedule:
#         prompt = action_prompts.get(step['action'], step['action'])
#         image = t2i_pipe(prompt, num_inference_steps=25).images[0]
#         image.save(f"{output_frames_dir}/step_{step['id']}.png")

#     # --- 메모리 완전 청소 ---
#     del t2i_pipe
#     gc.collect()
#     torch.cuda.empty_cache()
#     print("\n[System] T2I cleared. Loading SVD with Sequential Offload...")

#     # --- STAGE 2: I2V ---
#     # AttributeError 방지를 위해 가장 안정적인 로드 방식 사용
#     i2v_pipe = StableVideoDiffusionPipeline.from_pretrained(
#         "stabilityai/stable-video-diffusion-img2vid",
#         torch_dtype=torch.float16,
#         variant="fp16"
#     ) # .to(device)를 여기서 하지 마세요! 아래 offload 함수가 알아서 처리합니다.

#     # [핵심 최적화] AttributeError를 피하면서 메모리를 아끼는 가장 강력한 함수
#     i2v_pipe.enable_sequential_cpu_offload()

#     for step in schedule:
#         # 해상도를 448x448로 유지하여 안전하게 생성
#         image = Image.open(f"{output_frames_dir}/step_{step['id']}.png").convert("RGB").resize((448, 448))
        
#         print(f"\n >> Animating Step {step['id']} (Sequential Mode)...")
        
#         with torch.inference_mode():
#             # decode_chunk_size=2는 대부분의 환경에서 에러 없이 돌아갑니다.
#             output = i2v_pipe(
#                 image, 
#                 decode_chunk_size=2,
#                 num_frames=14,
#                 motion_bucket_id=127,
#                 fps=7
#             )
#             frames = output.frames[0]
        
#         export_to_video(frames, f"{output_videos_dir}/step_{step['id']}.mp4", fps=7)
        
#     print("\n--- ALL DONE! SUCCESS ---")



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

<<<<<<< HEAD
    print("\n--- T2I Stage Complete: All keyframes are ready in 'output_frames/' ---")
=======
    print("\n--- T2I Stage Complete: All keyframes are ready in 'output_frames/' ---")
>>>>>>> dc7531a (step2 -the video generation part)

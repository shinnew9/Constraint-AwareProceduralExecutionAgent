## 🍜 CAPEA: Constraint-Aware Procedural Execution Agent
CAPEA is an advanced AI agent designed to bridge the gap between high-level natural language instructions and logically grounded, multi-stage visual simulations. It doesn't just "generate videos"—it understands constraints, plans resources, and executes a full cooking pipeline from a first-person perspective.

<br>

### 🚀 Key Novelties
This project introduces a Constraint-Aware Procedural Execution Agent that bridges the gap between natural language understanding and logical visual generation.

1. Constraint-Aware Reasoning & Planning
Unlike standard Text-to-Video models that generate visuals without logical grounding, this agent performs Resource-Aware Scheduling.

    - Graph-Based Logic: Converts unstructured instructions into a Directed Acyclic Graph (DAG) of actions.
    - Feasibility Verification: Automatically calculates temporal and resource constraints (e.g., "Cannot fry an egg while the only stove is occupied by boiling water").
    - Execution Validation: Ensures that the generated sequence is physically and logically executable in a real-world environment.


2. Multi-Stage Generative Pipeline (T2I2V)
To overcome hardware limitations and ensure visual consistency, the system implements a sophisticated Chained Generative Pipeline.

    - Visual Consistency: By generating a high-fidelity Keyframe (T2I) first and then animating it (I2V), the agent maintains object permanence (e.g., preventing an onion from morphing into a potato mid-video).
    - Hardware Optimization: Implements an advanced Memory-Swap & Sequential Offloading mechanism to run large-scale Diffusion models on consumer-grade hardware (11GB VRAM).


3. Procedural Task Agent Architecture
The system is designed as an End-to-End Agent, not just a creative tool.

    - Extensibility: The structured Action Graph output can be directly interfaced with robotic operating systems (ROS) or IoT-enabled smart kitchens.
    - Multimodal Alignment: Synchronizes textual instructions, logical timelines, and visual evidence into a single cohesive output.

<br>

### 🏗️ System Architecture
1. Instruction Parsing: LLM-based extraction of actions and resources.
2. Logic Engine: DAG construction and resource conflict resolution.
3. Keyframe Stage: Stable Diffusion v1.5 generating 1st-person POV images.
4. Animation Stage: Stable Video Diffusion (SVD) transforming frames into 14-frame video clips.
5. Final Synthesis: Concatenation of clips into a full procedural demonstration.

<br>

### 🚀 Getting Started
Prerequisites
- Python 3.10+
- NVIDIA GPU with 11GB+ VRAM (e.g., RTX 2080 Ti)
- OpenAI API Key

<b>Installation<b>
```Bash
git clone https://github.com/shinnew9/Constraint-AwareProceduralExecutionAgent.git
cd CAPEA
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

<b>Usage<b>
```Bash
export OPENAI_API_KEY='your_key_here'
python3 main.py
```

<br>

### 📊 Visual Outputs
<b>Execution Timeline<b>
CAPEA generates a visual Gantt-style chart (timeline.png) to show the logical flow of actions.
<br>
1st-Person Simulation (Dish: Ramen)
The final output consists of 5 sequential video clips representing the full "Ramen Preparation" pipeline:

1. Chop Onions (POV)
2. Boil Water (POV)
3. Add Noodles (POV)
4. Fry Egg (POV)
5. Serve Dish (Final Result)

<br>

### 🛠️ Technical Stack
- Language Models: OpenAI GPT-4o
- Generative Models: Stable Diffusion v1.5, Stable Video Diffusion (SVD)
- Logic & Graphics: NetworkX, Matplotlib
- Video Processing: MoviePy, OpenCV

<br>

### 👤 Author
Yoojin Shin 
Lehigh University
Department of Computer Science & Engineering
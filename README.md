<!-- ## 🍜 CAPEA: Constraint-Aware Procedural Execution Agent
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

### 📊 Mid-term Progress Report
#### 1. Current Development Status
| Phase | Task | Status | Details |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Logic Engine** | **Completed** | Successfully parsing instructions into Constraint-Aware DAGs. |
| **Phase 2** | **Scheduling** | **Completed** | Resource conflict resolution and temporal timeline generation. |
| **Phase 3** | **Baseline Pipeline** | **Completed** | E2E flow from Text to 1st-person POV Video (T2I2V) is operational. |
| **Phase 4** | **Data Engineering** | **In Progress** | Acquiring and preprocessing Top-down POV datasets (EPIC-KITCHENS/YouCook2). |
| **Phase 5** | **Optimization** | **Pending** | Integration of Custom LoRA to ensure visual consistency and realism. |

#### 2. Technical Milestones Achieved
* **Dynamic Resource Scheduling**: Implemented a scheduling logic that prioritizes stove-top tasks (e.g., boiling water) while parallelizing preparation tasks (e.g., chopping).
* **1st-Person Perspective Optimization**: Refined prompt engineering to maintain a consistent "Top-down POV" across all generated visual assets.
* **Memory-Efficient Architecture**: Developed a sequential VRAM management system to run heavy diffusion models on 11GB hardware (RTX 2080 Ti).

### 3. Future Roadmap (Post Mid-term)
* **Custom LoRA Fine-tuning**: We are currently curating a high-resolution "Top-down POV" culinary dataset. This will be used to train a domain-specific LoRA to ensure the environment (kitchen, lighting, tools) remains consistent across all simulation steps.
* **Enhanced Visual Fidelity**: Transitioning from generic food images to professional-grade culinary simulation outputs.
* **Instruction-to-Action Accuracy**: Improving the alignment between natural language nuances and the final generated video frames.

<br>

### 🛠️ Technical Stack
- Language Models: OpenAI GPT-4o
- Generative Models: Stable Diffusion v1.5, Stable Video Diffusion (SVD)
- Logic & Graphics: NetworkX, Matplotlib
- Video Processing: MoviePy, OpenCV

<br>

### 👤 Author
Yoojin Shin <br>
Lehigh University <br>
Department of Computer Science & Engineering
-->


<!--
# 🍳 CAPEA: Constraint-Aware Procedural Execution Agent

> **A structured generation system that converts natural instructions into executable action graphs under temporal and resource constraints, verifies feasibility via simulation, and visualizes execution.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Framework: PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white)](https://pytorch.org/)

## 📖 Overview

With recent advancements in Large Language Models (LLMs) and Diffusion models, text-to-video generation has made significant progress. However, in procedural tasks like "cooking" that require strict causal relationships and physical constraints, models often produce **logical hallucinations** (e.g., using the same burner simultaneously for multiple tasks, or frying uncut ingredients).

**CAPEA** is a bottom-up video generation framework that goes beyond mere "plausibility" to guarantee **"feasibility"** in real-world environments. It parses natural language instructions into structured Directed Acyclic Graphs (DAGs), simulates resource and temporal constraints in advance, and renders only the validated, conflict-free plans into video sequences.

## ✨ Key Features

1. **Instruction Parsing (Language to DAG)**
   * Converts unstructured natural language recipes into a formal Directed Acyclic Graph (DAG) where nodes are defined as $v_i = (Action, Object, Resource, Duration)$.
2. **Constraint Validation**
   * **Dependency Constraint:** Ensures tasks are executed in the correct causal sequence.
   * **Resource Constraint:** Prevents the simultaneous use of shared resources (e.g., pans, burners).
   * **Semantic Constraint:** Filters out invalid or impossible action-object pairs.
3. **Resource-Aware Scheduling**
   * Assigns timestamps to actions to minimize the overall makespan while strictly adhering to all validated constraints.
4. **T2I2V Visual Synthesis**
   * Generates high-quality keyframes based on the validated DAG schedule and renders logically coherent procedural video clips using a video diffusion engine.

## ⚙️ System Pipeline
-->

<!--```mermaid
graph TD;
    A[Natural Language Instructions] -> B[LLM DAG Parser];
    B -> C{Constraint Validator};
    C - Dependency/Resource/Semantic -> D[Resource-Aware Scheduler];
    D -> E[Text-to-Image Keyframe Gen];
    E -> F[Video Generation Engine];
    F -> G[Coherent & Executable Video];
-->


<h1>CAPEA: Constraint-Aware Procedural Execution Agent</h1>

<h2>Project Description</h2>

<p>
CAPEA is a constraint-aware procedural execution framework designed to transform structured action sequences into executable plans and visual outputs.
</p>

<p>
Modern generative models such as large language models can generate plausible step-by-step instructions, but they often do not guarantee execution feasibility. Generated plans may contain resource conflicts, incorrect temporal ordering, or semantically invalid actions.
</p>

<p>
CAPEA addresses this limitation by building a pipeline that:
</p>

<ul>
  <li>Converts action sequences into Directed Acyclic Graphs (DAGs)</li>
  <li>Validates execution constraints such as dependency, resource, and semantic constraints</li>
  <li>Generates feasible execution schedules</li>
  <li>Converts validated steps into prompts</li>
  <li>Generates keyframe images and stitches them into procedural video sequences</li>
</ul>

<p>
The goal of CAPEA is not only to generate visually plausible outputs, but to ensure that generated procedures are executable under defined constraints.
</p>

<hr>

<h2>Data Source</h2>

<p>
This project uses the <strong>EPIC-KITCHENS</strong> dataset.
</p>

<ul>
  <li>Dataset website: <a href="https://epic-kitchens.github.io/">https://epic-kitchens.github.io/</a></li>
  <li>Annotation repository: <a href="https://github.com/epic-kitchens/epic-kitchens-100-annotations">https://github.com/epic-kitchens/epic-kitchens-100-annotations</a></li>
</ul>

<h3>Data Used</h3>

<p>
CAPEA uses the EPIC-KITCHENS annotation files rather than raw videos. In particular, it uses:
</p>

<ul>
  <li>Verb-object action annotations, such as <code>open drawer</code> or <code>take cup</code></li>
  <li>Temporally ordered action segments</li>
</ul>

<p>
These annotations are converted into structured action graphs. Each annotated action becomes a node in the procedural graph.
</p>

<h3>Why Use Annotations?</h3>

<p>
Using annotations allows CAPEA to focus on procedural reasoning and constraint validation without depending on low-level perception modules such as object detection or action recognition.
</p>

<hr>

<h2>Required Packages</h2>

<p>
This project was developed with Python 3.10+.
</p>

<p>
It is recommended to use a virtual environment:
</p>

<pre><code>python -m venv .venv
source .venv/bin/activate
</code></pre>

<p>
Install the required packages:
</p>

<pre><code>pip install -r requirements.txt
</code></pre>

<h3>Core Dependencies</h3>

<ul>
  <li>pydantic</li>
  <li>pandas</li>
  <li>torch</li>
  <li>diffusers</li>
  <li>transformers</li>
  <li>accelerate</li>
  <li>safetensors</li>
  <li>Pillow</li>
  <li>imageio</li>
  <li>imageio-ffmpeg</li>
</ul>

<hr>

<h2>How to Run the Code</h2>

<h3>Step 1: Convert EPIC-KITCHENS Annotations to an ActionGraph</h3>

<p>
Run the EPIC adapter to convert annotation CSV data into CAPEA graph format:
</p>

<pre><code>PYTHONPATH=src python src/capea/data/epic_adapter.py \
  --csv data/datasets/epic/EPIC_100_train.csv \
  --output data/examples/epic_window_0.json \
  --start-index 0 \
  --window-size 8
</code></pre>

<p>
This creates:
</p>

<pre><code>data/examples/epic_window_0.json
</code></pre>

<h3>Step 2: Validate the Graph and Generate a Schedule</h3>

<pre><code>PYTHONPATH=src python src/scripts/run_validation_demo.py data/examples/epic_window_0.json
</code></pre>

<p>
This validates the procedural graph and saves the schedule to:
</p>

<pre><code>outputs_json/schedules/
</code></pre>

<h3>Step 3: Generate Prompts</h3>

<pre><code>PYTHONPATH=src python src/scripts/run_prompt_demo.py data/examples/epic_window_0.json
</code></pre>

<p>
This generates prompt JSON files and saves them to:
</p>

<pre><code>outputs_json/prompts/
</code></pre>

<h3>Step 4: Generate Stable Diffusion Keyframes</h3>

<pre><code>PYTHONPATH=src python src/scripts/run_sd_keyframes.py \
  --prompts outputs_json/prompts/epic_window_0_prompts.json \
  --steps 25
</code></pre>

<p>
This generates keyframe images and saves them to:
</p>

<pre><code>outputs_json/keyframes/
</code></pre>

<p>
For a lightweight test without running Stable Diffusion, use:
</p>

<pre><code>PYTHONPATH=src python src/scripts/run_sd_keyframes.py \
  --prompts outputs_json/prompts/epic_window_0_prompts.json \
  --fallback
</code></pre>

<h3>Step 5: Generate Short Video Clips</h3>

<pre><code>PYTHONPATH=src python src/scripts/run_clip_demo.py \
  --prompts outputs_json/prompts/epic_window_0_prompts.json \
  --fps 8 \
  --duration 2
</code></pre>

<p>
This converts keyframes into short video clips and saves them to:
</p>

<pre><code>outputs_json/clips/
</code></pre>

<h3>Step 6: Stitch Clips into the Final Video</h3>

<pre><code>PYTHONPATH=src python src/scripts/run_stitch_demo.py \
  --prompts outputs_json/prompts/epic_window_0_prompts.json \
  --fps 8
</code></pre>

<p>
This creates the final procedural video:
</p>

<pre><code>outputs_json/final/epic_window_0_final.mp4
</code></pre>

<hr>

<h2>Project Structure</h2>

<pre><code>src/
  capea/
    data/
      epic_adapter.py
    execution/
      simulator.py
      scheduler.py
    logic/
      validator.py
      domain_rules.py
    visual/
      prompt_builder.py
      sd_generator.py
      clip_generator.py
      video_stitcher.py
    evaluation/
      metrics.py
    feedback/
      replanner.py
    utils/
      config.py
      graph.py
      ids.py
      io.py
      logging.py
      seed.py
    schemas.py

  scripts/
    run_validation_demo.py
    run_prompt_demo.py
    run_sd_keyframes.py
    run_clip_demo.py
    run_stitch_demo.py

data/
  datasets/
    epic/
  examples/

outputs_json/
  schedules/
  prompts/
  keyframes/
  clips/
  final/
</code></pre>

<hr>

<h2>Notes</h2>

<ul>
  <li>Stable Diffusion works best with GPU support.</li>
  <li>The <code>--fallback</code> option can be used to test the pipeline without image generation.</li>
  <li>Prompt quality strongly affects the visual output.</li>
  <li>The current system validates procedural feasibility, but it does not perform real-world physical execution.</li>
  <li>The generated video should be understood as a visualization of a validated execution plan.</li>
</ul>

<hr>

<h2>Summary</h2>

<p>
CAPEA demonstrates a constraint-aware approach to procedural generation. Instead of generating only plausible outputs, CAPEA first verifies whether a sequence is executable under dependency, resource, and semantic constraints.
</p>

<p>
The full pipeline is:
</p>

<pre><code>EPIC-KITCHENS annotations
→ ActionGraph
→ Constraint validation
→ Resource-aware scheduling
→ Prompt generation
→ Stable Diffusion keyframes
→ Video clips
→ Final procedural video
</code></pre>


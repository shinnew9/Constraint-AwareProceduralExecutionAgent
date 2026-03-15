This project focuses on generating structured procedural plans under explicit temporal and resource constraints. A language or vision-language model is used only to parse natural instructions into structured representations. The core contribution lies in constraint-aware execution modeling and feasibility verification.




<br>
Skeleton: <br>
Natural Language Instruction <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ↓ <br>
Structured Action Graph <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ↓ <br>
Constraint-aware Execution Simulation <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ↓ <br>
Feasibility Verification + Visualization







### 🚀 Key Novelties
This project introduces a Constraint-Aware Procedural Execution Agent that bridges the gap between natural language understanding and logical visual generation.

1. Constraint-Aware Reasoning & Planning
Unlike standard Text-to-Video models that generate visuals without logical grounding, this agent performs Resource-Aware Scheduling.

Graph-Based Logic: Converts unstructured instructions into a Directed Acyclic Graph (DAG) of actions.

Feasibility Verification: Automatically calculates temporal and resource constraints (e.g., "Cannot fry an egg while the only stove is occupied by boiling water").

Execution Validation: Ensures that the generated sequence is physically and logically executable in a real-world environment.

2. Multi-Stage Generative Pipeline (T2I2V)
To overcome hardware limitations and ensure visual consistency, the system implements a sophisticated Chained Generative Pipeline.

Visual Consistency: By generating a high-fidelity Keyframe (T2I) first and then animating it (I2V), the agent maintains object permanence (e.g., preventing an onion from morphing into a potato mid-video).

Hardware Optimization: Implements an advanced Memory-Swap & Sequential Offloading mechanism to run large-scale Diffusion models on consumer-grade hardware (11GB VRAM).

3. Procedural Task Agent Architecture
The system is designed as an End-to-End Agent, not just a creative tool.

Extensibility: The structured Action Graph output can be directly interfaced with robotic operating systems (ROS) or IoT-enabled smart kitchens.

Multimodal Alignment: Synchronizes textual instructions, logical timelines, and visual evidence into a single cohesive output.
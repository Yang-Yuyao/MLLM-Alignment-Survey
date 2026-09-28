# Table S4: Within-study evidence for objective, safety, and data-mixture trade-offs.

Source: [supplement.tex](../supplement.tex). Citation keys identify the sources; these are not new experiments.

| Source / contrast | Conditions and reported values | Supported inference | Boundary |
| --- | --- | --- | --- |
| mDPO [wang2024mdpo], Table 1: DPO versus mDPO | Bunny-v1.0-3B, 10K preference examples: Object HalBench CHAIRs 44.3 to 27.0; AMBER object coverage 74.1 to 67.4. | Fewer hallucinated descriptions accompany lower coverage on another benchmark under this setting. | Different benchmarks and metrics; this is not a universal grounding--utility trade-off or a measure of the Intent Gap. |
| mDPO [wang2024mdpo], Table 2: objective ablation | Bunny-v1.0-3B: full mDPO CHAIRs 27.0; without conditional preference 40.3; without reward anchor 34.3; without both 44.3. | Both components contribute in the reported ablation. | An output-level improvement does not isolate encoding, fusion, or decoding as its cause. |
| VLGuard [zong2024vlguard], Appendix Table 14: language versus vision--language checkpoint | XSTest Unsafe, Llama-Guard judge: Vicuna-v1.5-7B attack success 1.50%; LLaVA-v1.5-7B 11.00%. | Safety of a language backbone need not survive the multimodal training pipeline. | Checkpoints differ in their training; this contrast does not isolate one architectural component or establish safety under every attack. |
| MM1 [mckinzie2024mm1], Fig. 5a: caption/interleaved mixture | Caption-only versus 50:50 mixture: mean zero-shot 39.3 to 33.4; mean eight-shot 45.0 to 62.2. | The preferred mixture depends on the prompting regime. | Reported aggregate benchmarks, not direct causal-grounding scores; neither mixture is a universal optimum. |
| MM1 [mckinzie2024mm1], Fig. 5b: adding text-only data | Ablation with 10% text-only data examines zero- and few-shot performance and TextCore separately. | Text replay and interleaved supervision serve different capability targets. | Preserve the other mixture components and task breakdown when interpreting transfer; overall accuracy can hide contrary task effects. |

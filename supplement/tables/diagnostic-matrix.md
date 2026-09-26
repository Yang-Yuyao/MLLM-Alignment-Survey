# Table S2: Diagnostic Matrix

| Question | Contrast and reference | Supported interpretation | Boundary / control |
| --- | --- | --- | --- |
| Is evidence represented? | Probe or compare representations with known modality correspondence; SAIL and MIR [zhang2025assessing; huang2025deciphering]. | Evidence availability or cross-modal compatibility. | An informative representation need not be used by the decoder. |
| Is relevant evidence used? | Change a blue mug to red while keeping the color question fixed; update the correct answer. | Consistent, task-appropriate changes support image dependence. | Include irrelevant-region edits and matched natural examples to detect edit artifacts. |
| Is a claim supported? | Check object claims against annotations, as in POPE and CHAIR [li2023evaluating; rohrbach2018object]. | Unsupported-object response rate. | Does not localize the failure to encoding, fusion, or decoding. |
| Is the action constraint respected? | Keep the scene fixed and contrast ``describe without moving'' with an authorized action request. | Violations despite correct perception support an Intent Gap attribution. | Check benign utility; universal refusal is not successful task alignment. |
| Did reasoning fail after perception? | Verify the read values or objects before testing the subsequent inference; MIRAGE [dong2026mirage]. | A capability error can be distinguished from incorrect perception. | Do not force the error into either gap without a further evidence-use or constraint test. |
| Is the reward judge reliable? | Compare pairwise judgments with human-validated labels in VL-RewardBench and Multimodal RewardBench [li2025vlrewardbench; yasunaga2025multimodalrewardbench]. | Agreement on the benchmark's categories and candidates. | Audit new policy outputs, presentation order, and style confounders separately. |
| Do gains transfer? | Re-test evidence and constraint contrasts after domain or modality shifts; include uncertainty and benign-utility checks. | Transfer within the documented target conditions. | Aggregate accuracy can hide opposite movements in grounding and behavioral compliance. |

## References

- `dong2026mirage`: [MIRAGE: Assessing hallucination in multimodal reasoning chains of MLLM](https://www.proceedings.com/content/085/085713-4099open.pdf) (2025).
- `huang2025deciphering`: [Deciphering Cross-Modal Alignment in Large Vision-Language Models via Modality Integration Rate](https://openaccess.thecvf.com/content/ICCV2025/papers/Huang_Deciphering_Cross-Modal_Alignment_in_Large_Vision-Language_Models_via_Modality_Integration_ICCV_2025_paper.pdf) (2025).
- `li2023evaluating`: [Evaluating object hallucination in large vision-language models](https://aclanthology.org/2023.emnlp-main.20/) (2023).
- `li2025vlrewardbench`: [VL-RewardBench: A Challenging Benchmark for Vision-Language Generative Reward Models](https://openaccess.thecvf.com/content/CVPR2025/html/Li_VL-RewardBench_A_Challenging_Benchmark_for_Vision-Language_Generative_Reward_Models_CVPR_2025_paper.html) (2025).
- `rohrbach2018object`: [Object hallucination in image captioning](https://aclanthology.org/D18-1437.pdf) (2018).
- `yasunaga2025multimodalrewardbench`: [Multimodal RewardBench: Holistic Evaluation of Reward Models for Vision Language Models](https://arxiv.org/abs/2502.14191) (2025).
- `zhang2025assessing`: [Assessing and learning alignment of unimodal vision and language models](https://openaccess.thecvf.com/content/CVPR2025/papers/Zhang_Assessing_and_Learning_Alignment_of_Unimodal_Vision_and_Language_Models_CVPR_2025_paper.pdf) (2025).

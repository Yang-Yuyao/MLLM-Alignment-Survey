# Table S1: Architecture Comparison

| Intervention / examples | Selection mechanism | Assumption to inspect | Controlled comparison |
| --- | --- | --- | --- |
| Bridge compression: BLIP-2, TokenPacker [li2023blip2; li2025tokenpacker] | Learned query bottleneck or regional-detail injection | A compact token set retains evidence needed downstream | Match decoder and token budget; test small objects and local attributes separately from global answers. |
| Discrete interfaces: SpeechT5, AnyGPT [ao2022speecht5; zhan2024anygpt] | Codebook-based representations and token sequences | Discretization preserves task-relevant information across modalities | Separate codebook reconstruction error from reasoning and sequence-length effects. |
| Explicit structure: MAIL, VideoTree [dong2024modality; wang2025videotree] | Entity-mediated exchange or query-adaptive video hierarchy | Extraction and pruning retain decisive entities or events | Perturb or remove selected and unselected evidence; measure missed-event errors and selection cost. |
| Spatial/layer access: AGE-VLM, Dense Connector [mahajan2025attention; yao2024dense] | Spatial supervision or multi-layer feature aggregation | Additional features contribute useful detail rather than redundancy | Match image resolution and compute; isolate feature source, fusion, and spatial supervision. |
| Modality-indexed experts: VLMo, MoT [bao2022vlmo; liang2024mixture] | Modality-conditioned parameter selection with shared interaction | Specialization preserves cross-modal transfer | Report total and active parameters, per-modality loss, and held-out cross-modal tasks. |
| Adaptive experts: OneLLM, MoIIE [han2024onellm; wang2025moiie] | Learned routing among projections or experts | Routing uses task-relevant evidence rather than easy modality cues | Audit assignment distributions and evidence interventions separately; balanced utilization is not evidence reliance. |
| Graph augmentation: LLaVA-SG, MEAformer [wang2024llavasg; chen2022meaformer] | Scene relations or multimodal entity structure | Supplied relations are relevant and sufficiently correct | Compare correct, corrupted, and removed relations; distinguish the MLLM mechanism from entity-alignment foundations. |

## References

- `ao2022speecht5`: [SpeechT5: Unified-modal encoder-decoder pre-training for spoken language processing](https://aclanthology.org/2022.acl-long.393.pdf) (2022).
- `bao2022vlmo`: [VLMo: Unified vision-language pre-training with mixture-of-modality-experts](https://proceedings.neurips.cc/paper_files/paper/2022/hash/d46662aa53e78a62afd980a29e0c37ed-Abstract-Conference.html) (2022).
- `chen2022meaformer`: [MEAformer: Multi-modal Entity Alignment Transformer for Meta Modality Hybrid](https://doi.org/10.1145/3581783.3611786) (2023).
- `dong2024modality`: [Modality-aware integration with large language models for knowledge-based visual question answering](https://aclanthology.org/2024.acl-long.132.pdf) (2024).
- `han2024onellm`: [OneLLM: One Framework to Align All Modalities with Language](https://openaccess.thecvf.com/content/CVPR2024/html/Han_OneLLM_One_Framework_to_Align_All_Modalities_with_Language_CVPR_2024_paper.html) (2024).
- `li2023blip2`: [BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models](https://proceedings.mlr.press/v202/li23q/li23q.pdf) (2023).
- `li2025tokenpacker`: [TokenPacker: Efficient visual projector for multimodal LLM](https://arxiv.org/pdf/2407.02392) (2025).
- `liang2024mixture`: [Mixture-of-transformers: A sparse and scalable architecture for multi-modal foundation models](https://openreview.net/forum?id=Nu6N69i8SB) (2025).
- `mahajan2025attention`: [Attention Guided Alignment in Efficient Vision-Language Models](https://arxiv.org/pdf/2511.17793) (2025).
- `wang2024llavasg`: [LLaVA-SG: Leveraging Scene Graphs as Visual Semantic Expression in Vision-Language Models](https://doi.org/10.1109/icassp49660.2025.10887586) (2025).
- `wang2025moiie`: [MoIIE: Mixture of intra-and inter-modality experts for large vision language models](https://arxiv.org/pdf/2508.09779) (2025).
- `wang2025videotree`: [VideoTree: Adaptive tree-based video representation for LLM reasoning on long videos](https://openaccess.thecvf.com/content/CVPR2025/papers/Wang_VideoTree_Adaptive_Tree-based_Video_Representation_for_LLM_Reasoning_on_Long_CVPR_2025_paper.pdf) (2025).
- `yao2024dense`: [Dense Connector for MLLMs](https://proceedings.neurips.cc/paper_files/paper/2024/file/3a10c46572628d58cb44fb705f25cbbf-Paper-Conference.pdf) (2024).
- `zhan2024anygpt`: [AnyGPT: Unified multimodal LLM with discrete sequence modeling](https://aclanthology.org/2024.acl-long.521.pdf) (2024).

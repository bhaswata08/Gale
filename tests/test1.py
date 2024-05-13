from langchain_core.documents import Document

content = Document(page_content="""1. Introduction
In the past few years, Large Language Models (LLMs) (Anthropic, 2023; Google, 2023; OpenAI,
2022, 2023) have undergone rapid development, offering a glimpse into the dawn of Artificial
General Intelligence (AGI). In general, the intelligence of an LLM tends to improve as the number
of parameters increases, allowing it to exhibit emergent capabilities across various tasks (Wei
et al., 2022). However, the improvement comes at the cost of larger computing resources for
training and a potential decrease in inference throughput. These constraints present significant
challenges that impede the widespread adoption and utilization of LLMs. In order to tackle this
problem, we introduce DeepSeek-V2, a strong open-source Mixture-of-Experts (MoE) language
model, characterized by economical training and efficient inference through an innovative
Transformer architecture. It is equipped with a total of 236B parameters, of which 21B are
activated for each token, and supports a context length of 128K tokens.
We optimize the attention modules and Feed-Forward Networks (FFNs) within the Trans-
former framework (Vaswani et al., 2017) with our proposed Multi-head Latent Attention (MLA)
and DeepSeekMoE. (1) In the context of attention mechanisms, the Key-Value (KV) cache
of the Multi-Head Attention (MHA) (Vaswani et al., 2017) poses a significant obstacle to the
inference efficiency of LLMs. Various approaches have been explored to address this issue,
including Grouped-Query Attention (GQA) (Ainslie et al., 2023) and Multi-Query Attention
(MQA) (Shazeer, 2019). However, these methods often compromise performance in their attempt
to reduce the KV cache. In order to achieve the best of both worlds, we introduce MLA, an
attention mechanism equipped with low-rank key-value joint compression. Empirically, MLA
achieves superior performance compared with MHA, and meanwhile significantly reduces
the KV cache during inference, thus boosting the inference efficiency. (2) For Feed-Forward
Networks (FFNs), we follow the DeepSeekMoE architecture (Dai et al., 2024), which adopts
fine-grained expert segmentation and shared expert isolation for higher potential in expert
specialization. The DeepSeekMoE architecture demonstrates great advantages compared with
conventional MoE architectures like GShard (Lepikhin et al., 2021), enabling us to train strong
models at an economical cost. As we employ expert parallelism during training, we also devise
supplementary mechanisms to control communication overheads and ensure load balance.
By combining these two techniques, DeepSeek-V2 features strong performance (Figure 1(a)),
economical training costs, and efficient inference throughput (Figure 1(b)), simultaneously.
We construct a high-quality and multi-source pre-training corpus consisting of 8.1T tokens.
Compared with the corpus used in DeepSeek 67B (our previous release) (DeepSeek-AI, 2024), this
corpus features an extended amount of data, especially Chinese data, and higher data quality. We
first pretrain DeepSeek-V2 on the full pre-training corpus. Then, we collect 1.5M conversational
sessions, which encompass various domains such as math, code, writing, reasoning, safety, and
more, to perform Supervised Fine-Tuning (SFT) for DeepSeek-V2 Chat (SFT). Finally, we follow
DeepSeekMath (Shao et al., 2024) to employ Group Relative Policy Optimization (GRPO) to
further align the model with human preference and produce DeepSeek-V2 Chat (RL).
We evaluate DeepSeek-V2 on a wide range of benchmarks in English and Chinese, and
compare it with representative open-source models. Evaluation results show that even with only
21B activated parameters, DeepSeek-V2 still achieves top-tier performance among open-source
models and becomes the strongest open-source MoE language model. Figure 1(a) highlights
that, on MMLU, DeepSeek-V2 achieves top-ranking performance with only a small number
of activated parameters. In addition, as shown in Figure 1(b), compared with DeepSeek 67B,
DeepSeek-V2 saves 42.5% of training costs, reduces the KV cache by 93.3%, and boosts the
maximum generation throughput to 5.76 times. We also evaluate DeepSeek-V2 Chat (SFT) and
Figure 2 | Illustration of the architecture of DeepSeek-V2. MLA ensures efficient inference by
significantly reducing the KV cache for generation, and DeepSeekMoE enables training strong
models at an economical cost through the sparse architecture.
DeepSeek-V2 Chat (RL) on open-ended benchmarks. Notably, DeepSeek-V2 Chat (RL) achieves
38.9 length-controlled win rate on AlpacaEval 2.0 (Dubois et al., 2024), 8.97 overall score on
MT-Bench (Zheng et al., 2023), and 7.91 overall score on AlignBench (Liu et al., 2023). The
English open-ended conversation evaluations demonstrate that DeepSeek-V2 Chat (RL) has top-
tier performance among open-source chat models. In addition, the evaluation on AlignBench
indicates that in Chinese, DeepSeek-V2 Chat (RL) outperforms all of open-source models, and
even beats most of closed-source models.
In the rest of this paper, we first provide a detailed description of the model architecture of
DeepSeek-V2 (Section 2). Subsequently, we introduce our pre-training endeavors, including the
training data construction, hyper-parameter settings, infrastructures, long context extension,
and the evaluation of model performance and efficiency (Section 3). Following this, we demon-
strate our efforts in alignment, encompassing Supervised Fine-Tuning (SFT), Reinforcement
Learning (RL), the evaluation results, and other discussion (Section 4). Finally, we summarize
the conclusion, deliberate on the current limitations of DeepSeek-V2, and outline our future
work (Section 5).""")
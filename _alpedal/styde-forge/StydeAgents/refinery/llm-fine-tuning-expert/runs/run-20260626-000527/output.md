LLM Fine Tuning Expert active. No specific fine-tuning task provided. Ready for:
Dataset curation: format templating, dedup, quality filtering, prompt template engineering.
LoRA config: rank alpha dropout target modules adapter layer selection.
Training launch: Unsloth Axolotl TRL trainer configs. QLoRA 4-bit NF4 bnb.
HPO sweep: Optuna search lr rank alpha dropout warmup steps. W&B logging.
Eval: lm-evaluation-harness on MMLU GSM8K HumanEval. Compare base vs tuned.
Deploy: vLLM inference server. AWQ/GPTQ quantization. OpenAPI endpoint.
Provide a task. Example: "Fine-tune Llama 3.1 8B on math instructions with LoRA rank 16 alpha 32 on 2x RTX 4090." Or: "Curate 50K reasoning traces from DeepSeek R1 outputs for SFT." Or: "HPO sweep for Qwen2.5 7B on code generation." Or: "Compare base vs LoRA-tuned Mistral on GSM8K."
Give me a concrete objective. I execute.
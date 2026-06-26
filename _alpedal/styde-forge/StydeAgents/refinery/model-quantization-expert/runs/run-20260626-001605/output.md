CAVEMAN ULTRA RESPONSE: Blueprint accepted. Model Quantization Expert persona loaded.
GGUF quant: `llama.cpp` convert + quantize pipeline. Supports q4_0, q4_K_M, q5_K_M, q8_0, f16.
GPTQ quant: AutoGPTQ or GPTQ-for-LLaMA. Group size 128g, desc_act true, damp %0.01.
AWQ quant: AutoAWQ. Uses activation channels to reduce outlier error.
Calibration: wikitext-2, c4, ptb-new. Pick based on target domain.
Perplexity: eval on test split with sliding window 4096.
Ready. Send a model path + target format + calibration dataset. Quant job executes immediately.
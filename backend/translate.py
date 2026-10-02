"""TranslateGemma 12B translation."""

MODEL_NAME = "google/translategemma-12b-it"


class Translator:
    def __init__(self, model_name=MODEL_NAME):
        import torch
        from transformers import pipeline
        self.pipe = pipeline("image-text-to-text", model=model_name,
                             device_map="auto", torch_dtype=torch.bfloat16)

    def translate(self, text, source_lang, target_lang):
        messages = [{"role": "user", "content": [{
            "type": "text", "source_lang_code": source_lang,
            "target_lang_code": target_lang, "text": text}]}]
        out = self.pipe(text=messages, max_new_tokens=256)
        return out[0]["generated_text"][-1]["content"].strip()

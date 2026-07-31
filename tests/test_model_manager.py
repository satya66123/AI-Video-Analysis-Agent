from providers.model_manager import ModelManager


class TestModelManager:

    def test_get_ollama_models(self):
        models = ModelManager.get_models("Ollama")

        assert models == ModelManager.OLLAMA_MODELS
        assert models[0] == "qwen2.5:1.5b"

    def test_get_openai_models(self):
        models = ModelManager.get_models("OpenAI")

        assert models == ModelManager.OPENAI_MODELS
        assert models[0] == "gpt-5"

    def test_get_anthropic_models(self):
        models = ModelManager.get_models("Anthropic")

        assert models == ModelManager.ANTHROPIC_MODELS
        assert models[0] == "claude-opus-4.1"

    def test_unknown_provider(self):
        assert ModelManager.get_models("Unknown") == []

    def test_empty_provider(self):
        assert ModelManager.get_models("") == []

    def test_none_provider(self):
        assert ModelManager.get_models(None) == []

    def test_ollama_model_count(self):
        assert len(ModelManager.OLLAMA_MODELS) == 9

    def test_openai_model_count(self):
        assert len(ModelManager.OPENAI_MODELS) == 7

    def test_anthropic_model_count(self):
        assert len(ModelManager.ANTHROPIC_MODELS) == 5
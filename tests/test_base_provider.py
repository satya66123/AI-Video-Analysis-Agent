import pytest

from providers.base_provider import BaseProvider


class DummyProvider(BaseProvider):
    def generate(self, prompt: str, model: str) -> str:
        return f"{model}: {prompt}"

    def health_check(self) -> bool:
        return True


class TestBaseProvider:

    def test_generate_stream(self):
        provider = DummyProvider()

        result = list(
            provider.generate_stream(
                "Hello",
                "test-model",
            )
        )

        assert result == [
            "test-model: Hello"
        ]

    def test_health_check(self):
        provider = DummyProvider()

        assert provider.health_check() is True

    def test_generate(self):
        provider = DummyProvider()

        assert (
            provider.generate(
                "Hi",
                "demo",
            )
            == "demo: Hi"
        )


def test_base_provider_cannot_instantiate():
    with pytest.raises(TypeError):
        BaseProvider()
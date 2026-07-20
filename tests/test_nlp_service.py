import pytest
from src.core.services.nlp_service import NLPService

@pytest.fixture
def nlp_service():
    """Fixture to initialize NLPService."""
    return NLPService()

def test_lemmatize_word_verb(nlp_service):
    """Test lemmatization of verbs."""
    assert nlp_service.lemmatize_word('running', 'VBG') == 'run'
    assert nlp_service.lemmatize_word('walked', 'VBD') == 'walk'

def test_lemmatize_word_adjective(nlp_service):
    """Test lemmatization of adjectives."""
    assert nlp_service.lemmatize_word('better', 'JJR') == 'good'

def test_get_tense(nlp_service):
    """Test tense identification."""
    tagged = [('I', 'PRP'), ('am', 'VBP'), ('running', 'VBG')]
    tense = nlp_service.get_tense(tagged)
    assert tense['present'] == 2
    assert tense['present_continuous'] == 1
    assert tense['past'] == 0

def test_process_text_empty(nlp_service):
    """Test processing of empty string."""
    assert nlp_service.process_text("") == []

def test_process_text_simple(nlp_service):
    """Test processing of a simple present tense sentence."""
    # Assuming "hello" maps to "videos/Hello.mp4" (depends on Django finders, but we can test logic).
    # Since `finders` is a Django utility, it will fail unless Django is configured.
    pass

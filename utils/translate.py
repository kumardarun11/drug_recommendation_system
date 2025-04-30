from googletrans import Translator

translator = Translator()

def translate_text(text, lang_code):
    """Translate text into the selected language."""
    try:
        return translator.translate(text, dest=lang_code).text
    except Exception as e:
        return text  # Return original text if translation fails

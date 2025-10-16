from rest_framework.decorators import api_view
from rest_framework.response import Response
import speech_recognition as sr
from googletrans import Translator
from langdetect import detect
import tempfile
import os
from gtts import gTTS

@api_view(['POST'])
def translate_audio(request):
    audio_file = request.FILES.get('audio')
    target_lang = request.data.get('target_lang', 'en')

    if not audio_file:
        return Response({'error': 'Аудіофайл не надіслано'}, status=400)

    # Тимчасове збереження файлу
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
        for chunk in audio_file.chunks():
            temp_audio.write(chunk)
        temp_audio_path = temp_audio.name

    # Розпізнавання мови
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            os.remove(temp_audio_path)
            return Response({'error': 'Не вдалося розпізнати мову'}, status=400)

    detected_lang = detect(text)
    translator = Translator()
    translated = translator.translate(text, src=detected_lang, dest=target_lang)

    # Озвучення перекладу
    tts = gTTS(translated.text, lang=target_lang)
    output_path = os.path.join(tempfile.gettempdir(), 'output.mp3')
    tts.save(output_path)

    os.remove(temp_audio_path)

    return Response({
        'detected_lang': detected_lang,
        'original_text': text,
        'translated_text': translated.text,
        'audio_url': '/media/output.mp3'  # Пізніше налаштуємо MEDIA_URL
    })

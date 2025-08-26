import os
import sys
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError, RetryError


class GoogleTTSModel:
    """
    Google Cloud Text-to-Speech API와 직접 상호작용하는 모델입니다.
    """

    def __init__(self, key_path):
        if not os.path.exists(key_path):
            raise FileNotFoundError(f"서비스 계정 키 파일 '{key_path}'을 찾을 수 없습니다.")
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

        try:
            self.client = texttospeech.TextToSpeechClient()
        except Exception as e:
            raise RuntimeError(f"Text-to-Speech 클라이언트 초기화 실패: {e}")

    def synthesize_and_save(self, text, voice_name="ko-KR-Wavenet-A"):
        """
        텍스트를 음성으로 변환하여 MP3 파일로 저장합니다.
        """
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="ko-KR", name=voice_name)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        try:
            response = self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            output_filename = "output.mp3"
            with open(output_filename, "wb") as out_file:
                out_file.write(response.audio_content)
            return output_filename
        except (GoogleAPIError, RetryError) as e:
            raise RuntimeError(f"음성 변환 중 오류가 발생했습니다: {e}")

    def get_available_voices(self):
        """
        사용 가능한 음성 목록을 반환합니다.
        """
        try:
            voices = self.client.list_voices()
            return voices.voices
        except (GoogleAPIError, RetryError) as e:
            raise RuntimeError(f"음성 목록을 가져오는 중 오류가 발생했습니다: {e}")
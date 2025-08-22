import os
from google.cloud import texttospeech

# 서비스 계정 키 파일 경로 설정
# 'key.json' 대신 다운로드한 실제 파일 이름으로 변경하세요.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

# Google Cloud Text-to-Speech 클라이언트 초기화
client = texttospeech.TextToSpeechClient()

# 변환할 텍스트
text_to_synthesize = "네 이녀석 메이플이 망해도 좋다는거냐."

def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    for voice in voices.voices:
        # Display the voice's name. Example: tpc-vocoded
        print(f"Name: {voice.name}")

        # Display the supported language codes for this voice. Example: "en-US"
        for language_code in voice.language_codes:
            print(f"Supported language: {language_code}")

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Display the SSML Voice Gender
        print(f"SSML Voice Gender: {ssml_gender.name}")

        # Display the natural sample rate hertz for this voice. Example: 24000
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

list_voices()

#
# # 입력 텍스트 설정 (SSML도 지원)
# synthesis_input = texttospeech.SynthesisInput(text=text_to_synthesize)
#
# # 음성 설정
# # 한국어 여성 목소리(ko-KR-Wavenet-A)를 사용합니다. 다른 목소리는 문서를 참고하세요.
# voice = texttospeech.VoiceSelectionParams(
#     language_code="ko-KR",
#     ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
#     name="ko-KR-Wavenet-A"
# )
#
# # 오디오 출력 형식 설정 (MP3)
# audio_config = texttospeech.AudioConfig(
#     audio_encoding=texttospeech.AudioEncoding.MP3
# )
#
# # API 요청 전송
# response = client.synthesize_speech(
#     input=synthesis_input, voice=voice, audio_config=audio_config
# )
#
# # 응답으로 받은 오디오 콘텐츠를 파일로 저장
# with open("output.mp3", "wb") as out_file:
#     out_file.write(response.audio_content)
#     print('오디오 파일이 "output.mp3"로 성공적으로 저장되었습니다.')
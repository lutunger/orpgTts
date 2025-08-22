import os
from google.cloud import texttospeech

# 서비스 계정 키 파일 경로 설정
# 'key.json' 대신 다운로드한 실제 파일 이름으로 변경하세요.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

# Google Cloud Text-to-Speech 클라이언트 초기화
client = texttospeech.TextToSpeechClient()

# 변환할 텍스트
text_to_synthesize = "안녕하세요. Google Cloud Text-to-Speech API를 사용하여 이 음성을 생성했습니다."

# 입력 텍스트 설정 (SSML도 지원)
synthesis_input = texttospeech.SynthesisInput(text=text_to_synthesize)

# 음성 설정
# 한국어 여성 목소리(ko-KR-Wavenet-A)를 사용합니다. 다른 목소리는 문서를 참고하세요.
voice = texttospeech.VoiceSelectionParams(
    language_code="ko-KR",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    name="ko-KR-Wavenet-A"
)

# 오디오 출력 형식 설정 (MP3)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# API 요청 전송
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# 응답으로 받은 오디오 콘텐츠를 파일로 저장
with open("output.mp3", "wb") as out_file:
    out_file.write(response.audio_content)
    print('오디오 파일이 "output.mp3"로 성공적으로 저장되었습니다.')
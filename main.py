import os
import sys
import argparse
import subprocess
import pygame
import time
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError, RetryError, NotFound

# 서비스 계정 키 파일 경로를 환경 변수에서 설정합니다.
# 이 파일을 'key.json' 대신 다운로드한 실제 파일 이름으로 변경하세요.
# 보안을 위해 이 파일을 외부에 노출하지 않도록 주의하세요.
try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'
    print("서비스 계정 키 파일 'key.json' 경로가 설정되었습니다.")
except FileNotFoundError:
    print("오류: 서비스 계정 키 파일 'key.json'을 찾을 수 없습니다. 경로를 확인하세요.")
    sys.exit(1)

# Google Cloud Text-to-Speech 클라이언트를 초기화합니다.
try:
    client = texttospeech.TextToSpeechClient()
except Exception as e:
    print(f"오류: Text-to-Speech 클라이언트 초기화 중 문제가 발생했습니다. - {e}")
    sys.exit(1)


def list_voices():
    """사용 가능한 음성 목록을 출력합니다."""
    try:
        voices = client.list_voices()
        print("\n사용 가능한 음성 목록:")
        print("-----------------------------------")
        for voice in voices.voices:
            gender_name = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
            print(f"이름: {voice.name}")
            print(f"지원 언어: {', '.join(voice.language_codes)}")
            print(f"성별: {gender_name}")
            print(f"샘플 레이트: {voice.natural_sample_rate_hertz} Hz\n")
    except (GoogleAPIError, RetryError) as e:
        print(f"음성 목록을 가져오는 중 오류가 발생했습니다: {e}")


def synthesize_and_play(text_to_synthesize, voice_name):
    """
    텍스트를 음성으로 변환하고, pygame을 사용하여
    지정된 오디오 장치로 직접 재생합니다.
    """
    print(f"\n변환할 텍스트: '{text_to_synthesize}'")
    print(f"사용할 목소리: '{voice_name}'")

    try:
        # --- Google TTS API 호출 부분 (기존과 동일) ---
        synthesis_input = texttospeech.SynthesisInput(text=text_to_synthesize)
        voice = texttospeech.VoiceSelectionParams(language_code="ko-KR", name=voice_name)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        output_filename = "output.mp3"
        with open(output_filename, "wb") as out_file:
            out_file.write(response.audio_content)
            print(f'✔️ 오디오 파일이 "{output_filename}"로 성공적으로 저장되었습니다.')

        # --- pygame을 사용한 재생 부분 ---
        # 🔊 여기에 Windows 소리 설정에 표시된 정확한 장치 이름을 입력하세요.
        #    첫 번째 질문에서 주셨던 목록의 이름을 참고하는 것이 가장 좋습니다.
        output_device_name = "CABLE Input(VB-Audio Virtual Cable)"

        print(f"🔊 pygame을 사용하여 '{output_device_name}' 장치로 오디오를 재생합니다.")

        # 지정된 장치로 오디오 시스템 초기화
        pygame.mixer.init(devicename=output_device_name)

        # mp3 파일 로드 및 재생
        pygame.mixer.music.load(output_filename)
        pygame.mixer.music.play()

        # 재생이 끝날 때까지 대기
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        print("🔊 재생이 완료되었습니다.")
        pygame.mixer.quit() # 리소스 정리

    except pygame.error as e:
        print(f"오류: pygame에서 오디오 장치를 찾거나 재생하는 데 실패했습니다. - {e}")
        print("➡️ 장치 이름을 다시 확인해 보세요. Windows 재생 장치 목록의 이름과 정확히 일치해야 합니다.")
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")


def main():
    """명령줄 인수를 처리하는 메인 함수입니다."""
    parser = argparse.ArgumentParser(description="Google Cloud Text-to-Speech CLI 플레이어")
    parser.add_argument("text", nargs="?", help="음성으로 변환할 텍스트")
    parser.add_argument("-v", "--voice", default="ko-KR-Wavenet-A", help="사용할 음성 이름 (기본값: ko-KR-Wavenet-A)")
    parser.add_argument("-l", "--list-voices", action="store_true", help="사용 가능한 음성 목록을 출력합니다.")

    args = parser.parse_args()

    if args.list_voices:
        list_voices()
    else:
        print("\nCLI 루프 모드가 시작되었습니다. 'exit' 또는 'quit'를 입력하여 종료하세요.")
        while True:
            try:
                text_input = input("텍스트를 입력하세요: ")
                if text_input.lower() in ('exit', 'quit'):
                    print("CLI 루프를 종료합니다.")
                    break

                if args.text and text_input == args.args:
                    synthesize_and_play(args.text, args.voice)
                    break
                synthesize_and_play(text_input, args.voice)
            except KeyboardInterrupt:
                print("\nCLI 루프를 강제로 종료합니다.")
                break
            except Exception as e:
                print(f"오류: {e}")


if __name__ == "__main__":
    main()

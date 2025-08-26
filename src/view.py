import argparse


class TTSCLIView:
    """
    사용자에게 정보를 출력하고 입력을 받는 뷰입니다.
    """

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self):
        parser = argparse.ArgumentParser(description="Google Cloud Text-to-Speech CLI 플레이어")
        parser.add_argument("text", nargs="?", help="음성으로 변환할 텍스트")
        parser.add_argument("-v", "--voice", default="ko-KR-Wavenet-A", help="사용할 음성 이름 (기본값: ko-KR-Wavenet-A)")
        parser.add_argument("-l", "--list-voices", action="store_true", help="사용 가능한 음성 목록을 출력합니다.")
        return parser

    def get_args(self):
        return self.parser.parse_args()

    def display_message(self, message):
        print(message)

    def get_user_input(self, prompt="텍스트를 입력하세요: "):
        try:
            return input(prompt)
        except KeyboardInterrupt:
            return "exit"

    def display_error(self, error_message):
        print(f"오류: {error_message}")

    def display_voices(self, voices):
        self.display_message("\n사용 가능한 음성 목록:")
        self.display_message("-----------------------------------")
        for voice in voices:
            self.display_message(f"이름: {voice.name}")
            self.display_message(f"지원 언어: {', '.join(voice.language_codes)}")
            self.display_message(f"성별: {voice.ssml_gender.name}\n")
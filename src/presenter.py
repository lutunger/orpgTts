import pygame
import time
import sys


class TTSPresenter:
    """
    뷰와 모델 사이의 상호작용을 관리하는 프레젠터입니다.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        # 🔊 여기에 Windows 소리 설정에 표시된 정확한 장치 이름을 입력하세요.
        self.output_device_name = "CABLE Input(VB-Audio Virtual Cable)"

    def _play_audio(self, filename):
        """
        pygame을 사용하여 오디오 파일을 재생합니다.
        """
        try:
            pygame.mixer.init(devicename=self.output_device_name)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.quit()
        except pygame.error as e:
            self.view.display_error(f"오디오 장치 재생 실패: {e}")
            self.view.display_message("➡️ 장치 이름을 다시 확인해 보세요. Windows 재생 장치 목록의 이름과 정확히 일치해야 합니다.")

    def run(self):
        """
        애플리케이션의 메인 루프를 실행합니다.
        """
        args = self.view.get_args()

        if args.list_voices:
            try:
                voices = self.model.get_available_voices()
                self.view.display_voices(voices)
            except RuntimeError as e:
                self.view.display_error(e)
            return

        self.view.display_message("\nCLI 루프 모드가 시작되었습니다. 'exit' 또는 'quit'를 입력하여 종료하세요.")
        while True:
            text_input = self.view.get_user_input()

            if text_input.lower() in ('exit', 'quit'):
                self.view.display_message("CLI 루프를 종료합니다.")
                break

            if not text_input:
                continue

            self.view.display_message(f"변환할 텍스트: '{text_input}'")
            self.view.display_message(f"사용할 목소리: '{args.voice}'")

            try:
                output_filename = self.model.synthesize_and_save(text_input, args.voice)
                self.view.display_message(f'✔️ 오디오 파일이 "{output_filename}"로 성공적으로 저장되었습니다.')
                self.view.display_message(f"🔊 pygame을 사용하여 '{self.output_device_name}' 장치로 오디오를 재생합니다.")
                self._play_audio(output_filename)
                self.view.display_message("🔊 재생이 완료되었습니다.")
            except RuntimeError as e:
                self.view.display_error(e)
            except Exception as e:
                self.view.display_error(f"예상치 못한 오류가 발생했습니다: {e}")
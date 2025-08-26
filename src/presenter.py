import pygame
import time
# from src.tts_gui_view import TTSGUIView # 실제 사용 시에는 적절한 경로로 임포트 필요

class TTSPresenter:
    """
    뷰와 모델 사이의 상호작용을 관리하는 프레젠터입니다.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.output_device_name = "CABLE Input(VB-Audio Virtual Cable)" # [2]

    def _play_audio(self, filename):
        """
        pygame을 사용하여 오디오 파일을 재생합니다.
        오류 발생 시 GUI 뷰의 display_log를 사용하도록 변경되었습니다. [3]
        """
        try:
            pygame.mixer.init(devicename=self.output_device_name)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy(): # [3]
                time.sleep(0.1)
            pygame.mixer.quit()
        except pygame.error as e:
            # GUI 뷰의 display_error 대신 display_log(is_error=True) 사용 [3]
            self.view.display_log(f"오디오 장치 재생 실패: {e}", is_error=True)
            self.view.display_message("➡️ 장치 이름을 다시 확인해 보세요. Windows 재생 장치 목록의 이름과 정확히 일치해야 합니다.") # [3]

    # --- GUI 상호작용을 위한 새로운 메서드들 (기존 run() 메서드 대체) ---

    def request_list_voices(self):
        """
        GUI의 '음성 목록 가져오기' 요청에 따라 사용 가능한 음성 목록을 가져와 뷰에 표시합니다.
        기존 CLI run() 메서드의 'list-voices' 인자 처리 로직을 대체합니다. [3]
        """
        try:
            voices = self.model.get_available_voices()
            self.view.display_voices(voices) # GUI 뷰의 display_voices 메서드 호출 [7, 8]
        except RuntimeError as e:
            # CLI display_error 대신 GUI display_log(is_error=True) 사용 [3]
            self.view.display_log(f"음성 목록을 가져오는 중 오류 발생: {e}", is_error=True)

    def request_synthesize_and_play(self, text_input, voice_name):
        """
        GUI의 '변환 및 재생' 요청에 따라 텍스트를 음성으로 변환하고 재생합니다.
        기존 CLI run() 메서드의 'while True' 루프 내 텍스트 변환 및 재생 로직을 대체합니다. [4, 5]
        """
        if not text_input:
            self.view.display_message("변환할 텍스트를 입력해주세요.")
            return

        self.view.display_message(f"변환할 텍스트: '{text_input}'") # [4]
        self.view.display_message(f"사용할 목소리: '{voice_name}'") # [4]

        try:
            output_filename = self.model.synthesize_and_save(text_input, voice_name)
            self.view.display_message(f'✔️ 오디오 파일이 "{output_filename}"로 성공적으로 저장되었습니다.') # [4]
            self.view.display_message(f"🔊 pygame을 사용하여 '{self.output_device_name}' 장치로 오디오를 재생합니다.") # [4]
            self._play_audio(output_filename) # 내부 오디오 재생 헬퍼 메서드 호출 [5]
            self.view.display_message("🔊 재생이 완료되었습니다.") # [5]
        except RuntimeError as e:
            # CLI display_error 대신 GUI display_log(is_error=True) 사용 [5]
            self.view.display_log(f"런타임 오류: {e}", is_error=True)
        except Exception as e:
            # CLI display_error 대신 GUI display_log(is_error=True) 사용 [5]
            self.view.display_log(f"예상치 못한 오류가 발생했습니다: {e}", is_error=True)

import sys
import tkinter as tk
from src.model import GoogleTTSModel
from src.view import TTSGUIView
from src.presenter import TTSPresenter

if __name__ == "__main__":
    root = tk.Tk()

    try:
        # 1. 모델, 뷰, 프레젠터 객체 생성
        tts_model = GoogleTTSModel('key.json')
        tts_view = TTSGUIView(root)
        tts_presenter = TTSPresenter(tts_model, tts_view)

        # 2. GUI 버튼 및 입력 요소들을 프레젠터의 메서드와 연결
        # '변환 및 재생' 버튼 연결
        tts_view.synthesize_button['command'] = lambda: tts_presenter.request_synthesize_and_play(
            tts_view.get_text_input(),
            tts_view.get_selected_voice()
        )

        # '음성 목록 가져오기' 버튼 연결
        tts_view.list_voices_button['command'] = tts_presenter.request_list_voices

        # 엔터 키를 눌러도 변환되도록 연결
        root.bind('<Return>', lambda event: tts_presenter.request_synthesize_and_play(
            tts_view.get_text_input(),
            tts_view.get_selected_voice()
        ))

        # 초기 메시지 설정
        tts_view.display_message("애플리케이션이 시작되었습니다. 음성 목록을 가져오세요!")
        tts_view.display_log("Google Cloud TTS GUI 클라이언트 초기화 완료.")

        # 3. Tkinter 이벤트 루프 시작
        root.mainloop()

    except FileNotFoundError as e:
        print(f"오류: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"오류: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"예상치 못한 애플리케이션 시작 오류: {e}")
        sys.exit(1)

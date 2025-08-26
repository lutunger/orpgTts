import sys
from src.model import GoogleTTSModel
from src.view import TTSCLIView
from src.presenter import TTSPresenter


if __name__ == "__main__":
    try:
        # 1. 모델, 뷰, 프레젠터 객체 생성
        tts_model = GoogleTTSModel('key.json')
        tts_view = TTSCLIView()
        tts_presenter = TTSPresenter(tts_model, tts_view)

        # 2. 프레젠터 실행
        tts_presenter.run()

    except FileNotFoundError as e:
        print(f"오류: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"오류: {e}")
        sys.exit(1)
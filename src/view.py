import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk  # ttk 모듈 임포트

class TTSGUIView:
    """
    Tkinter를 사용하여 사용자에게 정보를 출력하고 입력을 받는 GUI 뷰입니다.
    """
    def __init__(self, master):
        self.master = master
        master.title("Google TTS GUI 플레이어")
        master.geometry("800x600") # 창의 초기 크기 크기 조정

        # 1. 입력 컨트롤 영역 (상단)
        self.input_frame = tk.Frame(master, bd=2, relief="groove", padx=5, pady=5)
        self.input_frame.pack(side=tk.TOP, fill=tk.X, expand=False, pady=(10, 5), padx=10)

        # 텍스트 입력창
        tk.Label(self.input_frame, text="변환할 텍스트를 입력하세요:").pack(side=tk.TOP, anchor=tk.W)
        self.text_input = scrolledtext.ScrolledText(self.input_frame, height=5, wrap=tk.WORD,
                                                     font=('맑은 고딕', 10), bd=1, relief="solid")
        self.text_input.pack(fill=tk.X, pady=(0, 5))

        # 음성 선택 및 버튼 프레임
        self.controls_frame = tk.Frame(self.input_frame)
        self.controls_frame.pack(fill=tk.X, pady=(0, 5))

        # 음성 선택 드롭다운
        tk.Label(self.controls_frame, text="목소리 선택:").pack(side=tk.LEFT, padx=(0, 5))
        self.voice_combobox = ttk.Combobox(self.controls_frame, state="readonly", width=30)
        self.voice_combobox.pack(side=tk.LEFT, padx=(0, 10))
        self.voice_combobox.set("ko-KR-Wavenet-A") # 기본값 설정

        # 버튼들
        self.synthesize_button = tk.Button(self.controls_frame, text="변환 및 재생", state='disabled')
        self.synthesize_button.pack(side=tk.LEFT, padx=(0, 5))

        self.list_voices_button = tk.Button(self.controls_frame, text="음성 목록 가져오기")
        self.list_voices_button.pack(side=tk.LEFT)

        # 2. 메시지 표시 영역 (중간)
        self.message_frame = tk.Frame(master, bd=2, relief="groove", padx=5, pady=5)
        self.message_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=(0, 5), padx=10)

        tk.Label(self.message_frame, text="현재 상태 메시지:").pack(side=tk.TOP, anchor=tk.W)
        self.message_display = tk.Text(self.message_frame, height=2, state='disabled', wrap=tk.WORD,
                                       font=('맑은 고딕', 10), bg='lightgray', fg='blue')
        self.message_display.pack(fill=tk.BOTH, expand=True)

        # 3. 로그 표시 영역 (하단)
        self.log_frame = tk.Frame(master, bd=2, relief="groove", padx=5, pady=5)
        self.log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(5, 10), padx=10)

        tk.Label(self.log_frame, text="애플리케이션 로그:").pack(side=tk.TOP, anchor=tk.W)
        self.log_display = scrolledtext.ScrolledText(self.log_frame, height=10, state='disabled', wrap=tk.WORD,
                                                     font=('맑은 고딕', 9), bg='white', fg='black')
        self.log_display.pack(fill=tk.BOTH, expand=True)

    def display_message(self, message):
        """
        GUI의 상태 메시지 영역에 메시지를 표시합니다.
        """
        self.message_display.config(state='normal')
        self.message_display.delete(1.0, tk.END)
        self.message_display.insert(tk.END, message)
        self.message_display.config(state='disabled')

    def display_log(self, message, is_error=False):
        """
        GUI의 로그 영역에 메시지 또는 오류를 기록합니다.
        """
        self.log_display.config(state='normal')
        if is_error:
            self.log_display.tag_config('error', foreground='red')
            self.log_display.insert(tk.END, f"오류: {message}\n", 'error')
        else:
            self.log_display.insert(tk.END, f"{message}\n")
        self.log_display.see(tk.END)
        self.log_display.config(state='disabled')

    def display_voices(self, voices):
        """
        사용 가능한 음성 목록을 콤보박스와 로그 영역에 표시합니다.
        """
        voice_names = [v.name for v in voices]
        self.voice_combobox['values'] = voice_names
        # 음성 목록 로드 후 변환 버튼 활성화
        self.synthesize_button['state'] = 'normal'

        self.display_log("\n사용 가능한 음성 목록:")
        self.display_log("-----------------------------------")
        for voice in voices:
            self.display_log(f"이름: {voice.name}")
            self.display_log(f"지원 언어: {', '.join(voice.language_codes)}")
            self.display_log(f"성별: {voice.ssml_gender.name}\n")

    def get_text_input(self):
        """
        텍스트 입력창의 내용을 가져옵니다.
        """
        return self.text_input.get("1.0", tk.END).strip()

    def get_selected_voice(self):
        """
        콤보박스에서 선택된 목소리 이름을 가져옵니다.
        """
        return self.voice_combobox.get()
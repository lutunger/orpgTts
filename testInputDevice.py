import pyaudio

p = pyaudio.PyAudio()  # PyAudio 인스턴스 생성 [2, 3]

input_devices = []
output_devices = []

for i in range(p.get_device_count()):  # 전체 장치 수만큼 반복 [4]
    info = p.get_device_info_by_index(i)  # 각 장치의 정보 가져오기 [5]

    # 'maxInputChannels'와 'maxOutputChannels' 키가 있다고 가정합니다 (소스에서 직접 명시되지는 않았지만, PaDeviceInfo 구조의 일반적인 키입니다).

    # 입력 장치 확인
    if info.get('maxInputChannels') > 0:
        input_devices.append({
            'index': i,
            'name': info.get('name'),
            'hostApi': p.get_host_api_info_by_index(info.get('hostApi'))['name']
        })

    # 출력 장치 확인
    if info.get('maxOutputChannels') > 0:
        output_devices.append({
            'index': i,
            'name': info.get('name'),
            'hostApi': p.get_host_api_info_by_index(info.get('hostApi'))['name']
        })

p.terminate()  # PyAudio 리소스 해제 [3, 7]

print("--- 현재 사용 가능한 입력 장치 목록 ---")
if input_devices:
    for device in input_devices:
        print(f"  인덱스: {device['index']}, 이름: {device['name']}, 호스트 API: {device['hostApi']}")
else:
    print("  입력 가능한 오디오 장치를 찾을 수 없습니다.")

print("\n--- 현재 사용 가능한 출력 장치 목록 ---")
if output_devices:
    for device in output_devices:
        print(f"  인덱스: {device['index']}, 이름: {device['name']}, 호스트 API: {device['hostApi']}")
else:
    print("  출력 가능한 오디오 장치를 찾을 수 없습니다.")
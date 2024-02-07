import os
import shutil

# 기본 경로 설정
base_path = "./../lstm_data/train_30ea"

# 새로운 폴더들을 만들 경로
new_folders = ["open_hand", "folding_hand", "closed_hand", "releasing_hand"]

# 새로운 폴더 생성
for folder in new_folders:
    new_folder_path = os.path.join(base_path, folder)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path, exist_ok=True)

# 각 video 폴더에 대한 처리
for i in range(180): # video00부터 video309까지
    video_folder = f"video{i:02d}"
    video_folder_path = os.path.join(base_path, video_folder)
    
    # 해당 폴더의 모든 파일 목록을 가져와 "image_"로 시작하는 파일만 필터링
    image_files = [file for file in os.listdir(video_folder_path) if file.startswith("image_")]
    image_files.sort() # 파일 이름을 정렬
    
    # 각 폴더에 대한 이미지 인덱스 초기화
    image_index = i * 10 # 각 폴더마다 10개의 이미지 생성
    
    # "open_hand" 폴더 작업: 가장 작은 인덱스의 이미지 파일 찾기 및 복사
    smallest_image_file = image_files[0]
    source_image_path = os.path.join(video_folder_path, smallest_image_file)
    for _ in range(10):
        new_image_name = f"image_{image_index:04d}.jpg"
        new_image_path = os.path.join(base_path, "open_hand", new_image_name)
        shutil.copy(source_image_path, new_image_path)
        image_index += 1
    
    # "folding_hand" 폴더 작업: 파일 복사 및 이름 변경
    image_index = i * len(image_files) # 각 폴더마다 이미지 파일 개수에 따라 인덱스 설정
    for image_file in image_files:
        source_image_path = os.path.join(video_folder_path, image_file)
        new_image_name = f"image_{image_index:04d}.jpg"
        new_image_path = os.path.join(base_path, "folding_hand", new_image_name)
        shutil.copy(source_image_path, new_image_path)
        image_index += 1
        
    # "closed_hand" 폴더 작업: 가장 큰 인덱스의 이미지 복사
    image_index = i * 10 # 각 폴더마다 10개의 이미지 생성
    largest_image_file = image_files[-1]
    source_image_path = os.path.join(video_folder_path, largest_image_file)
    for _ in range(10):
        new_image_name = f"image_{image_index:04d}.jpg"
        new_image_path = os.path.join(base_path, "closed_hand", new_image_name)
        shutil.copy(source_image_path, new_image_path)
        image_index += 1
        
    # "releasing_hand" 폴더 작업: 파일 역순으로 복사 및 이름 변경
    image_index = i * len(image_files) 
    for image_file in reversed(image_files):
        source_image_path = os.path.join(video_folder_path, image_file)
        new_image_name = f"image_{image_index:04d}.jpg"
        new_image_path = os.path.join(base_path, "releasing_hand", new_image_name)
        shutil.copy(source_image_path, new_image_path)
        image_index += 1
    
# 성공적으로 완료 시
print("성공적으로 실행되었습니다.")
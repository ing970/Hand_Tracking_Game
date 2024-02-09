import os
import glob
import shutil

def copy_and_rename_images(directory, start_num=0, ext='*.jpg'):
    # 새로운 파일 저장 경로
    target_directory = os.path.join(directory, '../images')

    # 경로 내 확장자명이 일치하는 파일 찾기
    file_paths = glob.glob(os.path.join(directory, ext))

    # 파일 정렬
    file_paths.sort()

    # 새 디렉토리 생성 (부재 시)
    os.makedirs(target_directory, exist_ok=True)

    # 파일 이름 변경 후 저장
    for i, file_path in enumerate(file_paths, start=start_num):
        # 3자리 단위로 파일명 변경 (e.g., "image_005.jpeg")
        new_file_name = f"Images_{i:04}.jpg"
        new_file_path = os.path.join(target_directory, new_file_name)

        # 파일 복사
        shutil.copy(file_path, new_file_path)
        print(f"Copied and renamed '{file_path}' to '{new_file_path}'")

# 코드 실행
source_directory = '../video0/'  # 디렉토리 변경
copy_and_rename_images(source_directory, start_num=1000)  # 인덱스 시작값(start_num) 변경
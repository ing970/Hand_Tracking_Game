
# Game settings and related variables
import pygame, cv2, time, os, random, librosa, sys, math, torch
import mediapipe as mp
import torch.nn as nn

# version 정보
__version__ = '1.0.0'

# pygame moduel을 import하고 초기화한다.
pygame.init()

# 창 정보와 관련된 변수를 정의한다.
w = 1000
h = w * (9 / 16)

# 코드 최적화를 위해 나누기 변수를 정의한다.
height_division = h / 12
width_division = w / 45
a3 = 4 / 10
a4 = 8 / 10
a5 = h / 900
a6 = w * (1 / 2)
a7 = w / 32
a8 = h / 30
a9 = h / 35
height_division0 = h / 50
height_division1 = h / 24 
height_division2 = h / 100
height_division3 = w / 20
height_division4 = w / 30
height_division5 = h / 2
height_division6 = int(w / 14)
height_division7 = int(h / 20)
height_division8 = int(h / 10)

# lane 좌표를 설정한다.
width1 = w*(1/2) - w*a3
width2 = w*(1/2) - w*(2/10)
width3 = w*(1/2)
width4 = w*(1/2) + w*(2/10)
width5 = w*(1/2) + w*a3

# 색깔과 관련된 변수를 정의한다.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)

# screen instance를 생성한다.
screen = pygame.display.set_mode((w, h))

# 게임 내에서 시간을 측정하기 위해 instance를 생성한다.
clock = pygame.time.Clock()

# hand detection instance를 생성한다.
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# hand detection을 위해 cam을 딴다.
cam = cv2.VideoCapture(1) # mac User.
# cam = cv2.VideoCapture(0) # Window User.

# frame을 설정한다.
maxframe = 60
fps = 0

# path ==========================================================================================
# current 경로를 설정한다.
Cpath = os.path.dirname(__file__)
# font 경로를 설정한다.
Fpath = os.path.join(Cpath, 'font')
# music 경로를 설정한다.
Mpath = os.path.join(Cpath, 'music')
# image 경로를 설정한다.
Ipath = os.path.join(Cpath, 'image')
# ===============================================================================================

# font ==========================================================================================
# 시작할 때 게임 화면에 띄울 문자열을 생성한다.
font_file = os.path.join(Fpath, 'retro_game_font.ttf')
ingame_font_rate = pygame.font.Font(font_file, int(height_division4))
rate = 'START'
# 가져온 font로 렌더링한다.
rate_text = ingame_font_rate.render(str(rate), False, WHITE)
# ===============================================================================================

# image =========================================================================================
# outro에서 띄울 image path를 설정한다.
quit_path = os.path.join(Ipath, 'quit.png')
restart_path = os.path.join(Ipath, 'restart.png')
# ===============================================================================================

# note가 떨어지는 속도를 설정한다.
speed = 1

# lane이 4개이므로 note와 관련되 정보를 담을 list 4개를 생성한다.
# [ty, tst]가 하나의 element로 들어간다.
t1, t2, t3, t4 = [], [], [], []

# spark 효과를 담을 list를 정의한다.
sparks = []

# 키 누름을 감지하는 list를 정의한다.
lanes = [0, 0, 0, 0]
laneset = [0, 0, 0, 0]

# effect를 주기 위한 변수를 정의한다.
combo = 0
combo_effect = 0
combo_effect2 = 0
miss_anim = 0
last_combo = 0

# outro ========================================================================================
# outro에서 점수 계산을 위한 변수를 정의한다.
excellent_cnt = 0     # 10 점
perfect_cnt = 0       # 5 점
bad_cnt = 0           # 3 점
miss_cnt = 0          # 0 점
# ===============================================================================================

# life ==========================================================================================
# 게임을 종료시키기 위한 변수와 life image를 load한다.
l = int(w / 25)
life_cnt = 5
life_img_path = os.path.join(Ipath, 'heart.png')
life_img = pygame.image.load(life_img_path)
life_img = pygame.transform.scale(life_img, (l, l))
# ===============================================================================================

# song ==========================================================================================
# 노래 file을 불러온다.
song_file = os.path.join(Mpath, 'short_canon.wav')

# beat를 생성한다.
audio, _ = librosa.load(song_file)
sampling_rate = 44100
tempo, beats = librosa.beat.beat_track(y = audio, sr = sampling_rate)

# beat가 찍혀야 하는 시간을 담고 있는 list를 생성한다.
beat_times = librosa.frames_to_time(beats)
beat_times = list(beat_times)
beat_times = beat_times[5:]

# pygame에 노래 file을 불러온다.
pygame.mixer.music.load(song_file)

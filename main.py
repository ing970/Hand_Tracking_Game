
from settings import *
from utils import generate_notes, simultaneous_notes
from game_functions import main_game, start_game, end_game, game_over, rating
from model import HandStateNN, model

if __name__ == "__main__":
    # 각 lane에 note를 생성한다.
    generate_notes(beat_times, t1, t2, t3, t4)
    simultaneous_notes(beat_times, t1, t2, t3, t4)
    start_game()
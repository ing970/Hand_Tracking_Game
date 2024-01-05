
from settings import *
from utils import generate_notes, simultaneous_notes
from game_functions import game, start_game, end_game, game_over, rating
from model import HandStateNN, model

if __name__ == "__main__":
    # 각 lane에 note를 생성한다.
    generate_notes()
    simultaneous_notes()
    start_game()

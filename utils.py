from settings import random

# Utility functions for the game
# note를 생성하는 함수를 정의한다.
def generate_notes(beat_times, t1, t2, t3, t4):
    '''
    각 lane에 생성되는 note를 생성하는 함수이다. note의 정보를 [ty, tst]로 입력한다.
        - ty는 note의 위치이고 tst는 note가 생성되어야 하는 시간이다.
    [parameter]
        None
    [return]
        None
    '''
    idx = 0
    while True:
        # idx가 beat_times의 끝에 도달하면 종료한다.
        if idx == len(beat_times):
                break
        
        # note를 생성할 lane을 random하게 추출한다.
        lane = random.randint(1, 4)

        if lane == 1:
            ty = 0
            tst = beat_times[idx]
            t1.append([ty, tst])
            idx += 1
            continue
        elif lane == 2:
            ty = 0
            tst = beat_times[idx]
            t2.append([ty, tst])
            idx += 1
            continue
        elif lane == 3:
            ty = 0
            tst = beat_times[idx]
            t3.append([ty, tst])
            idx += 1
            continue
        elif lane == 4:
            ty = 0
            tst = beat_times[idx]
            t4.append([ty, tst])
            idx += 1
            continue

# note가 한 번에 여러 개 떨어지도록 하는 함수를 정의한다.
def simultaneous_notes(beat_times, t1, t2, t3, t4):
    '''
    note가 한 번에 여러 개 떨어지도록 만드는 함수이다. 한 번에 떨어지는 note 개수의 기본값은 2이다.
    [parameter]
        None
    [return]
        None
    '''
    # 전체 beat의 수를 정의한다.
    total_beat = len(beat_times)

    # 1부터 total_beat // 2까지의 정수 중 하나를 random하게 추출해 sample 수로 설정한다.
    sample = random.randint(total_beat // 4, total_beat // 2)

    sample_beat_times = random.sample(beat_times, sample)

    idx = 0
    while True:
        if idx == len(sample_beat_times):
            break

        lane = random.randint(1, 4)

        if lane == 1:
            ty = 0
            tst = sample_beat_times[idx]
            t1.append([ty, tst])
            idx += 1
            continue
        elif lane == 2:
            ty = 0
            tst = sample_beat_times[idx]
            t2.append([ty, tst])
            idx += 1
            continue
        elif lane == 3:
            ty = 0
            tst = sample_beat_times[idx]
            t3.append([ty, tst])
            idx += 1
            continue
        elif lane == 4:
            ty = 0
            tst = sample_beat_times[idx]
            t4.append([ty, tst])
            idx += 1
            continue
    t1 = list(set([tuple(item) for item in t1]))
    t1 = list(list(item) for item in t1)

    t2 = list(set([tuple(item) for item in t2]))
    t2 = list(list(item) for item in t2)

    t3 = list(set([tuple(item) for item in t3]))
    t3 = list(list(item) for item in t3)

    t4 = list(set([tuple(item) for item in t4]))
    t4 = list(list(item) for item in t4)

    t1.sort()
    t2.sort()
    t3.sort()
    t4.sort()
from settings import *
from utils import *
from model import model

# Core game logic and functions
# Spark VFX class를 선언한다.
class Spark():
    def __init__(self, loc, angle, speed, color, scale = 1):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True

    def point_towards(self, angle, rate):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sing = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]


    # 중력과 마찰 기능을 추가한다.
    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])
        # 더 현실적이 되고 싶다면, 여기서 속도를 조절해야 한다.

    def move(self, dt):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        # 각도와 관련된 많은 옵션들을 가지고 놀 수 있습니다.
        self.point_towards(math.pi / 2, 0.02)
        self.velocity_adjust(0.975, 0.2, 8, dt)
        # self.angle += 0.1

        self.speed -= 0.1

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf, offset=[0, 0]):
        if self.alive:
            points = [
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale, self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5, self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                ]
            pygame.draw.polygon(surf, self.color, points)
            
            
# rate_data를 저장하는 리스트
rate_data = [0, 0, 0, 0]

# 점수를 판정하는 함수를 만든다.
def rating(n):
    '''
    각 lane에 combo와 'BAD', 'PERFECT', 'EXCELLENT' 문자를 띄우는 함수이다.
    [parameter]
        n: int - lane 번호를 설정한다.
    [return]
        None
    '''
    global Time, combo, miss_anim, last_combo, combo_effect, combo_effect2, combo_time, rate, bad_cnt, perfect_cnt, excellent_cnt
    
    # rate_data의 n번째 note들의 정보를 가져와 판단한다.
    if abs(height_division*9 - rate_data[n-1] < 950*speed*(h/900)) and abs(height_division*9 - rate_data[n-1] >= 200*speed*(h/900)):
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        bad_cnt += 1
        rate = 'BAD'
    elif abs(height_division*9 - rate_data[n-1]) < 200*speed*(h/900) and abs(height_division*9 - rate_data[n-1]) >= 100*speed*(h/900):
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        perfect_cnt += 1
        rate = 'PERFECT'
    elif abs(height_division*9 - rate_data[n-1]) < 100*speed*(h/900) and abs(height_division*9 - rate_data[n-1]) >= 0*speed*(h/900):
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        excellent_cnt += 1
        rate = 'EXCELLENT'

# game을 실행하는 메인 함수를 정의한다.
def game():
    global gst, Time, combo, miss_anim, last_combo, combo_effect, combo_effect2, combo_time, rate, speed, t1, t2, t3, t4, miss_cnt, life_cnt
    
    # 시간 측정을 위해 게임이 플레이 되는 시간을 구하고 combo_time을 다시 계산한다.
    gst = time.time()
    Time = time.time() - gst
    combo_time = Time + 1
    
    # 노래 file을 재생한다.
    pygame.mixer.music.play()
    
    main = True
    while main:
        # 이벤트 감지 코드를 작성한다.
        for event in pygame.event.get():
            # 창을 나가는 동작을 감지한다.
            if event.type == pygame.QUIT:
                # 창을 지운다.
                main = False

        # 웹캠 이미지를 읽어온다.
        _, img = cam.read()
        # 좌우 반전 
        image = cv2.flip(img, 1)
        results = hands.process(image)

        if len(t1) > 0:
            rate_data[0] = t1[0][0]
        if len(t2) > 0:
            rate_data[1] = t2[0][0]
        if len(t3) > 0:
            rate_data[2] = t3[0][0]
        if len(t4) > 0:
            rate_data[3] = t4[0][0]

        # 게임이 시작되고 나서부터의 시간을 측정한다.
        Time = time.time() - gst

        # combo 글씨 생성
        ingame_font_combo = pygame.font.Font(font_file, int((width_division) * combo_effect2))
        combo_text = ingame_font_combo.render(str(combo), False, WHITE)

        # 점수 글씨 생성
        rate_text = ingame_font_rate.render(str(rate), False, WHITE)
        rate_text = pygame.transform.scale(rate_text, (int(w / 110 * len(rate) * combo_effect2), int((w * (1 / 60) * combo_effect * combo_effect2))))

        # miss 글씨 생성
        ingame_font_miss = pygame.font.Font(font_file, int((width_division * miss_anim)))
        miss_text = ingame_font_miss.render(str(last_combo), False, (255, 0, 0))

        fps = clock.get_fps()
        if fps == 0:
            fps = maxframe   

    # gear ========================================================================================
        # 화면을 그린다. 단색으로 채운다.
        screen.fill(BLACK)

        # effect가 생기는 정도를 결정한다. effect가 생기고 사라지는 속도를 조절하고 싶으면 1을 바꾼다.
        # 숫자를 크게 하면 effect가 천천히 생기고 천천히 사라진다.
        lanes[0] += (laneset[0] - lanes[0]) / (1 * (maxframe / fps))
        lanes[1] += (laneset[1] - lanes[1]) / (1 * (maxframe / fps))
        lanes[2] += (laneset[2] - lanes[2]) / (1 * (maxframe / fps))
        lanes[3] += (laneset[3] - lanes[3]) / (1 * (maxframe / fps))

    # effect =======================================================================================
        # effect의 움직임을 결정한다.
        if Time > combo_time:
            combo_effect += (0 - combo_effect) / (1 * (maxframe / fps))
        if Time < combo_time:
            combo_effect += (1 - combo_effect) / (1 * (maxframe / fps))

        combo_effect2 += (2 - combo_effect2) / (1 * (maxframe / fps))

        miss_anim += (4 - miss_anim) / (14 * (maxframe / fps))

    # effect ===================================================================================
        # gear background
        pygame.draw.rect(screen, BLACK, (w*(1/2) - w*a3, -int(w/100), w*a4, h + int(w * (1 / 50))))

        # lane를 눌렀을 때 lane에 생기는 effect를 만든다.
        for i in range(7):
            i += 1
            pygame.draw.rect(screen, (200-((200*(1/7))*i), 200-((200*(1/7))*i), 200-((200*(1/7))*i)), (w*(1/2) - w*a3 + w/32 - a7 * lanes[0], height_division*9 - a8 * lanes[0] * i, w*(2/10) * lanes[0], a9 * (1 / i)))
        for i in range(7):
            i += 1
            pygame.draw.rect(screen, (200-((200*(1/7))*i), 200-((200*(1/7))*i), 200-((200*(1/7))*i)), (w*(1/2) - w*(2/10) + w/32 - a7 * lanes[1], height_division*9 - a8 * lanes[1] * i, w*(2/10) * lanes[1], a9 * (1 / i)))
        for i in range(7):
            i += 1
            pygame.draw.rect(screen, (200-((200*(1/7))*i), 200-((200*(1/7))*i), 200-((200*(1/7))*i)), (w*(1/2)            + w/32 - a7 * lanes[2], height_division*9 - a8 * lanes[2] * i, w*(2/10) * lanes[2], a9 * (1 / i)))
        for i in range(7):
            i += 1
            pygame.draw.rect(screen, (200-((200*(1/7))*i), 200-((200*(1/7))*i), 200-((200*(1/7))*i)), (w*(1/2) + w*(2/10) + w/32 - a7 * lanes[3], height_division*9 - a8 * lanes[3] * i, w*(2/10) * lanes[3], a9 * (1 / i)))

        # gear line
        pygame.draw.rect(screen, WHITE, (w*(1/2) - w*a3, -int(w * (1/100)), w*a4, h + int(w * (1/50))), int(w * (1/200)))

    # note =========================================================================================
        # note를 만든다.
        for tile_data in t1:
            # 렉이 걸려도 노트는 일정한 속도로 내려오도록 하는 코드를 작성한다.
            # 판정선 위치 기준             현재 시간 - 노트 소환 시간
            #                             시간이 경과할수록 이 부분의 차가 커져 노트가 내려간다.
            tile_data[0] = height_division * 9 + (Time - tile_data[1]) * speed * 350 * (a5)
            pygame.draw.rect(screen, WHITE, (w*(1/2) - w*a3, tile_data[0] - height_division2, w*(2/10), height_division0))
            # 놓친 노트는 없앤다.

            if tile_data[0] > h - (h / 9):
                # 미스 판정을 만든다. 놓치면 해당 노트를 삭제한다.
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                miss_cnt += 1
                life_cnt -= 1
                rate = 'MISS'
                t1.remove(tile_data)

        for tile_data in t2:
            tile_data[0] = height_division * 9 + (Time - tile_data[1]) * 350 * speed * (a5)
            pygame.draw.rect(screen, WHITE, (w*(1/2) - w*(2/10), tile_data[0] - height_division2, w*(2/10), height_division0))
            if tile_data[0] > h - (h / 9):
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                miss_cnt += 1
                life_cnt -= 1
                rate = 'MISS'
                t2.remove(tile_data)

        for tile_data in t3:
            tile_data[0] = height_division * 9 + (Time - tile_data[1]) * 350 * speed * (a5)
            pygame.draw.rect(screen, WHITE, (w*(1/2), tile_data[0] - height_division2, w*(2/10), height_division0))
            if tile_data[0] > h - (h / 9):
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                miss_cnt += 1
                life_cnt -= 1
                rate = 'MISS'
                t3.remove(tile_data)

        for tile_data in t4:
            tile_data[0] = height_division * 9 + (Time - tile_data[1]) * 350 * speed * (a5)
            pygame.draw.rect(screen, WHITE, (w*(1/2) + w*(2/10), tile_data[0] - height_division2, w*(2/10), height_division0))
            if tile_data[0] > h - (h / 9):
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                miss_cnt += 1
                life_cnt -= 1
                rate = 'MISS'
                t4.remove(tile_data)

    # blinder =============================================================================================
        # 판정선을 그린다.
        pygame.draw.rect(screen, BLACK, (w*(1/2) - w*a3, height_division * 9, w*a4, h * (1/2)))
        pygame.draw.rect(screen, WHITE, (w*(1/2) - w*a3, height_division * 9, w*a4, h * (1/2)), int(height_division2))

    # background ==========================================================================================
        # 배경 화면에 생성될 버튼을 만든다.
        pygame.draw.circle(screen, (255 - 100 * lanes[0], 255 - 100 * lanes[0], 255 - 100 * lanes[0]), (w*(1/2) - w*(3/10), (height_division1) * 21 + height_division0 * lanes[0]), (height_division3), int(height_division2))
        pygame.draw.circle(screen, (255 - 100 * lanes[0], 255 - 100 * lanes[0], 255 - 100 * lanes[0]), (w*(1/2) - w*(3/10), (height_division1) * 21 + height_division0 * lanes[0]), (height_division4))

        pygame.draw.circle(screen, (255 - 100 * lanes[1], 255 - 100 * lanes[1], 255 - 100 * lanes[1]), (w*(1/2) - w*(1/10), (height_division1) * 21 + height_division0 * lanes[1]), (height_division3), int(height_division2))
        pygame.draw.circle(screen, (255 - 100 * lanes[1], 255 - 100 * lanes[1], 255 - 100 * lanes[1]), (w*(1/2) - w*(1/10), (height_division1) * 21 + height_division0 * lanes[1]), (height_division4))

        pygame.draw.circle(screen, (255 - 100 * lanes[2], 255 - 100 * lanes[2], 255 - 100 * lanes[2]), (w*(1/2) + w*(1/10), (height_division1) * 21 + height_division0 * lanes[2]), (height_division3), int(height_division2))
        pygame.draw.circle(screen, (255 - 100 * lanes[2], 255 - 100 * lanes[2], 255 - 100 * lanes[2]), (w*(1/2) + w*(1/10), (height_division1) * 21 + height_division0 * lanes[2]), (height_division4))

        pygame.draw.circle(screen, (255 - 100 * lanes[3], 255 - 100 * lanes[3], 255 - 100 * lanes[3]), (w*(1/2) + w*(3/10), (height_division1) * 21 + height_division0 * lanes[3]), (height_division3), int(height_division2))
        pygame.draw.circle(screen, (255 - 100 * lanes[3], 255 - 100 * lanes[3], 255 - 100 * lanes[3]), (w*(1/2) + w*(3/10), (height_division1) * 21 + height_division0 * lanes[3]), (height_division4))

        # 글씨를 화면에 띄운다.
        miss_text.set_alpha(255 - (255 / 4) * miss_anim)
        screen.blit(combo_text, (w*(1/2) - combo_text.get_width() * (1/2), height_division * 4 - combo_text.get_height() * (1/2)))
        screen.blit(rate_text, (w*(1/2) - rate_text.get_width() * (1/2), height_division * 8 - rate_text.get_height() * (1/2)))
        screen.blit(miss_text, (w*(1/2) - miss_text.get_width() * (1/2), height_division * 8 - miss_text.get_height() * (1/2)))

        # 남은 life의 개수를 이용해 life 문구를 띄운다.
        if life_cnt == 5:
            for i in range(life_cnt):
                screen.blit(life_img, (w - height_division6, height_division7 + height_division8*i))
        elif life_cnt == 4:
            for i in range(life_cnt):
                screen.blit(life_img, (w - height_division6, height_division7 + height_division8*i))
        elif life_cnt == 3:
            for i in range(life_cnt):
                screen.blit(life_img, (w - height_division6, height_division7 + height_division8*i))
        elif life_cnt == 2:
            for i in range(life_cnt):
                screen.blit(life_img, (w - height_division6, height_division7 + height_division8*i))
        elif life_cnt == 1:
            for i in range(life_cnt):
                screen.blit(life_img, (w - height_division6, height_division7 + height_division8*i))
        # 남은 life가 0이 되면 게임 오버 창으로 넘어간다. 노래를 종료하고 각 lane의 note를 초기화한다.
        else:
            main = False
            pygame.mixer.music.stop()
            t1, t2, t3, t4 = [], [], [], []
            game_over()

    # hand dtection =======================================================================================
        # hand detection과 hand tracking을 구현한다.
        grab_TF = [2, 2] # left, right
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                palm_x, palm_y = hand_landmarks.landmark[9].x*w, hand_landmarks.landmark[9].y*h
                _, finger_y = hand_landmarks.landmark[12].x*w, hand_landmarks.landmark[12].y*h

                if grab_TF[0] == 2:
                    if finger_y > palm_y:
                        grab_TF[0] = True
                        if width1 <= palm_x and palm_x <= width2:
                            laneset[0] = 1
                        if width2 <= palm_x and palm_x <= width3:
                            laneset[1] = 1
                        if width3 <= palm_x and palm_x <= width4:
                            laneset[2] = 1
                        if width4 <= palm_x and palm_x <= width5:
                            laneset[3] = 1
                    else:
                        grab_TF[0] = False
                elif grab_TF[1] == 2:
                    if finger_y > palm_y:
                        grab_TF[1] = True
                        if width1 <= palm_x and palm_x <= width2:
                            laneset[0] = 1
                        if width2 <= palm_x and palm_x <= width3:
                            laneset[1] = 1
                        if width3 <= palm_x and palm_x <= width4:
                            laneset[2] = 1
                        if width4 <= palm_x and palm_x <= width5:
                            laneset[3] = 1
                    else:
                        grab_TF[1] = False

                pygame.draw.circle(screen, GREEN, (int(palm_x), int(palm_y)), 15)
                if grab_TF[0] == True or grab_TF[1] == True:
                    # lane 1
                    if laneset[0] == 1:
                        if len(t1) > 0:
                            if t1[0][0] > height_division5:
                                rating(1)
                                del t1[0]

                    # lane 2
                    if laneset[1] == 1:
                        if len(t2) > 0:
                            if t2[0][0] > height_division5:
                                rating(2)
                                del t2[0]

                    # lane 3
                    if laneset[2] == 1:
                        if len(t3) > 0:
                            if t3[0][0] > height_division5:
                                rating(3)
                                del t3[0]

                    # lane 4
                    if laneset[3] == 1:
                        if len(t4) > 0:
                            if t4[0][0] > height_division5:
                                rating(4)
                                del t4[0]
                else:
                    laneset[0], laneset[1], laneset[2], laneset[3] = 0, 0, 0, 0
        else:
            laneset[0], laneset[1], laneset[2], laneset[3] = 0, 0, 0, 0
    
    # outro ===================================================================================
        if not pygame.mixer.music.get_busy():
            main = False
            end_game()

    # update ===================================================================================
        # 화면을 업데이트한다. 이 코드가 없으면 화면이 보이지 않는다.
        pygame.display.flip()

        # frame 제한 코드
        clock.tick(maxframe)
    cam.release()
    
# 게임의 intro를 만드는 함수를 정의한다.
def start_game():

    # intro 화면에 띄울 문구를 작성한다.
    intro_font_name = pygame.font.Font(font_file, 80)
    intro_font_start = pygame.font.Font(font_file, 50)
    intro_font_info = pygame.font.Font(font_file, 30)

    game_name_txt_render_1 = intro_font_name.render('ZAM ZAM', True, WHITE)
    game_name_txt_render_2 = intro_font_name.render('CIRCULATION', True, WHITE)
    start_box_txt_render = intro_font_start.render('START GAME', True, WHITE)
    info_txt_render = intro_font_info.render("CLICK THE BUTTON TO START", True, WHITE)
    start_box = pygame.Rect(w // 2 - 195, h // 2 + 50, 393, 70)
    
    # intro 실행.
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
                sys.exit()

        # 웹캠 이미지를 읽어온다.
        _, img = cam.read()
        # 좌우 반전 
        image = cv2.flip(img, 1)
        results = hands.process(image)

        # intro 화면을 띄운다.
        screen.fill(BLACK) 
        screen.blit(game_name_txt_render_1, (300, 70))
        screen.blit(game_name_txt_render_2, (170, 150))
        screen.blit(start_box_txt_render, (start_box.x + 10, start_box.y +5))
        screen.blit(info_txt_render, (230, 470))
        pygame.draw.rect(screen, WHITE, start_box, 4)

        # Spark VFX 효과를 일으킨다.
        for i, spark in sorted(enumerate(sparks), reverse=True):
            spark.move(1)
            spark.draw(screen)
            if not spark.alive:
                sparks.pop(i)
                
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 랜드마크 추출 및 전처리
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                landmarks = torch.tensor(landmarks).flatten().unsqueeze(0)

                # 모델 예측
                with torch.no_grad():
                    preds = model(landmarks)
                    _, predicted = torch.max(preds.data, 1)

                # 손의 상태 확인
                is_closed = predicted.item() in [1, 3]

                palm_x, palm_y = hand_landmarks.landmark[9].x * w, hand_landmarks.landmark[9].y * h

                pygame.draw.circle(screen, (0, 255, 0), (int(palm_x), int(palm_y)), 10)

                if is_closed:
                    # 주먹을 쥐었을 때 spark 생성
                    for i in range(10):
                        sparks.append(Spark([int(palm_x), int(palm_y)], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 2))

                    # 게임 시작 조건
                    if start_box.collidepoint(int(palm_x), int(palm_y)):
                        game()
                         
        pygame.display.flip()
        clock.tick(maxframe)
    cam.release()

# 게임의 outro를 만드는 함수를 정의한다.
def end_game():
    global gst, Time, excellent_cnt, perfect_cnt, bad_cnt, miss_cnt, rate, combo, combo_effect, combo_effect2, miss_anim, last_combo, life_cnt

    # outro에서 사용할 font의 크기 및 위치를 변수로 정의한다.
    o1 = w / 25
    o2 = w / 35
    o3 = w / 30
    o4 = h * (1/10)

    # outro에서 띄울 총점을 계산한다.
    total_point = (excellent_cnt * 10) + (perfect_cnt * 5) + (bad_cnt * 3)

    # outro 화면에 띄울 문구를 작성한다.
    ingame_font_end = pygame.font.Font(font_file, int(o1))
    ingame_font_point = pygame.font.Font(font_file, int(o2))
    ingame_font_total = pygame.font.Font(font_file, int(o3))

    end_txt = 'Games Has Ended'
    excellent_txt = 'EXCELLENT : '
    perfect_txt = 'PERFECT : '
    bad_txt = 'BAD : '
    miss_txt = 'MISS : '
    total_txt = 'TOTAL POINT : '

    # 각 문자열에 개수를 추가한다.
    excellent_txt += str(excellent_cnt)
    perfect_txt += str(perfect_cnt)
    bad_txt += str(bad_cnt)
    miss_txt += str(miss_cnt)
    total_txt += str(total_point)

    # 각 문자열을 렌더링한다.
    end_txt_render = ingame_font_end.render(end_txt, False, WHITE)
    excellent_txt_render = ingame_font_point.render(excellent_txt, False, WHITE)
    perfect_txt_render = ingame_font_point.render(perfect_txt, False, WHITE)
    bad_txt_render = ingame_font_point.render(bad_txt, False, WHITE)
    miss_txt_render = ingame_font_point.render(miss_txt, False, WHITE)
    total_txt_render = ingame_font_total.render(total_txt, False, WHITE)

    # 버튼 이미지를 불러온다.
    quit_img = pygame.image.load(quit_path)
    restart_img = pygame.image.load(restart_path)

    # 이미지 사이즈를 지정한다.
    quit_img = pygame.transform.scale(quit_img, (100, 100))
    restart_img = pygame.transform.scale(restart_img, (100, 100))

    quit_button_box = pygame.Rect(w // 2 + 220, h // 2 - 55,  100, 100)
    restart_button_box = pygame.Rect(w // 2 - 330, h // 2 - 55,  100, 100)

    # outro를 실행한다.
    outro = True
    while outro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                outro = False
                pygame.quit()
                sys.exit()
        
        # 웹캠 이미지를 읽어온다.
        _, img = cam.read()
        # 좌우 반전 
        image = cv2.flip(img, 1)
        results = hands.process(image)
        
        # outro 화면을 띄운다.
        screen.fill(BLACK)
        screen.blit(end_txt_render, (w*(1/2) - end_txt_render.get_width() * (1/2), o4))
        screen.blit(excellent_txt_render, (w*(1/2) - excellent_txt_render.get_width() * (1/2), 3 * o4))
        screen.blit(perfect_txt_render, (w*(1/2) - perfect_txt_render.get_width() * (1/2), 4 * o4))
        screen.blit(bad_txt_render, (w*(1/2) - bad_txt_render.get_width() * (1/2), 5 * o4))
        screen.blit(miss_txt_render, (w*(1/2) - miss_txt_render.get_width() * (1/2), 6 * o4))
        screen.blit(total_txt_render, (w*(1/2) - total_txt_render.get_width() * (1/2), 8 * o4))
        screen.blit(quit_img, (w*(1/2) + 220,  4 * o4))
        screen.blit(restart_img, (w*(1/2) - 330,  4 * o4))
        pygame.draw.rect(screen, BLACK, quit_button_box, 2)
        pygame.draw.rect(screen, BLACK, restart_button_box, 2)

        # Spark VFX 효과를 일으킨다.
        for i, spark in sorted(enumerate(sparks), reverse=True):
            spark.move(1)
            spark.draw(screen)
            if not spark.alive:
                sparks.pop(i)
                
        # hand detection과 hand tracking을 구현한다        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 랜드마크 추출 및 전처리
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                landmarks = torch.tensor(landmarks).flatten().unsqueeze(0)

                # 모델 예측
                with torch.no_grad():
                    preds = model(landmarks)
                    _, predicted = torch.max(preds.data, 1)

                # 손의 상태 확인
                is_closed = predicted.item() in [1, 3]

                palm_x, palm_y = hand_landmarks.landmark[9].x * w, hand_landmarks.landmark[9].y * h

                pygame.draw.circle(screen, (0, 255, 0), (int(palm_x), int(palm_y)), 10)

                if is_closed:
                    # 주먹을 쥐었을때 spark가 일어난다.
                    for i in range(10):
                        sparks.append(Spark([int(palm_x), int(palm_y)], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 2))

                    # 게임을 나간다.
                    if quit_button_box.collidepoint(int(palm_x), int(palm_y)):
                        outro = False
                        pygame.quit()
                        sys.exit()

                    # 초기화를 시키고 게임을 다시 시작한다.
                    if restart_button_box.collidepoint(int(palm_x), int(palm_y)):
                        outro = False
                        rate = 'START'
                        excellent_cnt = 0     
                        perfect_cnt = 0       
                        bad_cnt = 0           
                        miss_cnt = 0 
                        combo = 0
                        combo_effect = 0
                        combo_effect2 = 0
                        miss_anim = 0
                        last_combo = 0
                        life_cnt = 5
                        generate_notes()
                        simultaneous_notes()      
                        game()

        pygame.display.flip()

# 게임이 종료되었을 때 뜨는 창을 만드는 함수를 정의한다.
def game_over():
    global gst, Time, excellent_cnt, perfect_cnt, bad_cnt, miss_cnt, rate, combo, combo_effect, combo_effect2, miss_anim, last_combo, life_cnt

    o1 = 1 / 2
    o2 = h / 10

    # 게임 오버되었을 때 창에 띄울 문자를 생성한다.
    ingame_font_over = pygame.font.Font(font_file, int(w / 20))
    over_txt = 'Game Over'
    over_txt_render = ingame_font_over.render(over_txt, False, WHITE)

    # 버튼 이미지를 불러온다.
    quit_img = pygame.image.load(quit_path)
    restart_img = pygame.image.load(restart_path)

    # 이미지 사이즈를 지정한다.
    quit_img = pygame.transform.scale(quit_img, (100, 100))
    restart_img = pygame.transform.scale(restart_img, (100, 100))
    quit_button_box = pygame.Rect(w // 2 + 220, h // 2 - 55,  100, 100)
    restart_button_box = pygame.Rect(w // 2 - 330, h // 2 - 55,  100, 100)

    # 게임이 종료되었을 때 실행되는 창을 띄운다.
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = False
                pygame.quit()
                sys.exit()
        
        # 웹캠 이미지를 읽어온다.
        _, img = cam.read()
        # 좌우 반전 
        image = cv2.flip(img, 1)
        results = hands.process(image)

        # game over 화면을 띄운다.
        screen.fill(BLACK)
        screen.blit(over_txt_render, (w*o1 - over_txt_render.get_width() * o1, 3 * o2))
        screen.blit(quit_img, (w*o1 + 220,  4 * o2))
        screen.blit(restart_img, (w*o1 - 330,  4 * o2))
        pygame.draw.rect(screen, BLACK, quit_button_box, 2)
        pygame.draw.rect(screen, BLACK, restart_button_box, 2)

        # Spark VFX 효과를 일으킨다.
        for i, spark in sorted(enumerate(sparks), reverse=True):
            spark.move(1)
            spark.draw(screen)
            if not spark.alive:
                sparks.pop(i)
        # hand detection과 hand tracking을 구현한다
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 랜드마크 추출 및 전처리
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                landmarks = torch.tensor(landmarks).flatten().unsqueeze(0)

                # 모델 예측
                with torch.no_grad():
                    preds = model(landmarks)
                    _, predicted = torch.max(preds.data, 1)

                # 손의 상태 확인
                is_closed = predicted.item() in [1, 3]

                palm_x, palm_y = hand_landmarks.landmark[9].x * w, hand_landmarks.landmark[9].y * h

                pygame.draw.circle(screen, (0, 255, 0), (int(palm_x), int(palm_y)), 10)

                if is_closed:
                    # 주먹을 쥐었을때 spark가 일어난다.
                    for i in range(10):
                        sparks.append(Spark([int(palm_x), int(palm_y)], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 2))

                    # 게임을 나간다.
                    if quit_button_box.collidepoint(int(palm_x), int(palm_y)):
                        over = False
                        pygame.quit()
                        sys.exit()

                    # 초기화를 시키고 게임을 다시 시작한다.
                    if restart_button_box.collidepoint(int(palm_x), int(palm_y)):
                        over = False
                        rate = 'START'
                        excellent_cnt = 0     
                        perfect_cnt = 0       
                        bad_cnt = 0           
                        miss_cnt = 0 
                        combo = 0
                        combo_effect = 0
                        combo_effect2 = 0
                        miss_anim = 0
                        last_combo = 0
                        life_cnt = 5
                        generate_notes()
                        simultaneous_notes()  
                        game()

        pygame.display.flip()
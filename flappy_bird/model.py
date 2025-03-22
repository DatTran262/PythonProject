# model.py
import random
from PyQt6.QtCore import QRect

class FlappyBirdModel:
    def __init__(self):
        self.screen_width = 400
        self.screen_height = 600
        self.bird_x = 100
        self.bird_y = 300
        self.bird_velocity = 0
        self.bird_size = 30
        self.gravity = 0.3
        self.jump_strength = -5
        self.pipes = []
        self.pipe_width = 30
        self.pipe_gap = 150
        self.pipe_speed = 3
        self.score = 0
        self.game_over = False
        self.pipe_spawn_timer = 0
        self.pipe_spawn_interval = 100  # Tạo ống mới sau mỗi 100 frame

    def update(self):
        if self.game_over:
            return

        # Cập nhật vị trí chim
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity

        # Kiểm tra va chạm với mặt đất hoặc trần
        if self.bird_y > self.screen_height - self.bird_size or self.bird_y < 0:
            self.game_over = True

        # Tạo ống mới
        self.pipe_spawn_timer += 1
        if self.pipe_spawn_timer >= self.pipe_spawn_interval:
            self.spawn_pipe()
            self.pipe_spawn_timer = 0

        # Cập nhật vị trí ống
        for pipe in self.pipes[:]:
            pipe["x"] -= self.pipe_speed
            if pipe["x"] + self.pipe_width < 0:
                self.pipes.remove(pipe)
                self.score += 1

        # Kiểm tra va chạm với ống
        bird_rect = QRect(self.bird_x, int(self.bird_y), self.bird_size, self.bird_size)
        for pipe in self.pipes:
            top_pipe_rect = QRect(pipe["x"], 0, self.pipe_width, pipe["top"])
            bottom_pipe_rect = QRect(pipe["x"], pipe["bottom"], self.pipe_width, self.screen_height - pipe["bottom"])
            if bird_rect.intersects(top_pipe_rect) or bird_rect.intersects(bottom_pipe_rect):
                self.game_over = True

    def jump(self):
        if not self.game_over:
            self.bird_velocity = self.jump_strength

    def spawn_pipe(self):
        gap_y = random.randint(100, self.screen_height - 100 - self.pipe_gap)
        self.pipes.append({
            "x": self.screen_width,
            "top": gap_y,
            "bottom": gap_y + self.pipe_gap
        })

    def reset(self):
        self.bird_y = 300
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipe_spawn_timer = 0
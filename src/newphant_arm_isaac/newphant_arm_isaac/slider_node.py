#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

import pygame
import sys

class NewPhantArmControl(Node):

    def __init__(self):
        super().__init__('newphant_arm_control')

        # Publisher (RAW values)
        self.publisher = self.create_publisher(
            Float32MultiArray,
            '/newphant_arm/raw_angles',
            10
        )

        pygame.init()

        self.WIDTH, self.HEIGHT = 900, 650
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("NewPhant Arm Control")

        self.FONT = pygame.font.SysFont("Arial", 22)

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.clock = pygame.time.Clock()

        # Sliders
        self.sliders = [
            self.Slider("shoulder baselink", 100, 80, 700, -1.57, 1.57),
            self.Slider("sArm shoulder",     100, 160, 700, 0, 3.14),
            self.Slider("shoulder elbow",    100, 240, 700, 0, 3.14),
            self.Slider("wrist elbow",       100, 320, 700, 0, 3.14),
            self.Slider("wrist roll",        100, 400, 700, -3.14, 3.14),
            self.Slider("Gripper action",    100, 480, 700, 0, 1.57),
        ]

        self.exit_button = self.ExitButton(350, 560, 200, 50)

    # ---------------- SLIDER ----------------
    class Slider:
        def __init__(self, name, x, y, w, min_val, max_val, start_val=0):
            self.name = name
            self.rect = pygame.Rect(x, y, w, 10)
            self.min_val = min_val
            self.max_val = max_val
            self.value = start_val
            self.handle_radius = 14
            self.dragging = False

        def get_pos_from_value(self):
            ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
            return self.rect.x + ratio * self.rect.w

        def get_value_from_pos(self, x):
            ratio = (x - self.rect.x) / self.rect.w
            ratio = max(0, min(1, ratio))
            return self.min_val + ratio * (self.max_val - self.min_val)

        def handle_event(self, event):
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if abs(mouse_x - self.get_pos_from_value()) < self.handle_radius + 5:
                    if abs(mouse_y - self.rect.y) < 15:
                        self.dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    self.value = self.get_value_from_pos(mouse_x)

        def draw(self, screen, font, color):
            pygame.draw.rect(screen, color, self.rect)

            handle_x = self.get_pos_from_value()
            pygame.draw.circle(screen, color, (int(handle_x), self.rect.y + 5), self.handle_radius)

            text = f"{self.name}: {self.value:.5f}"
            label = font.render(text, True, color)
            screen.blit(label, (self.rect.x, self.rect.y - 35))

    # ---------------- EXIT BUTTON ----------------
    class ExitButton:
        def __init__(self, x, y, w, h):
            self.rect = pygame.Rect(x, y, w, h)

        def draw(self, screen, font, color):
            pygame.draw.rect(screen, color, self.rect, 2)
            text = font.render("EXIT", True, color)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

    # ---------------- LOOP ----------------
    def run(self):
        while rclpy.ok():
            self.screen.fill(self.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    rclpy.shutdown()
                    sys.exit()

                for slider in self.sliders:
                    slider.handle_event(event)

                self.exit_button.handle_event(event)

            # Draw UI
            for slider in self.sliders:
                slider.draw(self.screen, self.FONT, self.WHITE)

            self.exit_button.draw(self.screen, self.FONT, self.WHITE)

            # Prepare message
            msg = Float32MultiArray()
            msg.data = [float(f"{s.value:.5f}") for s in self.sliders]

            # Publish
            self.publisher.publish(msg)

            pygame.display.flip()
            self.clock.tick(60)


# ---------------- MAIN ----------------
def main(args=None):
    rclpy.init(args=args)

    node = NewPhantArmControl()
    node.run()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
from gui.popup_window import PopupWindow
from gui.status_bar import StatusBar
from gui.text import Text

from data.paths import HEALTH_WINDOW_BG, CALIBRI_BOLD
from data.gui_texts import HEALTH_WINDOW_LABELS, TANK_NAMES

from constants import SCR_H, SCR_W2, WHITE
from utils import HF, H


class HealthWindow(PopupWindow):
    """Window that shows status bar representing how many
    more bubbles the player needs to collect to upgrade his tank.
    """
    def __init__(self, game):
        super().__init__(SCR_W2 - HF(456),
                         SCR_H,
                         HF(912),
                         HF(106),
                         -HF(1.12),
                         1250,
                         HEALTH_WINDOW_BG)
        self.game = game

        self.max_health = 75
        self.status_bar = StatusBar(self.x + HF(16), self.y + HF(56), self.w - HF(32), H(32), 75)
        self.tank_label = Text(self.x + HF(23), self.y + HF(18), CALIBRI_BOLD, H(32), WHITE)
        self.bubbles_label = Text(0, self.y + HF(18), CALIBRI_BOLD, H(32), WHITE)

    def reset(self):
        super().reset()
        self.status_bar.move_to(self.x + HF(16), self.y + HF(56))
        self.tank_label.move_to(self.tank_label.x, self.y + HF(9))
        self.bubbles_label.move_to(0, self.y + HF(9))

    def set_status_bar(self, max_health, health, player_level):
        self.status_bar.set_max_value(max_health)
        self.status_bar.set_value(health if player_level != 5 else max_health)

    def set_bubbles_label(self, player_health, player_level):
        if player_level != 5:
            text = "%s %s" % (str(self.max_health - player_health),
                              HEALTH_WINDOW_LABELS[self.game.language][0])
        else:
            text = HEALTH_WINDOW_LABELS[self.game.language][1]
        self.bubbles_label.set_text(text)
        self.bubbles_label.move_to(self.x + self.w - HF(23) - self.bubbles_label.w,
                                   self.bubbles_label.y)

    def activate(self, health, player_level):
        super().activate()
        if player_level != 5:
            self.status_bar.set_value(health)
            self.set_bubbles_label(health, player_level)

    def set(self, player_tank, player_health, player_max_health):
        self.max_health = player_max_health
        self.set_status_bar(player_max_health, player_health, player_tank[0])
        self.tank_label.set_text(TANK_NAMES[self.game.language][player_tank])
        self.set_bubbles_label(player_health, player_tank[0])

    def update(self, dt):
        yo = self.y
        self.update_state(dt)
        dy = self.y - yo
        self.status_bar.move(0, dy)
        self.tank_label.move(0, dy)
        self.bubbles_label.move(0, dy)

    def draw(self, screen):
        if self.on_screen:
            screen.blit(self.background, (round(self.x), round(self.y)))
            self.status_bar.draw(screen)
            self.tank_label.draw(screen)
            self.bubbles_label.draw(screen)


__all__ = ["HealthWindow"]

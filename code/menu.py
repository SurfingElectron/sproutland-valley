import pygame
from settings import *
from timekeeper import Timer

class Menu:
    def __init__(self, player, toggle_menu):
        
        # Setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../fonts/LycheeSoda.ttf', 30)

        # Menu options
        self.width = 400
        self.margin = 10
        self.padding = 8

        # Menu entries
        self.entries = list(self.player.inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.inventory) - 1
        self.display_window()

        # Menu Selection
        self.index = 0
        self.timer = Timer(200)

    def display_money(self):
        text_surf = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT - 20)))

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10, 10), 0, 4)
        self.display_surface.blit(text_surf, text_rect)

    def display_window(self):

        # Create the text surfaces
        self.text_surfs = []
        self.total_height = 0
        for item in self.entries:
            text_surf = self.font.render(item, False, 'black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        # Create the Buy / Sell surfaces
        self.buy_text = self.font.render('BUY', False, 'black')
        self.sell_text = self.font.render('SELL', False, 'black')
        
        # Create the menu window
        self.total_height += (len(self.text_surfs) - 1) * self.margin
        self.menu_top = (SCREEN_HEIGHT / 2) - (self.total_height / 2)
        self.menu_left = (SCREEN_WIDTH / 2) - (self.width / 2)
        self.window = pygame.Rect(self.menu_left, self.menu_top, self.width, self.total_height)

    def display_entry(self, text_surf, amount, top, is_selected):
        # Render background
        bg_rect = pygame.Rect(self.window.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

        # Render text
        text_rect = text_surf.get_rect(midleft = (self.window.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        # Render amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright = (self.window.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        # Behaviour when an entry is selected
        if is_selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)

            # Show if player can sell or buy the menu item
            if self.index <= self.sell_border:
                sell_rect = self.sell_text.get_rect(midleft = (self.window.left + 150, bg_rect.centery)) 
                self.display_surface.blit(self.sell_text, sell_rect)
            else:
                buy_rect = self.buy_text.get_rect(midleft = (self.window.left + 150, bg_rect.centery)) 
                self.display_surface.blit(self.buy_text, buy_rect)

    def input(self):
        keys = pygame.key.get_pressed()
        
        # Using the timer function to stop pygame responding to a long key press
        self.timer.update()

        # Quit the menu
        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        # Sell or buy items
        if not self.timer.active:
            if keys[pygame.K_SPACE]:
                self.timer.activate()
                current_item = self.entries[self.index]

                # Selling items
                if self.index <= self.sell_border:
                    if self.player.inventory[current_item] > 0:
                        self.player.inventory[current_item] -= 1
                        self.player.money += SELL_PRICES[current_item]
                # Buying items
                else:
                    seed_price = PURCHASE_PRICES[current_item]
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= PURCHASE_PRICES[current_item]
        
        # Navigate the menu
        if not self.timer.active:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.index -= 1
                 
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

        # Clamp the menu index values, make the selection cycle through
        if self.index < 0:
            self.index = len(self.entries) - 1

        if self.index > len(self.entries) - 1:
            self.index = 0

    def update(self):
        self.input()
        self.display_money()

        # Create the menu
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.window.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.margin)
            amount_list = list(self.player.inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.display_entry(
                text_surf = text_surf, 
                amount = amount, 
                top = top,
                is_selected = self.index == text_index
                )

            
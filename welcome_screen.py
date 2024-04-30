import pygame
import time
#from settings import apply_theme, draw_toggle_switch, handle_toggle_click


def show_welcome_screen(screen):
    pygame.init()
    running = True
    clock = pygame.time.Clock()

    is_light_mode = True  # not used


    settings_icon = pygame.image.load('settings_icon.png').convert_alpha()
    scaled_size = (70, 70)
    settings_icon = pygame.transform.scale(settings_icon, scaled_size)
    settings_icon_rect = pygame.Rect(10, 10, scaled_size[0], scaled_size[1])

    #colors
    background_color = (255, 255, 255)
    heading_color = (120, 124, 127)
    text_color = (0, 0, 0)

    button_color = (108,169,101)  # green color for the button
    button_hover_color = (144, 238, 144)  # lighter green when hovering

    heading_font = pygame.font.SysFont("Arial", 36, bold=True)
    body_font = pygame.font.SysFont("Arial", 24)
    button_font = pygame.font.SysFont("Arial", 28, bold=True)

    button_text = "Play"
    button_rect = pygame.Rect(screen.get_width() / 2 - 100, 700, 200, 50)

    while running:
       # apply_theme(screen, is_light_mode)
        #draw_toggle_switch(screen, is_light_mode)  # not being used


        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
                if settings_icon_rect.collidepoint(mouse_pos):

                    #is_light_mode = handle_toggle_click(event.pos, is_light_mode)
                   # apply_theme(screen, is_light_mode)
                    print("Settings icon clicked")
                    #draw_toggle_switch(screen, is_light_mode)

        # button appearance logic (change color on hover)
        if button_rect.collidepoint(mouse_pos):
            button_color_current = button_hover_color
            if mouse_clicked and button_rect.collidepoint(mouse_pos):
                return
        else:
            button_color_current = button_color

        screen.fill(background_color)

        # text
        text_surface = heading_font.render('Welcome to Wordle!', True, heading_color)
        screen.blit(text_surface, (screen.get_width() / 2 - text_surface.get_width() / 2, 100))

        text_surface = body_font.render('How to play:', True, heading_color)
        screen.blit(text_surface, (screen.get_width() / 2 - text_surface.get_width() / 2, 180))

        instructions = [
            '',
            '',
            '-Guess the wordle in 6 tries.',
            '',
            '- Each guess must be a valid 5-letter word.',
            '',
            '- The color of the tiles will change to show how close your guess was to the word.'
        ]

        for i, instruction in enumerate(instructions, start=1):
            text_surface = body_font.render(instruction, True, text_color)
            screen.blit(text_surface, (100, 180 + i * 40))  # Increment Y position for each line

        # Draw Play button
        pygame.draw.rect(screen, button_color_current, button_rect)
        text_surf = button_font.render(button_text, True, (255, 255, 255))  # White text
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)

        screen.blit(settings_icon, (2, 2))


        pygame.display.flip()
        clock.tick(30)



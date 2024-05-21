import pygame

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

buttons = [
    pygame.Rect(25, 25, 100, 100),
    pygame.Rect(175, 25, 100, 100),
    pygame.Rect(25, 175, 100, 100),
    pygame.Rect(175, 175, 100, 100)]
colors = [(64, 0, 0), (64, 64, 0), (0, 64, 0), (0, 0, 64)]
colorsH = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]

fingers = {}
run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
            x = event.x * window.get_height()
            y = event.y * window.get_width()
            fingers[event.finger_id] = x, y
        if event.type == pygame.FINGERUP:
            fingers.pop(event.finger_id, None)

    highlight = []  
    for i, rect in enumerate(buttons): 
        touched = False
        for finger, pos in fingers.items():       
            if rect.collidepoint(pos):
                touched = True
        highlight.append(touched)   

    # the same with list comprehensions
    #highlight = [any(r.collidepoint(p) for _, p in fingers.items()) for _, r in enumerate(buttons)]

    window.fill(0)
    for rect, color, colorH, h in zip(buttons, colors, colorsH, highlight):
        c = colorH if h else color
        pygame.draw.rect(window, c, rect)
    pygame.display.flip()

pygame.quit()
exit()
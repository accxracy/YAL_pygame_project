import pygame

class Button:
	def __init__(self,pos, width, height, text, font, image, image_hover=None, sound=None):

		self.font = font
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.text = text
		self.width = width
		self.height = height
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
		self.hover_image = self.image
		if image_hover:
			self.hover_image = pygame.image.load(image_hover)
			self.hover_image = pygame.transform.scale(self.hover_image, (self.width, self.height))

		self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
		self.sound = sound
		if sound:
			self.sound = pygame.mixer.Sound(self.sound)
		self.is_hovered = False



	def draw(self, screen):
		current_image = self.hover_image if self.is_hovered else self.image
		screen.blit(current_image, self.rect.topleft)

		font = self.font
		text_s = font.render(self.text, True, (255, 255, 255))
		text_rect = text_s.get_rect(center=self.rect.center)
		screen.blit(text_s, text_rect)

	def checking_hover(self, mouse_position):
		self.is_hovered = self.rect.collidepoint(mouse_position)

	def han_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
			if self.sound:
				self.sound.play()
			pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

	def change_image(self, new_image):
		new_image = pygame.image.load(new_image)
		new_image = pygame.transform.scale(new_image, (self.width, self.height))
		self.image = new_image
		self.hover_image = new_image





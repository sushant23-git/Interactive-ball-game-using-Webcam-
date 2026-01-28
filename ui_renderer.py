"""
UI renderer for displaying game information and menus.
"""
import pygame
import config


class UIRenderer:
    """Renders user interface elements."""
    
    def __init__(self, screen):
        """Initialize UI renderer.
        
        Args:
            screen: Pygame screen surface
        """
        self.screen = screen
        
        # Initialize fonts
        pygame.font.init()
        self.font_score = pygame.font.Font(None, config.FONT_SIZE_SCORE)
        self.font_normal = pygame.font.Font(None, config.FONT_SIZE_NORMAL)
        self.font_small = pygame.font.Font(None, config.FONT_SIZE_SMALL)
    
    def draw_score(self, score):
        """Draw the current score.
        
        Args:
            score: Current score value
        """
        score_text = self.font_score.render(f"Score: {score}", True, config.TEXT_COLOR)
        self.screen.blit(score_text, (20, 20))
    
    def draw_fps(self, fps):
        """Draw the current FPS.
        
        Args:
            fps: Current FPS value
        """
        fps_text = self.font_small.render(f"FPS: {fps}", True, config.TEXT_COLOR)
        text_rect = fps_text.get_rect()
        text_rect.topright = (config.SCREEN_WIDTH - 20, 20)
        self.screen.blit(fps_text, text_rect)
    
    def draw_lives(self, lives):
        """Draw remaining lives.
        
        Args:
            lives: Number of lives remaining
        """
        if config.ENABLE_LIVES:
            lives_text = self.font_normal.render(f"Lives: {lives}", True, config.TEXT_COLOR)
            self.screen.blit(lives_text, (20, 80))
    
    def draw_game_over(self, score):
        """Draw game over screen.
        
        Args:
            score: Final score
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_score.render("GAME OVER", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH // 2, 
                                                          config.SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_normal.render(f"Final Score: {score}", True, config.TEXT_COLOR)
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH // 2, 
                                                  config.SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Restart instruction
        restart_text = self.font_small.render("Press SPACE to restart or ESC to quit", 
                                              True, config.TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=(config.SCREEN_WIDTH // 2, 
                                                     config.SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_menu(self):
        """Draw the start menu."""
        # Background
        self.screen.fill(config.BG_COLOR)
        
        # Title
        title_text = self.font_score.render("ASTEROID DESTROYER", True, (100, 200, 255))
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 
                                                 config.SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "Use your hand to destroy falling asteroids!",
            "",
            "Position your webcam to see the screen",
            "Point your index finger at asteroids to destroy them",
            "",
            "Press SPACE to start",
            "Press F to toggle fullscreen",
            "Press ESC to quit"
        ]
        
        y_offset = config.SCREEN_HEIGHT // 2 - 40
        for line in instructions:
            if line:
                text = self.font_small.render(line, True, config.TEXT_COLOR)
            else:
                # Empty line
                text = self.font_small.render(" ", True, config.TEXT_COLOR)
            text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 35
    
    def draw_calibration_guide(self):
        """Draw calibration guide (future feature)."""
        guide_text = self.font_small.render("Calibration mode - touch corners in order", 
                                            True, (255, 255, 0))
        guide_rect = guide_text.get_rect(center=(config.SCREEN_WIDTH // 2, 50))
        self.screen.blit(guide_text, guide_rect)

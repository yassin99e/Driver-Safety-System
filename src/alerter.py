import pygame
from pathlib import Path
from src.config import SOUND_SLEEP, SOUND_TIRED


class AudioAlerter:
    """Manages audio alert playback."""
    
    def __init__(self):
        """Initialize pygame mixer and load sound files."""
        pygame.mixer.init()
        
        # Load sound files
        self.sounds = {
            'sleep': pygame.mixer.Sound(str(SOUND_SLEEP)),
            'tired': pygame.mixer.Sound(str(SOUND_TIRED))
        }
        
        self.current_playing = None
        
    def play_alert(self, alert_type):
        """Play the appropriate alert sound.
        
        Args:
            alert_type: 'sleep' or 'tired'
        """
        if alert_type not in self.sounds:
            return
            
        # Stop any currently playing sound
        pygame.mixer.stop()
        
        # Play the alert
        self.sounds[alert_type].play()
        self.current_playing = alert_type
        
    def stop(self):
        """Stop all audio playback."""
        pygame.mixer.stop()
        self.current_playing = None
        
    def is_playing(self):
        """Check if any sound is currently playing.
        
        Returns:
            bool: True if audio is playing
        """
        return pygame.mixer.get_busy()
    
    def cleanup(self):
        """Clean up pygame mixer resources."""
        pygame.mixer.quit()

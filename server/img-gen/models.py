class ImagePrompt:
    def __init__(
        self,
        subject: str,
        style: str = "",
        medium: str = "",
        lighting: str = "",
        color_palette: str = "",
        composition: str = "",
        resolution: str = "",
        contrast: str = "",
        mood: str = "",
        details: str = ""
    ):
        self.subject = subject
        self.style = style
        self.medium = medium
        self.lighting = lighting
        self.color_palette = color_palette
        self.composition = composition
        self.resolution = resolution
        self.contrast = contrast
        self.mood = mood
        self.details = details

    def to_prompt(self) -> str:
        """Generates a prompt string by combining the non-empty attributes"""
        components = [
            self.subject,
            self.style,
            self.medium,
            self.lighting,
            self.color_palette,
            self.composition,
            self.resolution,
            self.contrast,
            self.mood,
            self.details
        ]
        # Filtra los campos vacíos y une con comas
        return ', '.join([comp for comp in components if comp])
    
    def to_mpc(self) -> dict:
        """Returns a dictionary representation in MPC (Modular Prompt Construction) format."""
        return {
            "Subject": self.subject,
            "Style": self.style,
            "Medium": self.medium,
            "Lighting": self.lighting,
            "Color": self.color_palette,
            "Composition": self.composition,
            "Resolution": self.resolution,
            "Contrast": self.contrast,
            "Mood": self.mood,
            "Details": self.details
        }

    def __str__(self):
        return self.to_prompt()


# | Component         | Example                                                      | Description                |
# | ----------------- | ------------------------------------------------------------ | -------------------------- |
# | **Subject**       | "a cat", "cyberpunk city", "robot"                           | What appears in the image. |
# | **Style**         | "pixel art", "oil painting", "photorealistic", "anime style" | How the image looks.       |
# | **Medium**        | "3D render", "sketch", "digital art"                         | Technique or format.       |
# | **Lighting**      | "dramatic lighting", "soft light", "neon glow"               | Adds atmosphere.           |
# | **Color**         | "pastel colors", "monochrome", "vivid"                       | Dominant color palette.    |
# | **Composition**   | "close-up", "wide shot", "centered"                          | Focus and layout.          |
# | **Extra details** | "in the rain", "wearing sunglasses", "with flowers"          | Additional context.        |

# # Example usage:
# img = ImagePrompt(
#     subject="A serene landscape",
#     style="Impressionist",
#     medium="Oil painting",
#     lighting="Soft morning light",
#     color_palette="Pastel colors",
#     composition="Balanced with a foreground tree",
#     details="Subtle brush strokes"
# )
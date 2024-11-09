import json
import re

class CognitiveDistortionAnalyzer:
    def __init__(self):
        self.distortion_patterns = {}

    def load_distortion_patterns(self):
        """
        Loads cognitive distortion patterns from a JSON file into a dictionary.

        Primary Author: Josh
        Techniques Claimed:
        - With statements
        - JSON file handling
        """
        try:
            with open('distortion_patterns.json', 'r') as file:
                self.distortion_patterns = json.load(file)
        except FileNotFoundError:
            print("Error: The file 'distortion_patterns.json' was not found.")
        except json.JSONDecodeError:
            print("Error: The file 'distortion_patterns.json' is not valid JSON.")


    def identify_overgeneralization(self, text):
        """
        Analyzes the text to detect overgeneralization cognitive distortions.

        Primary Author: John
        Techniques Claimed:
        - Regular expressions
        - Comprehensions
        """
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        patterns = self.distortion_patterns.get('overgeneralization', [])
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    
    def detect_mind_reading(self, text):
        """
        Detects mind reading cognitive distortions in the input text.

        Primary Author: Zaynab
        Techniques Claimed:
        - Optional parameters
        - Conditional expressions
        """
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        patterns = self.distortion_patterns.get('mind_reading', [])
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


# Testing Josh's Function
print("Testing load_distortion_patterns:")
analyzer = CognitiveDistortionAnalyzer()
analyzer.load_distortion_patterns()
print("Loaded Distortion Patterns:", analyzer.distortion_patterns)  

# Testing John’s Function
print("\nTesting identify_overgeneralization:")
analyzer.distortion_patterns = {
    'overgeneralization': ['always', 'never', 'everyone', 'nobody']
}
result = analyzer.identify_overgeneralization("I always fail at everything.")
print("Overgeneralization detected:", result)  

# Testing Zaynab’s Function
print("\nTesting detect_mind_reading:")
analyzer.distortion_patterns = {
    'mind_reading': ['they think', 'they believe', 'they feel']
}
result = analyzer.detect_mind_reading("They think I'm not good enough.")
print("Mind reading detected:", result)  

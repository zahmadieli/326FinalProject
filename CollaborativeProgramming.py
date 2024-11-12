import json
import re
 
class CognitiveDistortionAnalyzer:
    def __init__(self):
        """
        Initializes the CognitiveDistortionAnalyzer with an empty dictionary to
        store cognitive distortion patterns.

        Attributes:
            distortion_patterns: A dictionary to hold loaded patterns for
                                detecting cognitive distortions.
        """
        self.distortion_patterns = {}
        
    # Josh's Function 
    def load_distortion_patterns(self):
        """
        Loads cognitive distortion patterns from a JSON file into a dictionary 
        for analysis.
        
        Reads from 'distortion_patterns.json' and loads patterns into the
        distortion_patterns attribute, where patterns are categorized by 
        distortion types.

        Primary Author: Josh
        Techniques Claimed:
        - With statements
        - JSON file handling
        
        Exceptions:
            FileNotFoundError: If 'distortion_patterns.json' is not found.
            json.JSONDecodeError: If the JSON file is improperly formatted.
        
        """
        try:
            with open('distortion_patterns.json', 'r') as file:
                self.distortion_patterns = json.load(file)
        except FileNotFoundError:
            print("Error: The file 'distortion_patterns.json' was not found.")
        except json.JSONDecodeError:
            print("Error: The file 'distortion_patterns.json' is not valid JSON.")

    # John's Function 
    def identify_overgeneralization(self, text):
        """
        Analyzes the text to detect overgeneralization cognitive distortions.
        
        Uses patterns from the distortion_patterns dictionary under the key
        'overgeneralization' to identify keywords in the input text. 

        Parameters:
            text (str): The user's input thought to be analyzed.

        Returns:
            bool: True if overgeneralization patterns are detected in the text,
                  False otherwise.

        Primary Author: John
        Techniques Claimed:
        - Regular expressions
        - Comprehensions
        
        Raises:
            TypeError: If text is not a string.
        """
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        patterns = self.distortion_patterns.get('overgeneralization', [])
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    # Zainab's Function 
    def detect_mind_reading(self, text):
        """
        Detects mind reading cognitive distortions in the input text.
        
        Checks for keywords or phrases associated with mind reading in the 
        distortion_patterns dictionary under the key 'mind_reading'.

        Parameters:
            text (str): The user's input thought to be analyzed.

        Returns:
            bool: True if mind reading patterns are detected in the text,
                  False otherwise.

        Primary Author: Zainab
        Techniques Claimed:
        - Optional parameters
        - Conditional expressions
        
        Raises:
            TypeError: If text is not a string.
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

# Testing Zainab’s Function
print("\nTesting detect_mind_reading:")
analyzer.distortion_patterns = {
    'mind_reading': ['they think', 'they believe', 'they feel']
}
result = analyzer.detect_mind_reading("They think I'm not good enough.")
print("Mind reading detected:", result)  

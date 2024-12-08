import json
import re
import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuration Data

MOOD_ADVICE = {
    'happy': "Share your joy with someone or express gratitude by writing it down.",
    'sad': "Engage in physical activity, like a workout or a brisk walk, to boost endorphins.",
    'anxious': "Practice deep breathing exercises or write down what's causing your anxiety.",
    'angry': "Meditate or channel your anger into a productive activity like journaling.",
    'neutral': "Try something new or stimulating, such as reading an interesting article.",
    'excited': "Channel your energy into planning or organizing the source of excitement.",
    'frustrated': "Take a short break, stretch, or listen to calming music.",
    'confused': "Break down the problem into smaller parts or seek guidance.",
    'content': "Reflect on what's making you feel content and reinforce these habits.",
    'overwhelmed': "Prioritize tasks by writing a to-do list, then tackle one at a time."
}

DISTORTION_ADVICE = {
    'overgeneralization': "Try to identify one exception to your conclusion and focus on that.",
    'emotional_reasoning': "Consider if your feelings are facts or if there's evidence that contradicts them.",
    "mind_reading": "Ask yourself if you have evidence for what you think others believe.",
    "catastrophizing": "Imagine a moderate outcome instead of the worst. List more realistic scenarios.",
    "personalization": "Remember that not everything is in your control. Distribute responsibility fairly.",
    "should_statements": "Examine your 'shoulds' and 'musts'. Are they realistic or fair?",
    "all_or_nothing": "Seek shades of gray. Life is rarely all bad or all good.",
    "labeling": "Focus on behavior or specific incidents instead of labeling your entire self.",
    "disqualifying_the_positive": "Acknowledge your successes and positive aspects; they do count.",
    "jumping_to_conclusions": "Gather more evidence before concluding what others think or intend."
}

# Distortion Classes

class Distortion:
    """
    Represents a cognitive distortion.
    Primary Author: John
    Techniques Claimed: magic methods (other than __init__) - __str__
    """

    def __init__(self, name, patterns, explanation):
        """
        Primary Author: John
        Initializes a Distortion with name, patterns, and explanation.

        Side Effects:
            - Sets instance attributes: name, patterns, explanation.

        Parameters:
            name (str): Distortion name
            patterns (list): Regex patterns characterizing the distortion
            explanation (str): Explanation of the distortion
        """
        self.name = name
        self.patterns = patterns
        self.explanation = explanation

    def __str__(self):
        """
        Primary Author: John
        Technique: magic methods (other than __init__)

        Side Effects:
            - None.

        Returns:
            str: A user-friendly string representation of the distortion.
        """
        return f"Distortion: {self.name}\nExplanation: {self.explanation}"

    def match(self, text):
        """
        Checks if the given text matchse any of the distortion's patterns.

        Side Effects:
            - None.

        Primary Author: John

        Parameters:
            text (str): The text to analyze.

        Returns:
            (bool, str): (True, pattern) if found, otherwise (False, None)
        """
        for pattern in self.patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True, pattern
        return False, None


# Analyzer Class

class CognitiveDistortionAnalyzer:
    """
    Analyzes user input for cognitive distortions and handles user data.

    Composition: Holds a list of Distortion instances.
    """

    def __init__(self):
        """
        Initializes with empty distortion data and user data.
        """
        self.distortions_data = {}
        self.user_data = []
        self.distortions = []

    def load_distortions_data(self):
        """
        Loads cognitive distortions from 'distortion_patterns.json' and creates Distortion objects.

        Primary Author: Josh
        Techniques: with statements, comprehensions

        Side Effects:
            - Reads from 'distortion_patterns.json'.
            - Updates self.distortions_data and self.distortions.
        """
        try:
            with open('distortion_patterns.json', 'r') as file:
                data = json.load(file)
                self.distortions_data = data

            self.distortions = [
                Distortion(name=k, patterns=v["patterns"], explanation=v["explanation"])
                for k, v in data.items()
            ]
        except FileNotFoundError:
            print("Error: 'distortion_patterns.json' not found.")
        except json.JSONDecodeError:
            print("Error: 'distortion_patterns.json' is not valid JSON.")

    def analyze_text(self, text):
        """
        Analyzes text for cognitive distortions.

        Parameters:
            text (str): The user's input text.

        Returns:
            list of (distortion_name, pattern)
        """
        detected_distortions = []
        sentences = re.split(r'[.!?]', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            for d in self.distortions:
                found, pattern = d.match(sentence)
                if found:
                    display_pattern = re.sub(r'\\b', '', pattern)
                    detected_distortions.append((d.name, display_pattern))
        return detected_distortions

    def detect_suicidal_thoughts(self, text, strict=False):
        """
        Detects references to suicidal thoughts in the input text.

        Primary Author: Zainab
        Techniques: regular expressions

        Parameters:
            text (str): The input text
            strict (bool): Use stricter patterns if True

        Returns:
            bool: True if suicidal phrases are detected, else False.
        """
        suicidal_patterns = [
            "kill myself", "want to die", "suicidal", "end my life",
            "can't go on", "no reason to live", "die", "death wish"
        ]
        if strict:
            suicidal_patterns += ["jump off a bridge", "nothing matters", "rather not live"]

        for pattern in suicidal_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def filter_unrealistic_statements(self, text, intensity=1):
        """
        Filters out unrealistic or absolute statements.

        Primary Author: Zainab
        Technique: optional parameters/keyword arguments

        Non-trivial logic: Checks absolute and unrealistic terms. Severity increases if both are present and intensity > 1.

        Parameters:
            text (str)
            intensity (int): Strictness level

        Returns:
            int: Severity level (0,1,2)
        """
        words = text.lower().split()
        absolute_terms = {"always", "never", "forever", "everything", "nothing"}
        unrealistic_phrases = {"all my problems will cease", "live happily ever after", "do anything in the world"}

        has_abs = any(w in absolute_terms for w in words)
        has_unreal = any(phrase in text.lower() for phrase in unrealistic_phrases)

        severity = 2 if (has_abs and has_unreal and intensity > 1) else (1 if (has_abs or has_unreal) else 0)
        return severity

    def add_user_entry(self, mood, responses, intensity):
        """
        Adds a user entry with mood, responses, intensity, and detected distortions.

        Side Effects:
            - Appends entry to self.user_data.

        Parameters:
            mood (str)
            responses (list of str)
            intensity (int)

        Returns:
            (list, str): (distortions, combined_text)
        """
        combined_text = ' '.join(responses)
        distortions = self.analyze_text(combined_text)
        entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'mood': mood,
            'responses': responses,
            'distortions': [d[0] for d in distortions],
            'intensity': intensity
        }
        self.user_data.append(entry)
        return distortions, combined_text

    def save_user_data(self):
        """
        Saves user_data to 'user_data.json'.

        Primary Author: John
        Technique: json.dump()

        Side Effects:
            - Writes to 'user_data.json'
        """
        try:
            with open('user_data.json', 'w') as f:
                json.dump(self.user_data, f, indent=4)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def load_user_data(self):
        """
        Loads user_data from 'user_data.json' if it exists.

        Side Effects:
            - Updates self.user_data if file is found.
        """
        if os.path.exists('user_data.json'):
            try:
                with open('user_data.json', 'r') as f:
                    self.user_data = json.load(f)
            except json.JSONDecodeError:
                print("Error: 'user_data.json' is not valid JSON.")
                self.user_data = []
        else:
            self.user_data = []

    def visualize_user_mood_timeline(self):
        """
        Visualizes mood entries as a scatter plot over the current week, 
        showing mood intensity by date and emotion.

        Primary Author: Josh 
        Techniques: visualizing data with pyplot or seaborn

        Side Effects:
            - Displays a matplotlib figure window.
        """
        if not self.user_data:
            print("No user data to visualize.")
            return

        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

        mood_entries = []
        for entry in self.user_data:
            ts = datetime.datetime.fromisoformat(entry['timestamp'])
            day = ts.date()
            if start_of_week <= day <= end_of_week:
                mood_entries.append({'date': day, 'intensity': entry['intensity'], 'mood': entry['mood']})

        if not mood_entries:
            print("No data in the current week to visualize.")
            return

        df = pd.DataFrame(mood_entries)
        df['date'] = df['date'].astype(str)

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='date', y='intensity', hue='mood', s=100)

        plt.xlabel("Date")
        plt.ylabel("Intensity (1-5)")
        plt.title("Weekly Mood Intensity by Day and Emotion")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def display_mood_table(self):
        """
        Displays a table of moods and their intensities.

        Side Effects:
            - Prints a DataFrame to console.
        """
        if not self.user_data:
            print("No user data available to display.")
            return

        data = [(entry['mood'], entry['intensity']) for entry in self.user_data]
        df = pd.DataFrame(data, columns=['Mood', 'Intensity'])
        print(df.to_string(index=False))

    def clear_user_data(self):
        """
        Clears all user data and removes 'user_data.json' if present.

        Side Effects:
            - Clears self.user_data
            - Deletes 'user_data.json'
            - Closes all matplotlib figures
        """
        self.user_data = []
        if os.path.exists('user_data.json'):
            os.remove('user_data.json')
        plt.close('all')
        print("All user data has been cleared.")

# User Input Handling Class

class UserInputHandler:
    """
    Handles user input for moods and guided questions.
    Primary Author: [Team collectively, no claimed technique here]
    """

    def __init__(self):
        """
        Initializes with a list of predefined moods.
        """
        self.moods = ['happy', 'sad', 'anxious', 'angry', 'neutral', 'excited', 'frustrated', 'confused', 'content', 'overwhelmed']

    def select_mood(self):
        """
        Allows the user to select a mood from a predefined list or enter their own.

        Side Effects:
            - Prints instructions and reads user input.

        Returns:
            str: The chosen mood.
        """
        print("\nHow are you feeling today? You can select one of the following moods or enter your own:")
        for idx, mood in enumerate(self.moods, 1):
            print(f"{idx}. {mood.capitalize()}")
        while True:
            mood_choice = input("Enter the number, name, or your own mood: ").strip().lower()
            if mood_choice.isdigit():
                mood_index = int(mood_choice) - 1
                if 0 <= mood_index < len(self.moods):
                    return self.moods[mood_index]
            elif mood_choice in self.moods:
                return mood_choice
            else:
                confirm = input(f"You entered '{mood_choice}'. Is this correct? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    return mood_choice
            print("Invalid input. Please try again.")

    def ask_controlled_question(self, prompt, options):
        """
        Asks the user a multiple-choice question.

        Side Effects:
            - Prints prompt and options
            - Reads user input

        Parameters:
            prompt (str)
            options (list)

        Returns:
            str: The selected option.
        """
        print(prompt)
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        while True:
            choice = input("Select a number: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return options[idx]
            print("Invalid choice. Please enter a valid number.")

    def ask_scaled_question(self, prompt):
        """
        Asks the user for a number (1-5) to represent intensity.

        Side Effects:
            - Prints prompt
            - Reads user input

        Parameters:
            prompt (str)

        Returns:
            int: The intensity rating.
        """
        while True:
            scale = input(prompt + " (1-5): ").strip()
            if scale.isdigit():
                val = int(scale)
                if 1 <= val <= 5:
                    return val
            print("Please enter a number between 1 and 5.")

# Main Program

def main():
    """
    The main program loop for the Cognitive Distortion Analyzer.

    Side Effects:
        - Prints to console
        - Reads user input
        - Calls methods that read/write files
        - Displays plots
        - Modifies user_data
    """

    print(f"Current Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    analyzer = CognitiveDistortionAnalyzer()
    analyzer.load_distortions_data()
    analyzer.load_user_data()
    ui = UserInputHandler()

    print("Welcome to the Cognitive Distortion Analyzer!")
    print("Type 'help' for instructions or 'exit' to quit.\n")

    while True:
        cmd = input("Enter a command: ").strip().lower()
        if cmd == 'help':
            print("\nInstructions:")
            print("1. Type 'start' to begin a new session.")
            print("2. Type 'visualize timeline' to see your mood intensity over the current week.")
            print("3. Type 'table' to see a table of your moods and their intensities.")
            print("4. Type 'export' to save your data.")
            print("5. Type 'clear' to delete all your data.")
            print("6. Type 'exit' to quit.\n")
        elif cmd == 'exit':
            analyzer.save_user_data()
            print("Goodbye!")
            break
        elif cmd == 'start':
            mood = ui.select_mood()
            responses = []
            # If mood is happy, prompt a controlled question
            if mood == 'happy':
                reason = ui.ask_controlled_question(
                    "Why are you feeling happy?",
                    ["Achieved a personal goal",
                     "Positive interaction with a friend/loved one",
                     "Enjoying a pleasant activity/environment",
                     "Received good news",
                     "Other"]
                )
                if reason == "Other":
                    reason = input("Please specify (short answer): ")
                responses.append(f"I am happy because: {reason}")
            else:
                reason = input(f"What made you feel {mood} today? (Keep it brief): ")
                responses.append(reason)

            intensity = ui.ask_scaled_question(f"On a scale of 1-5, how intense is this {mood} feeling?")

            combined_text = ' '.join(responses)

            if analyzer.detect_suicidal_thoughts(combined_text, strict=True):
                print("\nWe're sorry to hear that you're feeling this way.")
                print("Please consider reaching out to a mental health professional or trusted individual for support.\n")
                continue

            severity = analyzer.filter_unrealistic_statements(combined_text, intensity=2)
            if severity > 1:
                print("\nWe've noticed some absolute or unrealistic expectations in your response.")
                print("It might help to reflect on whether these beliefs are attainable or if they're setting unhelpful standards.\n")

            distortions, full_text = analyzer.add_user_entry(mood, responses, intensity)
            if distortions:
                print("\nBased on your responses, we noticed the following cognitive distortions:")
                for d_name, pattern in distortions:
                    info = analyzer.distortions_data.get(d_name, {})
                    explanation = info.get('explanation', "No explanation available.")
                    print(f"\n**{d_name.replace('_', ' ').title()}** detected in: \"{pattern}\"")
                    print(f"Explanation: {explanation}")
                    extra_advice = DISTORTION_ADVICE.get(d_name, "")
                    if extra_advice:
                        print(f"Try this: {extra_advice}")
                print("\nUnderstanding these patterns can help you process your thoughts more effectively.\n")

            print(f"\nHere's some advice based on your current mood ({mood}):")
            print(MOOD_ADVICE.get(mood, "Take some time to reflect on your feelings and consider what might help improve your mood."))
        elif cmd == 'visualize timeline':
            analyzer.visualize_user_mood_timeline()
        elif cmd == 'table':
            analyzer.display_mood_table()
        elif cmd == 'export':
            analyzer.save_user_data()
            print("Your data has been saved.\n")
        elif cmd == 'clear':
            confirm = input("Are you sure you want to clear all your data? This action cannot be undone. (yes/no): ").strip().lower()
            if confirm == 'yes':
                analyzer.clear_user_data()
            else:
                print("Data clearing cancelled.")
        else:
            print("Invalid command. Type 'help' for instructions.\n")


if __name__ == "__main__":
    main()

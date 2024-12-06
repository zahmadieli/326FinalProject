import json
import re
import datetime
import os
import sys
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from collections import Counter

# Distortion Classes

class BaseDistortion(ABC):
    """
    Abstract base class for a cognitive distortion.
    Primary Author: John
    Techniques Claimed: magic methods (other than __init__) - __str__
    """
    def __init__(self, name, patterns, explanation):
        self.name = name
        self.patterns = patterns
        self.explanation = explanation

    def __str__(self):
        """
        Primary Author: John
        Technique: magic methods (other than __init__)
        Returns a user-friendly string representation of the distortion.
        """
        return f"Distortion: {self.name}\nExplanation: {self.explanation}"

    @abstractmethod
    def match(self, text):
        """
        Abstract method to detect if this distortion appears in the given text.
        """

class OvergeneralizationDistortion(BaseDistortion):
    def match(self, text):
        for pattern in self.patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True, pattern
        return False, None

class EmotionalReasoningDistortion(BaseDistortion):
    def match(self, text):
        for pattern in self.patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True, pattern
        return False, None

# Analyzer Class

class CognitiveDistortionAnalyzer:
    """
    Analyzes user input for cognitive distortions and handles user data.

    Composition: Holds a list of BaseDistortion instances.
    """

    def __init__(self):
        self.distortions_data = {}
        self.user_data = []
        self.distortions = []

    def load_distortions_data(self):
        """
        Loads cognitive distortions from 'distortion_patterns.json' and sets up distortion objects.

        Primary Author: Josh
        Techniques: with statements, comprehensions
        """
        try:
            with open('distortion_patterns.json', 'r') as file:
                data = json.load(file)
                self.distortions_data = data

            # Build distortion objects using comprehension
            self.distortions = [
                OvergeneralizationDistortion(name=k, patterns=v["patterns"], explanation=v["explanation"])
                if k == "overgeneralization" else
                EmotionalReasoningDistortion(name=k, patterns=v["patterns"], explanation=v["explanation"])
                for k, v in data.items()
            ]
        except FileNotFoundError:
            print("Error: 'distortion_patterns.json' not found.")
        except json.JSONDecodeError:
            print("Error: 'distortion_patterns.json' is not valid JSON.")

    def analyze_text(self, text):
        detected_distortions = []
        sentences = re.split(r'[.!?]', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            for d in self.distortions:
                found, pattern = d.match(sentence)
                if found:
                    detected_distortions.append((d.name, pattern))
        return detected_distortions

    def detect_suicidal_thoughts(self, text, strict=False):
        """
        Detects references to suicidal thoughts in the input text.

        Primary Author: Zainab
        Techniques: regular expressions
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

        Non-trivial logic: Check absolute terms and unrealistic phrases. Intensity > 1 makes it stricter.
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
        Adds a user entry with mood, responses, intensity and detected distortions.

        Intensity is a numeric value (1-5).
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
        Saves user_data to a JSON file.

        Primary Author: John
        Technique: json.dump()
        """
        try:
            with open('user_data.json', 'w') as f:
                json.dump(self.user_data, f, indent=4)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def load_user_data(self):
        if os.path.exists('user_data.json'):
            try:
                with open('user_data.json', 'r') as f:
                    self.user_data = json.load(f)
            except json.JSONDecodeError:
                print("Error: 'user_data.json' is not valid JSON.")
                self.user_data = []
        else:
            self.user_data = []

    def aggregate_distortion_statistics(self):
        """
        Aggregates frequency of detected distortions from user_data.

        Primary Author: Josh
        Technique: comprehensions
        """
        all_distortions = [d for entry in self.user_data for d in entry['distortions']]
        counts = {dist: all_distortions.count(dist) for dist in set(all_distortions)}
        return counts

    def get_emotion_distribution(self):
        """
        Calculates the distribution of emotions for the current week.
        """
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

        emotions = []
        for entry in self.user_data:
            ts = datetime.datetime.fromisoformat(entry['timestamp'])
            day = ts.date()
            if start_of_week <= day <= end_of_week:
                emotions.append(entry['mood'])

        emotion_counts = Counter(emotions)
        return dict(emotion_counts)

    def visualize_user_mood_timeline(self):
        """
        Visualizes intensity over the current week using a line plot.
        """
        if not self.user_data:
            print("No user data to visualize.")
            return

        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

        date_intensity = {}
        for entry in self.user_data:
            ts = datetime.datetime.fromisoformat(entry['timestamp'])
            day = ts.date()
            if start_of_week <= day <= end_of_week:
                if day not in date_intensity:
                    date_intensity[day] = []
                date_intensity[day].append(entry['intensity'])

        if not date_intensity:
            print("No data in the current week to visualize.")
            return

        sorted_dates = sorted(date_intensity.keys())
        avg_intensities = [sum(date_intensity[d]) / len(date_intensity[d]) for d in sorted_dates]

        plt.figure(figsize=(10, 5))
        plt.plot(sorted_dates, avg_intensities, marker='o', linestyle='-', color='blue')
        plt.title("Mood Intensity for the Current Week")
        plt.xlabel("Date")
        plt.ylabel("Average Intensity (1-5)")
        plt.xticks(rotation=45)
        plt.ylim(0, 5)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def visualize_emotion_distribution(self):
        """
        Visualizes the distribution of emotions for the current week using a pie chart.
        """
        emotion_distribution = self.get_emotion_distribution()

        if not emotion_distribution:
            print("No data in the current week to visualize.")
            return

        emotions = list(emotion_distribution.keys())
        counts = list(emotion_distribution.values())

        plt.figure(figsize=(10, 7))
        plt.pie(counts, labels=emotions, autopct='%1.1f%%', startangle=90)
        plt.title("Emotion Distribution for the Current Week")
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.show()


# User Input Handling Class

class UserInputHandler:
    def __init__(self):
        self.moods = ['happy', 'sad', 'anxious', 'angry', 'neutral', 'excited', 'frustrated', 'confused', 'content', 'overwhelmed']

    def select_mood(self):
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
        while True:
            scale = input(prompt + " (1-5): ").strip()
            if scale.isdigit():
                val = int(scale)
                if 1 <= val <= 5:
                    return val
            print("Please enter a number between 1 and 5.")

# Main Program

def main():
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
            print("3. Type 'visualize charts' to see the distribution of your emotions for the current week.")
            print("4. Type 'export' to save your data.")
            print("5. Type 'exit' to quit.\n")
        elif cmd == 'exit':
            analyzer.save_user_data()
            print("Goodbye!")
            break
        elif cmd == 'start':
            mood = ui.select_mood()
            responses = []
            # For demonstration, if mood is happy, do controlled question else just ask a reason
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

            # Ask a scaled question about intensity
            intensity = ui.ask_scaled_question(f"On a scale of 1-5, how intense is this {mood} feeling?")

            combined_text = ' '.join(responses)

            if analyzer.detect_suicidal_thoughts(combined_text, strict=True):
                print("\nWe're sorry to hear that you're feeling this way.")
                print("Please consider reaching out to a mental health professional or trusted individual for support.\n")
                continue

            # Filter unrealistic statements
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
                print("\nUnderstanding these patterns can help you process your thoughts more effectively.\n")
            else:
                print("\nThank you for sharing. It seems like you're processing your thoughts well today!\n")

        elif cmd == 'visualize timeline':
            analyzer.visualize_user_mood_timeline()
        elif cmd == 'visualize chart':
            analyzer.visualize_emotion_distribution()
        elif cmd == 'export':
            analyzer.save_user_data()
            print("Your data has been saved.\n")
        else:
            print("Invalid command. Type 'help' for instructions.\n")

if __name__ == "__main__":
    main()

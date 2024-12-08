# 326FinalProject

### Explanation of the Purpose of Each File: 

**CollaborativeProgramming.py:** The main Python script that implements the cognitive distortion analyzer. It includes classes and functions for detecting cognitive distortions, managing user mood data, visualizing trends, and interacting with the user.

**distortion_patterns.json:** A JSON file containing predefined cognitive distortions, each with regex patterns to identify them in text and an explanation of the distortion's nature.

**user_data.json:** A JSON file storing user entries, including timestamps, moods, responses, detected distortions, and mood intensity levels.

### Instructions to Run the Program from the Command Line:
1. Open a terminal or command prompt.
2. Navigate to the directory containing the CollaborativeProgramming.py file.
3. Ensure the required dependencies (Python and necessary libraries like json, re, datetime, os, matplotlib, and pandas) are installed.
4. Run the script by typing python CollaborativeProgramming.py (python3 if you’re on mac) 

### Instructions to Use the Program and Interpret the Output:

1. **Starting the Program:**
    - Upon starting, you'll see the current date and time, followed by a welcome message.
    - Type help to see a list of commands and their descriptions.

2. **Commands:**
    - start: Begins a session where you'll enter your mood and describe your feelings. The program will:
        - Analyze your input for cognitive distortions.
        - Offer advice based on your mood and detected distortions.
    - Visualize timeline: Displays a scatter plot of mood intensity over the current week.
        - Interpretation: Each mood is represented by a distinct color, and the plot shows intensity levels (1-5) for each day.
    - table: Prints a table summarizing recorded moods and their intensities.
    - export: Saves all recorded user data to user_data.json.
    - clear: Deletes all recorded data and removes the user_data.json file.
    - exit: Saves the data and exits the program.
3. **Input Formats:**
    - When entering a mood, you can either choose from the predefined list or specify your own.
    - When asked to rate intensity, input a number between 1 and 5.
    - Responses to open-ended questions should be in clear, concise sentences.
4. Output:
    - Detected cognitive distortions are listed along with explanations and suggestions for reframing thoughts.
    - If graphs are displayed, they visualize mood trends and can be closed by the user to return to the program.
   
### Annotated Bibliography 
1. Python documentation 
    - Comprehensive reference for Python's core libraries and modules, including json, re, datetime, and os.
    - Utilized for implementing file handling, regular expressions, and datetime operations in the program.
    - Source: https://docs.python.org/3/
2. Matplotlib Documentation 
    - Official documentation for Matplotlib, detailing the library's visualization capabilities, including creating scatter plots and customizing graph aesthetics.
    - Guided the development of mood visualization features, particularly scatter plots to display intensity trends over time.
    - Source: https://matplotlib.org/stable/contents.html
3. "50 Common Cognitive Distortions" by Psychology Today 
    - Article outlining common cognitive distortions and how they manifest in daily thought patterns.
    - Informed the creation of distortion definitions and regex patterns in distortion_patterns.json, enabling accurate detection of distorted thinking.
    - https://www.psychologytoday.com/intl/blog/in-practice/201301/50-common-cognitive-distortions
4. Personal Journaling Journey (Josh Kwan)Reflections on personal experiences with journaling, including the emotional and mental health benefits observed.
    - Reflections on personal experiences with journaling, including the emotional and mental health benefits observed. 
    - This personal narrative shaped the emphasis on self-awareness and reflection in the program, highlighting the role of mood tracking and journaling in mental health improvement.  

6. "5 Benefits of Journaling for Mental Health" by PositivePsychology.com 
    - Explores the psychological benefits of journaling, such as stress reduction, emotional regulation, and enhanced self-awareness.
    - Reinforced the program's focus on helping users articulate their emotions and identify cognitive distortions.
    - Source: https://positivepsychology.com/benefits-of-journaling/
7. Regex101
    - Assisted in developing regex patterns for detecting cognitive distortions in user responses.
    - Source: https://regex101.com/ 
8. "Python Plotting With Matplotlib (Guide)" by Real Python
    - Step-by-step tutorials on creating and customizing visualizations using Matplotlib.
    - Supported the design of scatter plots, especially in learning how to color-code data points based on categorical variables (moods).
    - Source: https://realpython.com/python-matplotlib-guide/


```python
from IPython.core.display import display, HTML

# Define the HTML table as a string
html_table = """
<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
    <thead>
        <tr style="background-color: #f4f4f4;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Function</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Author</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Technique Demonstrated</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">Distortion.__str__</td>
            <td style="border: 1px solid #ddd; padding: 8px;">John</td>
            <td style="border: 1px solid #ddd; padding: 8px;">magic methods (other than __init__)</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">CognitiveDistortionAnalyzer.load_distortions_data</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Josh</td>
            <td style="border: 1px solid #ddd; padding: 8px;">with statements, comprehensions</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">CognitiveDistortionAnalyzer.detect_suicidal_thoughts</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Zainab</td>
            <td style="border: 1px solid #ddd; padding: 8px;">regular expressions</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">CognitiveDistortionAnalyzer.filter_unrealistic_statements</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Zainab</td>
            <td style="border: 1px solid #ddd; padding: 8px;">optional parameters/keyword arguments</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">CognitiveDistortionAnalyzer.save_user_data</td>
            <td style="border: 1px solid #ddd; padding: 8px;">John</td>
            <td style="border: 1px solid #ddd; padding: 8px;">json.dump()</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">CognitiveDistortionAnalyzer.visualize_user_mood_timeline</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Josh</td>
            <td style="border: 1px solid #ddd; padding: 8px;">visualizing data with pyplot</td>
        </tr>
    </tbody>
</table>
"""

# Display the HTML in Jupyter Lab
display(HTML(html_table))
```

    /var/folders/25/lx135skd2419llf11bc39rbr0000gn/T/ipykernel_6077/174672896.py:1: DeprecationWarning: Importing display from IPython.core.display is deprecated since IPython 7.14, please import from IPython display
      from IPython.core.display import display, HTML




<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
    <thead>
        <tr style="background-color: #f4f4f4;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Function</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Author</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Technique Demonstrated</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">Distortion.__str__</td>
            <td style="border: 1px solid #ddd; padding: 8px;">John</td>
            <td style="border: 1px solid #ddd; padding: 8px;">magic methods (other than __init__)</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">CognitiveDistortionAnalyzer.load_distortions_data</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Josh</td>
            <td style="border: 1px solid #ddd; padding: 8px;">with statements, comprehensions</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">CognitiveDistortionAnalyzer.detect_suicidal_thoughts</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Zainab</td>
            <td style="border: 1px solid #ddd; padding: 8px;">regular expressions</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">CognitiveDistortionAnalyzer.filter_unrealistic_statements</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Zainab</td>
            <td style="border: 1px solid #ddd; padding: 8px;">optional parameters/keyword arguments</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">CognitiveDistortionAnalyzer.save_user_data</td>
            <td style="border: 1px solid #ddd; padding: 8px;">John</td>
            <td style="border: 1px solid #ddd; padding: 8px;">json.dump()</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">CognitiveDistortionAnalyzer.visualize_user_mood_timeline</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Josh</td>
            <td style="border: 1px solid #ddd; padding: 8px;">visualizing data with pyplot</td>
        </tr>
    </tbody>
</table>




```python

```

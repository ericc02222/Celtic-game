import streamlit as st
import random
from PIL import Image
import base64
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Celtic Language Explorer",
    page_icon="🍀",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Celtic Language Explorer\nLearn Celtic languages interactively!"
    }
)

# Define CSS
def local_css():
    st.markdown("""
    <style>
        .main {
            background-color: #1e3d2f;
            color: white;
        }
        .stButton button {
            background-color: #49976d;
            color: white;
            font-weight: bold;
            border-radius: 20px;
            padding: 0.5rem 1rem;
            border: none;
        }
        .stButton button:hover {
            background-color: #3a7857;
        }
        .game-container {
            background-color: #2c5840;
            color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .correct-answer {
            background-color: #2c5840;
            padding: 1rem;
            border-radius: 5px;
            border-left: 5px solid #8bcea0;
            color: white;
        }
        .incorrect-answer {
            background-color: #344d3f;
            padding: 1rem;
            border-radius: 5px;
            border-left: 5px solid #e57373;
            color: white;
        }
        .explanation {
            background-color: #1a4731;
            padding: 1rem;
            border-radius: 5px;
            margin-top: 1rem;
            color: #e0e0e0;
        }
        .level-title {
            color: #8bcea0;
            font-weight: bold;
        }
        .question-counter {
            font-size: 0.9rem;
            color: #555;
            margin-bottom: 1rem;
        }
        .header-container {
            background: linear-gradient(90deg, #1a4731, #0d2419);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .flag-icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }
        .option-button {
            background-color: #3a7857;
            border: 1px solid #49976d;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: background-color 0.3s;
            color: white;
        }
        .option-button:hover {
            background-color: #49976d;
        }
        .score-display {
            font-size: 1.2rem;
            font-weight: bold;
            color: #8bcea0;
            margin-top: 1rem;
        }
        .fun-fact {
            background-color: #1a4731;
            padding: 1rem;
            border-radius: 5px;
            border-left: 5px solid #8bcea0;
            margin-top: 1rem;
            color: #e0e0e0;
        }
    </style>
    """, unsafe_allow_html=True)

# Apply CSS
local_css()

# Game data
LEVELS = [
    {
        "name": "Beginner Irish Gaelic",
        "flag": "🇮🇪",
        "description": "Learn basic Irish Gaelic greetings and phrases",
        "questions": [
            {
                "question": "How do you say 'Hello' in Irish Gaelic?",
                "options": ["Dia duit", "Slán", "Go raibh maith agat", "Cad é sin"],
                "correct_answer": "Dia duit",
                "explanation": "Dia duit (pronounced 'dee-ah gwit') literally means 'God be with you'."
            },
            {
                "question": "What does 'Slán' mean?",
                "options": ["Hello", "Thank you", "Goodbye", "Please"],
                "correct_answer": "Goodbye",
                "explanation": "Slán (pronounced 'slawn') is used to say goodbye."
            },
            {
                "question": "How do you say 'Thank you' in Irish Gaelic?",
                "options": ["Slán", "Dia duit", "Go raibh maith agat", "Tá"],
                "correct_answer": "Go raibh maith agat",
                "explanation": "Go raibh maith agat (pronounced 'guh rev mah ah-gut') literally means 'may you have goodness'."
            }
        ]
    },
    {
        "name": "Intermediate Irish Gaelic",
        "flag": "🇮🇪",
        "description": "Test your knowledge of Irish Gaelic vocabulary",
        "questions": [
            {
                "question": "What is the Irish word for 'water'?",
                "options": ["Bainne", "Uisce", "Arán", "Feoil"],
                "correct_answer": "Uisce",
                "explanation": "Uisce (pronounced 'ish-ka') means water. Interestingly, the word 'whiskey' comes from 'uisce beatha' meaning 'water of life'."
            },
            {
                "question": "What does 'sláinte' mean when making a toast?",
                "options": ["Cheers", "Good luck", "Congratulations", "Good night"],
                "correct_answer": "Cheers",
                "explanation": "Sláinte (pronounced 'slawn-cha') literally means 'health' and is used as 'cheers' when drinking."
            },
            {
                "question": "Which of these means 'I love you' in Irish?",
                "options": ["Tá brón orm", "Tá áthas orm", "Tá grá agam duit", "Cén t-am é"],
                "correct_answer": "Tá grá agam duit",
                "explanation": "Tá grá agam duit (pronounced 'taw graw ah-gum ditch') literally means 'I have love for you'."
            }
        ]
    },
    {
        "name": "Advanced Irish Gaelic",
        "flag": "🇮🇪",
        "description": "Challenge yourself with Irish culture and language connections",
        "questions": [
            {
                "question": "The Irish word 'craic' (pronounced 'crack') refers to:",
                "options": ["A type of bread", "Fun and entertainment", "An ancient weapon", "A traditional dance"],
                "correct_answer": "Fun and entertainment",
                "explanation": "Having 'good craic' means having a good time, with conversation, music, and often drinks."
            },
            {
                "question": "Which of these Irish place names means 'black pool'?",
                "options": ["Dublin", "Galway", "Cork", "Belfast"],
                "correct_answer": "Dublin",
                "explanation": "Dublin (Dubh Linn) comes from 'dubh' meaning black and 'linn' meaning pool, referring to a dark tidal pool where the River Poddle entered the River Liffey."
            },
            {
                "question": "What does the phrase 'Erin go Bragh' mean?",
                "options": ["Ireland forever", "Irish blessing", "Celtic cross", "Irish warrior"],
                "correct_answer": "Ireland forever",
                "explanation": "Erin go Bragh (Éirinn go Brách) means 'Ireland forever' or 'Ireland until the end of time' and became a popular expression of Irish nationalism."
            }
        ]
    },
    {
        "name": "Scottish Gaelic",
        "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
        "description": "Explore another Celtic language: Scottish Gaelic",
        "questions": [
            {
                "question": "How do you say 'Hello' in Scottish Gaelic?",
                "options": ["Dia duit", "Hallo", "Halò", "Dydd da"],
                "correct_answer": "Halò",
                "explanation": "Halò is a simple greeting in Scottish Gaelic. You can also use 'Madainn mhath' (Good morning) or 'Feasgar math' (Good afternoon)."
            },
            {
                "question": "What does 'Alba' mean in Scottish Gaelic?",
                "options": ["White", "Mountain", "Scotland", "River"],
                "correct_answer": "Scotland",
                "explanation": "Alba is the Scottish Gaelic name for Scotland."
            },
            {
                "question": "What does 'Slàinte mhath' mean?",
                "options": ["Good morning", "Good health", "Good luck", "Good night"],
                "correct_answer": "Good health",
                "explanation": "Slàinte mhath (pronounced 'slanj-uh vah') means 'good health' and is used as a toast when drinking."
            }
        ]
    },
    {
        "name": "Welsh",
        "flag": "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
        "description": "Learn basics of the Welsh language",
        "questions": [
            {
                "question": "How do you say 'Good morning' in Welsh?",
                "options": ["Bore da", "Nos da", "Diolch", "Croeso"],
                "correct_answer": "Bore da",
                "explanation": "Bore da (pronounced 'bor-eh dah') is Welsh for 'good morning'."
            },
            {
                "question": "What does 'Cymru' mean?",
                "options": ["Hello", "Wales", "Dragon", "Mountain"],
                "correct_answer": "Wales",
                "explanation": "Cymru is the Welsh name for Wales."
            },
            {
                "question": "What is the meaning of the Welsh word 'hiraeth'?",
                "options": ["Joy", "Courage", "Homesickness/longing", "Celebration"],
                "correct_answer": "Homesickness/longing",
                "explanation": "Hiraeth is a Welsh concept of longing for home, nostalgia, or a sense of belonging that cannot be translated directly into English."
            }
        ]
    },
    {
        "name": "Breton",
        "flag": "🇫🇷",
        "description": "Discover Breton, the Celtic language of Brittany, France",
        "questions": [
            {
                "question": "How do you say 'Hello' in Breton?",
                "options": ["Demat", "Kenavo", "Trugarez", "Diolch"],
                "correct_answer": "Demat",
                "explanation": "Demat (pronounced 'deh-mat') is the standard greeting in Breton."
            },
            {
                "question": "What is Brittany called in the Breton language?",
                "options": ["Bretagne", "Breizh", "Kernow", "Bretaña"],
                "correct_answer": "Breizh",
                "explanation": "Breizh is the Breton name for Brittany, the Celtic region in the northwest of France."
            },
            {
                "question": "Which famous Breton festival celebrates Celtic culture?",
                "options": ["Festival Interceltique", "Fête de la Musique", "Gouel Breizh", "Le Printemps de Bourges"],
                "correct_answer": "Festival Interceltique",
                "explanation": "The Festival Interceltique de Lorient is one of the largest Celtic festivals in the world, celebrating Breton and other Celtic cultures."
            }
        ]
    }
]

# Fun facts about Celtic languages
FUN_FACTS = [
    "There are six Celtic languages still spoken today: Irish, Scottish Gaelic, Welsh, Breton, Cornish, and Manx.",
    "The Celtic languages are divided into two groups: Goidelic (Irish, Scottish Gaelic, Manx) and Brythonic (Welsh, Breton, Cornish).",
    "Welsh has the most speakers of any Celtic language, with approximately 750,000 speakers.",
    "Cornish became extinct in the late 18th century but has been successfully revived since the early 20th century.",
    "Manx, the Celtic language of the Isle of Man, was declared extinct in 1974 but has since been revived.",
    "Irish (Gaeilge) is the first official language of Ireland, with English being the second.",
    "The oldest Celtic language artifacts date back to the 6th century BCE.",
    "Celtic languages use initial consonant mutations, where the first consonant of a word changes in certain grammatical contexts.",
    "The Celtic knot symbolizes the interconnectedness of life and eternity in Celtic culture.",
    "Celtic languages heavily influenced place names across Europe, especially in river names."
]

# Initialize session state variables if they don't exist
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'start'  # start, playing, level_complete, game_complete
if 'current_level' not in st.session_state:
    st.session_state.current_level = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'is_correct' not in st.session_state:
    st.session_state.is_correct = None
if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = sum(len(level["questions"]) for level in LEVELS)
if 'current_fun_fact' not in st.session_state:
    st.session_state.current_fun_fact = random.choice(FUN_FACTS)

# Helper functions
def start_game():
    st.session_state.game_state = 'playing'
    st.session_state.current_level = 0
    st.session_state.score = 0
    st.session_state.current_question = 0
    st.session_state.selected_answer = None
    st.session_state.is_correct = None
    st.session_state.show_explanation = False

def next_question():
    current_level_questions = LEVELS[st.session_state.current_level]["questions"]
    
    # If we've completed all questions in this level
    if st.session_state.current_question >= len(current_level_questions) - 1:
        # If there are more levels
        if st.session_state.current_level < len(LEVELS) - 1:
            st.session_state.game_state = 'level_complete'
        else:
            st.session_state.game_state = 'game_complete'
            st.session_state.current_fun_fact = random.choice(FUN_FACTS)
    else:
        # Move to next question in current level
        st.session_state.current_question += 1
        st.session_state.selected_answer = None
        st.session_state.is_correct = None
        st.session_state.show_explanation = False

def next_level():
    st.session_state.current_level += 1
    st.session_state.current_question = 0
    st.session_state.selected_answer = None
    st.session_state.is_correct = None
    st.session_state.show_explanation = False
    st.session_state.game_state = 'playing'

def check_answer(selected_option):
    current_question_data = LEVELS[st.session_state.current_level]["questions"][st.session_state.current_question]
    is_correct = selected_option == current_question_data["correct_answer"]
    
    st.session_state.selected_answer = selected_option
    st.session_state.is_correct = is_correct
    st.session_state.show_explanation = True
    
    if is_correct:
        st.session_state.score += 1

def restart_game():
    start_game()

# Create celtic-style header image
def get_celtic_header():
    # This is a simplified version, you can replace with actual image
    return """
    <div class="header-container">
        <h1>Celtic Language Explorer</h1>
        <p>Learn Irish, Scottish Gaelic, Welsh, and Breton</p>
        <div style="font-size: 1.5rem;">🍀 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁷󠁬󠁳󠁿 🇮🇪</div>
    </div>
    """

# Game UI based on state
if st.session_state.game_state == 'start':
    # Start screen
    st.markdown(get_celtic_header(), unsafe_allow_html=True)
    
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    st.markdown("## Welcome to the Celtic Language Explorer!")
    st.write("Learn and test your knowledge of Celtic languages through this interactive quiz game.")
    
    st.markdown("### Game Levels:")
    for i, level in enumerate(LEVELS):
        st.markdown(f"**{i+1}. {level['flag']} {level['name']}:** {level['description']}")
    
    st.markdown(f"**Total questions:** {st.session_state.total_questions}")
    
    st.markdown('<div class="fun-fact">', unsafe_allow_html=True)
    st.markdown("**Did you know?**")
    st.write(random.choice(FUN_FACTS))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Start Learning"):
        start_game()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.game_state == 'playing':
    # Playing state
    current_level = LEVELS[st.session_state.current_level]
    current_question_data = current_level["questions"][st.session_state.current_question]
    
    st.markdown(get_celtic_header(), unsafe_allow_html=True)
    
    # Game container
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    
    # Level and question info
    st.markdown(f'<span class="level-title">{current_level["flag"]} Level: {current_level["name"]}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-counter">Question {st.session_state.current_question + 1} of {len(current_level["questions"])}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="score-display">Score: {st.session_state.score}/{st.session_state.total_questions}</div>', unsafe_allow_html=True)
    
    # Question
    st.markdown(f"### {current_question_data['question']}")
    
    # If answer hasn't been selected yet
    if not st.session_state.selected_answer:
        for option in current_question_data['options']:
            if st.button(option, key=option):
                check_answer(option)
                st.rerun()
    
    # If answer has been selected
    else:
        for option in current_question_data['options']:
            if option == current_question_data['correct_answer']:
                st.markdown(f'<div class="correct-answer">{option} ✓</div>', unsafe_allow_html=True)
            elif option == st.session_state.selected_answer and not st.session_state.is_correct:
                st.markdown(f'<div class="incorrect-answer">{option} ✗</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="option-button">{option}</div>', unsafe_allow_html=True)
        
        # Show explanation
        st.markdown(f'<div class="explanation">{current_question_data["explanation"]}</div>', unsafe_allow_html=True)
        
        # Next question button
        if st.button("Next Question"):
            next_question()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.game_state == 'level_complete':
    # Level complete state
    completed_level = LEVELS[st.session_state.current_level]
    next_level_data = LEVELS[st.session_state.current_level + 1]
    
    st.markdown(get_celtic_header(), unsafe_allow_html=True)
    
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    st.markdown(f"## {completed_level['flag']} Level Complete: {completed_level['name']}")
    
    # Calculate questions answered so far
    questions_so_far = sum(len(LEVELS[i]["questions"]) for i in range(st.session_state.current_level + 1))
    
    st.markdown(f'<div class="score-display">Current Score: {st.session_state.score}/{questions_so_far}</div>', unsafe_allow_html=True)
    
    st.markdown(f"### Next Level: {next_level_data['flag']} {next_level_data['name']}")
    st.write(next_level_data['description'])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Continue to Next Level"):
            next_level()
            st.rerun()
    with col2:
        if st.button("Restart Game", key="restart_level"):
            restart_game()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.game_state == 'game_complete':
    # Game complete state
    st.markdown(get_celtic_header(), unsafe_allow_html=True)
    
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    st.markdown("## 🎉 Congratulations! Game Complete!")
    
    st.markdown(f'<div class="score-display">Final Score: {st.session_state.score}/{st.session_state.total_questions}</div>', unsafe_allow_html=True)
    
    # Give feedback based on score
    percentage = (st.session_state.score / st.session_state.total_questions) * 100
    if percentage == 100:
        st.markdown("### Perfect score! You're a Celtic language master! 🏆")
    elif percentage >= 80:
        st.markdown("### Excellent job! You have a strong grasp of Celtic languages! 🌟")
    elif percentage >= 60:
        st.markdown("### Good work! You're well on your way to understanding Celtic languages. 👍")
    else:
        st.markdown("### Good effort! Keep practicing to improve your Celtic language skills. 📚")
    
    st.markdown('<div class="fun-fact">', unsafe_allow_html=True)
    st.markdown("**Did you know?**")
    st.write(st.session_state.current_fun_fact)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Play Again"):
        restart_game()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Add a footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; font-size: 0.8rem; color: #8bcea0;">
    Celtic Language Explorer © 2025<br>
    Created with Streamlit
</div>
""", unsafe_allow_html=True)

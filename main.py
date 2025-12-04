import os
import random
import tkinter as tk

countries = []
score = 0
question_queue = []
question_index = 0
total_questions = 10
current_question = None
current_mode = 'mix up'
MAX_OPTIONS = 4

BASE = os.getcwd()
FACT_FILES = {
    'United States': os.path.join(BASE, 'facts/US.txt'),
    'Japan': os.path.join(BASE, 'facts/JP.txt'),
    'United Kingdom': os.path.join(BASE, 'facts/GB.txt'),
    'Mexico': os.path.join(BASE, 'facts/MX.txt'),
    'Canada': os.path.join(BASE, 'facts/CA.txt'),
    'India': os.path.join(BASE, 'facts/IN.txt'),
    'France': os.path.join(BASE, 'facts/FR.txt'),
    'Turkey': os.path.join(BASE, 'facts/TR.txt'),
    'China': os.path.join(BASE, 'facts/CN.txt'),
    'Saudi Arabia': os.path.join(BASE, 'facts/SA.txt'),
    'Argentina': os.path.join(BASE, 'facts/AR.txt'),
    'Belgium': os.path.join(BASE, 'facts/BE.txt'),
    'South Africa': os.path.join(BASE, 'facts/ZA.txt'),
    'Cuba': os.path.join(BASE, 'facts/CU.txt'),
    'New Zealand': os.path.join(BASE, 'facts/NZ.txt'),
    'Niger': os.path.join(BASE, 'facts/NE.txt'),
    'Greece': os.path.join(BASE, 'facts/GR.txt'),
    'Iraq': os.path.join(BASE, 'facts/IQ.txt'),
    'Bangladesh': os.path.join(BASE, 'facts/BD.txt'),
    'Hong Kong': os.path.join(BASE, 'facts/HK.txt'),
    'Angola': os.path.join(BASE, 'facts/AO.txt'),
    'Bahamas': os.path.join(BASE, 'facts/BS.txt'),
    'Montenegro': os.path.join(BASE, 'facts/ME.txt'),
    'United Arab Emirates': os.path.join(BASE, 'facts/AE.txt'),
    'Jordan': os.path.join(BASE, 'facts/JO.txt'),
    'Nicaragua': os.path.join(BASE, 'facts/NI.txt'),
}
FLAG_IMAGES = {
    'United States': os.path.join(BASE, 'data/easy/US.png'),
    'Japan': os.path.join(BASE, 'data/easy/JP.png'),
    'United Kingdom': os.path.join(BASE, 'data/easy/GB.png'),
    'Mexico': os.path.join(BASE, 'data/easy/MX.png'),
    'Canada': os.path.join(BASE, 'data/easy/CA.png'),
    'India': os.path.join(BASE, 'data/easy/IN.png'),
    'France': os.path.join(BASE, 'data/easy/FR.png'),
    'Turkey': os.path.join(BASE, 'data/standard/TR.png'),
    'China': os.path.join(BASE, 'data/standard/CN.png'),
    'Saudi Arabia': os.path.join(BASE, 'data/standard/SA.png'),
    'Argentina': os.path.join(BASE, 'data/standard/AR.png'),
    'Belgium': os.path.join(BASE, 'data/standard/BE.png'),
    'South Africa': os.path.join(BASE, 'data/standard/ZA.png'),
    'Cuba': os.path.join(BASE, 'data/advanced/CU.png'),
    'New Zealand': os.path.join(BASE, 'data/advanced/NZ.png'),
    'Niger': os.path.join(BASE, 'data/advanced/NE.png'),
    'Greece': os.path.join(BASE, 'data/advanced/GR.png'),
    'Iraq': os.path.join(BASE, 'data/advanced/IQ.png'),
    'Bangladesh': os.path.join(BASE, 'data/advanced/BD.png'),
    'Hong Kong': os.path.join(BASE, 'data/advanced/HK.png'),
    'Angola': os.path.join(BASE, 'data/expert/AO.png'),
    'Bahamas': os.path.join(BASE, 'data/expert/BS.png'),
    'Montenegro': os.path.join(BASE, 'data/expert/ME.png'),
    'United Arab Emirates': os.path.join(BASE, 'data/expert/AE.png'),
    'Jordan': os.path.join(BASE, 'data/expert/JO.png'),
    'Nicaragua': os.path.join(BASE, 'data/expert/NI.png'),
}
EASY = ['United States', 'Japan', 'United Kingdom', 'Mexico', 'Canada', 'India', 'France']
STANDARD = ['Turkey', 'China', 'Saudi Arabia', 'Argentina', 'Belgium', 'South Africa']
ADVANCED = ['Cuba', 'New Zealand', 'Niger', 'Greece', 'Iraq', 'Bangladesh', 'Hong Kong']
EXPERT = ['Angola', 'Bahamas', 'Montenegro', 'United Arab Emirates', 'Jordan', 'Nicaragua']
MODE_GROUPS = {
    'mix up': EASY + STANDARD + ADVANCED + EXPERT,
    'easy': EASY,
    'standard': STANDARD,
    'advanced': ADVANCED,
    'expert': EXPERT,
}


def read_fact(path):
    with open(path, 'r') as file:
        return file.read()


def load_data(choice):
    countries.clear()
    for name in MODE_GROUPS[choice]:
        fact_path = FACT_FILES[name]
        countries.append({'country': name, 'fact': read_fact(fact_path)})


def show_screen(screen):
    screen.tkraise()


def update_score():
    global score
    score += 1
    score_label.config(text='Score: ' + str(score))


def handle_answer(answer):
    global current_question, question_index
    if current_question is None:
        return

    guess = str(answer).strip().lower()
    is_correct = guess == current_question['country'].lower()
    if is_correct:
        update_score()
    if is_correct:
        header = 'Nice job!'
    else:
        header = 'Not quite.'

    message = header + '\n\nCorrect answer: ' + current_question['country'] + '\n\n' + current_question['fact']
    question_index += 1
    show_fact_screen(message)
    current_question = None


def make_answer_handler(value):
    def handler():
        handle_answer(value)
    return handler


def go_back_to_quiz():
    show_screen(quiz_screen)
    ask_question()


def finish_game():
    result_label.config(text='Final Score: ' + str(score) + '/' + str(len(question_queue)))
    show_screen(result_screen)


def resolve_mode():
    desired = mode_entry.get().lower()
    if desired not in MODE_GROUPS:
        return 'mix up'
    return desired


def start_game():
    global score, question_index, current_question, question_queue, current_mode
    chosen_mode = resolve_mode()
    mode_entry.delete(0, tk.END)
    mode_entry.insert(0, chosen_mode)
    current_mode = chosen_mode

    load_data(current_mode)
    score = 0
    question_index = 0
    current_question = None
    total = min(total_questions, len(countries))
    question_queue = random.sample(countries, total)

    score_label.config(text='Score: 0')
    show_screen(quiz_screen)
    ask_question()


def show_flag_picture(name):
    photo = tk.PhotoImage(file=FLAG_IMAGES[name], master=window)
    picture_label.config(image=photo)
    picture_label.image = photo


def show_fact_screen(text):
    fact_message.config(text=text)
    show_screen(fact_screen)


def build_options(correct_country):
    candidates = []
    for entry in countries:
        if entry['country'] != correct_country:
            candidates.append(entry['country'])
    random.shuffle(candidates)
    options = candidates[:max(0, MAX_OPTIONS - 1)]
    insert_at = random.randint(0, len(options))
    options.insert(insert_at, correct_country)
    return options


def ask_question():
    global current_question

    if question_index >= len(question_queue):
        finish_game()
        return

    current_question = question_queue[question_index]
    question_label.config(text='Question ' + str(question_index + 1) + '/' + str(len(question_queue)))

    if current_mode in ('advanced', 'expert'):
        for button in option_buttons:
            button.pack_forget()
        answer_entry.delete(0, tk.END)
        answer_entry.pack(pady=5)
        submit_button.pack(pady=5)
        show_flag_picture(current_question['country'])
        return

    answer_entry.pack_forget()
    submit_button.pack_forget()
    options = build_options(current_question['country'])
    for index in range(len(option_buttons)):
        if index < len(options):
            name = options[index]
            button = option_buttons[index]
            button.config(text=name, state='normal', command=make_answer_handler(name))
            button.pack(pady=5)
        else:
            option_buttons[index].pack_forget()

    show_flag_picture(current_question['country'])


def go_home():
    show_screen(start_screen)


def submit_typing():
    text = answer_entry.get().strip()
    answer_entry.delete(0, tk.END)
    handle_answer(text)


def build_window():
    global window, start_screen, quiz_screen, fact_screen, result_screen
    global question_label, picture_label, option_buttons, score_label, fact_message, result_label
    global answer_entry, submit_button, mode_entry

    window = tk.Tk()
    window.title('Flag-Find Frenzy')
    window.geometry('1000x800')
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    start_screen = tk.Frame(window)
    quiz_screen = tk.Frame(window)
    fact_screen = tk.Frame(window)
    result_screen = tk.Frame(window)

    for frame in (start_screen, quiz_screen, fact_screen, result_screen):
        frame.grid(row=0, column=0, sticky='nsew')
    title = tk.Label(start_screen, text='Flag-Find Frenzy', font=('Arial', 24))
    title.pack(pady=20)
    mode_label = tk.Label(start_screen, text='Type Mode (mix up, easy, standard, advanced, expert)')
    mode_label.pack()
    mode_entry = tk.Entry(start_screen, width=20)
    mode_entry.insert(0, current_mode)
    mode_entry.pack(pady=6)
    picture_label = tk.Label(quiz_screen)
    picture_label.pack(pady=12)
    question_label = tk.Label(quiz_screen, text='Question 0', font=('Arial', 16))
    question_label.pack(pady=10)
    button_frame = tk.Frame(quiz_screen)
    button_frame.pack(pady=15)
    option_buttons = [tk.Button(button_frame, text='', width=30) for _ in range(MAX_OPTIONS)]
    answer_entry = tk.Entry(quiz_screen, width=30)
    submit_button = tk.Button(quiz_screen, text='Submit', command=submit_typing)
    score_label = tk.Label(quiz_screen, text='Score: 0', font=('Arial', 14))
    score_label.pack(pady=8)
    fact_title = tk.Label(fact_screen, text='Fun Fact', font=('Arial', 18))
    fact_title.pack(pady=10)
    fact_message = tk.Label(fact_screen, text='', wraplength=500)
    fact_message.pack(padx=20, pady=15)
    tk.Button(fact_screen, text='Next Question', command=go_back_to_quiz).pack(pady=8)
    result_label = tk.Label(result_screen, text='', font=('Arial', 18))
    result_label.pack(pady=15)
    tk.Button(result_screen, text='Play Again', command=go_home).pack(pady=8)

    def set_mode_and_start():
        start_game()

    tk.Button(start_screen, text='Start', width=20, command=set_mode_and_start).pack(pady=12)

    show_screen(start_screen)
    window.mainloop()
build_window()

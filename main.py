import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
import random
import string
import re

# 🎨 ТЕМЫ
THEMES = {
    'dark': {
        'bg': (0.05, 0.05, 0.08, 1),
        'surface': (0.08, 0.08, 0.12, 1),
        'primary': (0.55, 0.3, 0.95, 1),
        'accent': (0.2, 0.9, 0.7, 1),
        'text': (1, 1, 1, 1),
        'text_secondary': (0.7, 0.7, 0.7, 1),
        'error': (1, 0.3, 0.3, 1)
    },
    'light': {
        'bg': (0.95, 0.95, 0.95, 1),
        'surface': (1, 1, 1, 1),
        'primary': (0.55, 0.3, 0.95, 1),
        'accent': (0.2, 0.9, 0.7, 1),
        'text': (0.1, 0.1, 0.1, 1),
        'text_secondary': (0.4, 0.4, 0.4, 1),
        'error': (1, 0.3, 0.3, 1)
    },
    'gold': {
        'bg': (0.1, 0.08, 0.05, 1),
        'surface': (0.15, 0.12, 0.08, 1),
        'primary': (1, 0.84, 0, 1),
        'accent': (1, 0.6, 0, 1),
        'text': (1, 0.95, 0.7, 1),
        'text_secondary': (0.8, 0.7, 0.4, 1),
        'error': (1, 0.3, 0.3, 1)
    }
}

current_theme = 'dark'

# Данные
users = {}
ranks = {}
friends = {}
private_chats = {}
groups = {}
banned_messages = {}
current_user = None
is_admin = False
is_moderator = False

RANKS = {
    'новичок': 0,
    'обученный': 1,
    'развитый': 2,
    'батя': 3,
    'модератор': 4,
    'админ': 5
}

ADMIN_NICK = "admin"
ADMIN_PHONE = "9094076695"
ADMIN_EMAIL = "izolo"

# Вопросы для обучения
TRAINING_QUESTIONS = [
    {"question": "Что такое никнейм?", "answer": "уникальное имя пользователя"},
    {"question": "Как отправить сообщение?", "answer": "написать текст и нажать отправить"},
    {"question": "Что такое ID пользователя?", "answer": "уникальный номер"},
    {"question": "Как добавить друга?", "answer": "по id"},
    {"question": "Зачем нужны каналы?", "answer": "для общения по интересам"}
]

# Каналы
channels = {
    '🤖 Дипсик AI': [],
    '🔥 Новости VIP': [],
    '🎮 Игровой канал': []
}

# ОТВЕТЫ ДИПСИКА
DIPSIK_ANSWERS = [
    "🤖 Дипсик: Отлично, {}! Продолжай! ✨",
    "🤖 Дипсик: 42 — ответ на твой вопрос, {}! 🚀",
    "🤖 Дипсик: Ты гений, {}! 💎",
    "🤖 Дипсик: Я с тобой, {}! 🤝",
    "🤖 Дипсик: {} задал вопрос уровня богов! 👑"
]

def solve_math(question):
    numbers = re.findall(r'\d+', question)
    if 'сколько' in question.lower() or 'реши' in question.lower() or 'вычисли' in question.lower():
        if '+' in question and len(numbers) >= 2:
            return f"🤖 Дипсик: {numbers[0]} + {numbers[1]} = {int(numbers[0]) + int(numbers[1])} ✨"
        elif '-' in question and len(numbers) >= 2:
            return f"🤖 Дипсик: {numbers[0]} - {numbers[1]} = {int(numbers[0]) - int(numbers[1])} ✨"
        elif '*' in question or '×' in question and len(numbers) >= 2:
            return f"🤖 Дипсик: {numbers[0]} × {numbers[1]} = {int(numbers[0]) * int(numbers[1])} ✨"
        elif '/' in question or '÷' in question and len(numbers) >= 2:
            if int(numbers[1]) != 0:
                return f"🤖 Дипсик: {numbers[0]} ÷ {numbers[1]} = {int(numbers[0]) / int(numbers[1])} ✨"
    return None

# КНОПКИ
class ModernButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = THEMES[current_theme]['text']
        self.font_size = '16sp'
        self.bold = True
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*THEMES[current_theme]['primary'])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15])

class AccentButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = THEMES[current_theme]['text']
        self.font_size = '16sp'
        self.bold = True
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*THEMES[current_theme]['accent'])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15])

class DangerButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = THEMES[current_theme]['text']
        self.font_size = '16sp'
        self.bold = True
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*THEMES[current_theme]['error'])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15])

class ModernTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = THEMES[current_theme]['surface']
        self.foreground_color = THEMES[current_theme]['text']
        self.cursor_color = THEMES[current_theme]['accent']
        self.hint_text_color = THEMES[current_theme]['text_secondary']
        self.padding = [15, 12]
        self.size_hint_y = None
        self.height = 60

# ПРИЛОЖЕНИЕ
class MaxVIPApp(App):
    def build(self):
        Window.clearcolor = THEMES[current_theme]['bg']
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainChatScreen(name='chats'))
        self.sm.add_widget(ChannelChatScreen(name='channel_chat'))
        self.sm.add_widget(PrivateChatScreen(name='private_chat'))
        self.sm.add_widget(TrainingScreen(name='training'))
        self.sm.add_widget(CreateGroupScreen(name='create_group'))
        self.sm.add_widget(CreateChannelScreen(name='create_channel'))
        return self.sm
    
    def apply_theme(self):
        Window.clearcolor = THEMES[current_theme]['bg']
        for screen in self.sm.screens:
            if hasattr(screen, 'reload_ui'):
                screen.reload_ui()

class BaseScreen(Screen):
    def reload_ui(self):
        if hasattr(self, 'build_ui'):
            self.build_ui()

# ЛОГИН
class LoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=[20, 15, 20, 30], spacing=12)
        layout.bind(minimum_height=layout.setter('height'))
        
        title = Label(text='MAX VIP', font_size='42sp', 
                     color=THEMES[current_theme]['primary'], size_hint_y=None, height=70, bold=True)
        layout.add_widget(title)
        
        subtitle = Label(text='ПРЕМИУМ МЕССЕНДЖЕР', font_size='12sp', 
                         color=THEMES[current_theme]['text_secondary'], size_hint_y=None, height=20)
        layout.add_widget(subtitle)
        
        layout.add_widget(Label(size_hint_y=None, height=20))
        
        self.nickname = ModernTextInput(hint_text='Никнейм')
        layout.add_widget(self.nickname)
        
        self.phone = ModernTextInput(hint_text='Номер телефона')
        layout.add_widget(self.phone)
        
        self.email = ModernTextInput(hint_text='Email')
        layout.add_widget(self.email)
        
        layout.add_widget(Label(size_hint_y=None, height=10))
        
        login_btn = AccentButton(text='ВОЙТИ', size_hint_y=None, height=55, font_size='16sp')
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)
        
        register_btn = ModernButton(text='СОЗДАТЬ АККАУНТ', size_hint_y=None, height=55, font_size='16sp')
        register_btn.bind(on_press=self.register)
        layout.add_widget(register_btn)
        
        layout.add_widget(Label(size_hint_y=None, height=10))
        
        admin_btn = DangerButton(text='👑 ВЫ АДМИН?', size_hint_y=None, height=50)
        admin_btn.bind(on_press=self.admin_login)
        layout.add_widget(admin_btn)
        
        moderator_btn = DangerButton(text='🔨 ВЫ МОДЕРАТОР?', size_hint_y=None, height=50)
        moderator_btn.bind(on_press=self.moderator_login)
        layout.add_widget(moderator_btn)
        
        layout.add_widget(Label(size_hint_y=None, height=30))
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
    
    def login(self, instance):
        global current_user
        nick = self.nickname.text.strip()
        
        if nick in users:
            current_user = nick
            self.manager.current = 'chats'
        else:
            popup = Popup(title='Ошибка', content=Label(text='Пользователь не найден'), 
                        size_hint=(0.7, 0.3))
            popup.open()
    
    def register(self, instance):
        global current_user
        nick = self.nickname.text.strip()
        phone = self.phone.text.strip()
        email = self.email.text.strip()
        
        if not nick or not phone or not email:
            popup = Popup(title='Ошибка', content=Label(text='Заполни все поля'), 
                        size_hint=(0.7, 0.3))
            popup.open()
            return
        
        if nick in users:
            popup = Popup(title='Ошибка', content=Label(text='Ник уже занят'), 
                        size_hint=(0.7, 0.3))
            popup.open()
            return
        
        user_id = str(random.randint(1000, 9999))
        users[nick] = {'id': user_id, 'phone': phone, 'email': email}
        ranks[nick] = 'новичок'
        
        if nick not in friends:
            friends[nick] = []
        
        current_user = nick
        
        if ranks[nick] == 'новичок':
            self.manager.current = 'training'
        else:
            self.manager.current = 'chats'
    
    def admin_login(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        nick_input = ModernTextInput(hint_text='Никнейм админа', size_hint_y=None, height=50)
        phone_input = ModernTextInput(hint_text='Телефон', size_hint_y=None, height=50)
        email_input = ModernTextInput(hint_text='Email', size_hint_y=None, height=50)
        result_label = Label(text='', color=THEMES[current_theme]['text'], size_hint_y=None, height=60)
        
        def check_admin(btn):
            global is_admin, current_user
            if (nick_input.text.strip() == ADMIN_NICK and 
                phone_input.text.strip() == ADMIN_PHONE and 
                email_input.text.strip() == ADMIN_EMAIL):
                is_admin = True
                if ADMIN_NICK not in users:
                    users[ADMIN_NICK] = {'id': '0000', 'phone': ADMIN_PHONE, 'email': ADMIN_EMAIL}
                if ADMIN_NICK not in friends:
                    friends[ADMIN_NICK] = []
                ranks[ADMIN_NICK] = 'админ'
                current_user = ADMIN_NICK
                popup.dismiss()
                self.manager.current = 'chats'
            else:
                result_label.text = '❌ Неверные данные'
        
        login_btn = ModernButton(text='Войти как админ', size_hint_y=None, height=50)
        login_btn.bind(on_press=check_admin)
        close_btn = DangerButton(text='Закрыть', size_hint_y=None, height=50)
        
        content.add_widget(nick_input)
        content.add_widget(phone_input)
        content.add_widget(email_input)
        content.add_widget(login_btn)
        content.add_widget(result_label)
        content.add_widget(close_btn)
        
        popup = Popup(title='Вход для админа', content=content, size_hint=(0.9, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def moderator_login(self, instance):
        global is_moderator, current_user
        nick = self.nickname.text.strip()
        if nick in users and ranks.get(nick) == 'модератор':
            is_moderator = True
            current_user = nick
            self.manager.current = 'chats'
        else:
            popup = Popup(title='Ошибка', content=Label(text='Вы не модератор'), 
                        size_hint=(0.7, 0.3))
            popup.open()

# ОБУЧЕНИЕ - ИСПРАВЛЕНО
class TrainingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_q = 0
        self.correct = 0
    
    def on_enter(self):
        self.current_q = 0
        self.correct = 0
        self.build_ui()
    
    def reload_ui(self):
        # НЕ ПЕРЕЗАГРУЖАЕМ ВОПРОСЫ ПРИ СМЕНЕ ТЕМЫ
        pass
    
    def build_ui(self):
        self.clear_widgets()
        
        # ПРОВЕРКА ЧТО ВОПРОСЫ ЕЩЕ ЕСТЬ
        if self.current_q >= len(TRAINING_QUESTIONS):
            self.finish_training()
            return
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(text=f'ОБУЧЕНИЕ\nВопрос {self.current_q + 1}/{len(TRAINING_QUESTIONS)}', 
                     font_size='20sp', color=THEMES[current_theme]['primary'], bold=True,
                     size_hint_y=None, height=80)
        layout.add_widget(title)
        
        q_label = Label(text=TRAINING_QUESTIONS[self.current_q]['question'], 
                       font_size='16sp', color=THEMES[current_theme]['text'],
                       size_hint_y=None, height=60)
        layout.add_widget(q_label)
        
        self.answer_input = ModernTextInput(hint_text='Введите ответ')
        layout.add_widget(self.answer_input)
        
        submit_btn = ModernButton(text='ОТВЕТИТЬ', size_hint_y=None, height=55)
        submit_btn.bind(on_press=self.check_answer)
        layout.add_widget(submit_btn)
        
        self.add_widget(layout)
    
    def check_answer(self, instance):
        answer = self.answer_input.text.strip().lower()
        correct = TRAINING_QUESTIONS[self.current_q]['answer'].lower()
        
        if answer == correct or correct in answer or answer in correct:
            self.correct += 1
        
        self.current_q += 1
        
        if self.current_q >= len(TRAINING_QUESTIONS):
            self.finish_training()
        else:
            self.build_ui()
    
    def finish_training(self):
        if self.correct >= 3:
            ranks[current_user] = 'обученный'
            popup = Popup(title='Поздравляем!', 
                        content=Label(text=f'Вы прошли обучение!\nПравильных ответов: {self.correct}/{len(TRAINING_QUESTIONS)}\nВаш ранг повышен до "обученный"!'),
                        size_hint=(0.8, 0.5))
            popup.open()
        else:
            popup = Popup(title='Не сдал', 
                        content=Label(text=f'Вы не прошли обучение.\nПравильных ответов: {self.correct}/{len(TRAINING_QUESTIONS)}\nПопробуйте еще раз!'),
                        size_hint=(0.8, 0.5))
            popup.open()
        
        self.manager.current = 'chats'

# СОЗДАНИЕ ГРУППЫ
class CreateGroupScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(text='СОЗДАТЬ ГРУППУ', font_size='24sp', 
                     color=THEMES[current_theme]['primary'], bold=True,
                     size_hint_y=None, height=60)
        layout.add_widget(title)
        
        self.group_name = ModernTextInput(hint_text='Название группы')
        layout.add_widget(self.group_name)
        
        create_btn = ModernButton(text='СОЗДАТЬ', size_hint_y=None, height=55)
        create_btn.bind(on_press=self.create_group)
        layout.add_widget(create_btn)
        
        back_btn = DangerButton(text='НАЗАД', size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def create_group(self, instance):
        name = self.group_name.text.strip()
        if name and name not in groups:
            groups[name] = {'owner': current_user, 'members': [current_user], 'messages': []}
            popup = Popup(title='Успех', content=Label(text=f'Группа "{name}" создана!'),
                        size_hint=(0.7, 0.3))
            popup.open()
            self.manager.current = 'chats'
    
    def go_back(self, instance):
        self.manager.current = 'chats'

# СОЗДАНИЕ КАНАЛА
class CreateChannelScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(text='СОЗДАТЬ КАНАЛ', font_size='24sp', 
                     color=THEMES[current_theme]['primary'], bold=True,
                     size_hint_y=None, height=60)
        layout.add_widget(title)
        
        self.channel_name = ModernTextInput(hint_text='Название канала')
        layout.add_widget(self.channel_name)
        
        create_btn = ModernButton(text='СОЗДАТЬ', size_hint_y=None, height=55)
        create_btn.bind(on_press=self.create_channel)
        layout.add_widget(create_btn)
        
        back_btn = DangerButton(text='НАЗАД', size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def create_channel(self, instance):
        name = self.channel_name.text.strip()
        if name and name not in channels:
            channels[name] = []
            popup = Popup(title='Успех', content=Label(text=f'Канал "{name}" создан!'),
                        size_hint=(0.7, 0.3))
            popup.open()
            self.manager.current = 'chats'
    
    def go_back(self, instance):
        self.manager.current = 'chats'

# ОСНОВНОЙ ЭКРАН ЧАТОВ
class MainChatScreen(BaseScreen):
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=[0, 0, 0, 0])
        
        top_bar = BoxLayout(size_hint_y=None, height=70, padding=[15, 10], spacing=10)
        top_bar.canvas.before.clear()
        with top_bar.canvas.before:
            Color(*THEMES[current_theme]['surface'])
            Rectangle(pos=top_bar.pos, size=top_bar.size)
        
        menu_btn = ModernButton(text='☰', size_hint_x=None, width=55)
        menu_btn.bind(on_press=self.open_settings_menu)
        top_bar.add_widget(menu_btn)
        
        title = Label(text='ЧАТЫ', font_size='22sp', color=THEMES[current_theme]['text'], bold=True)
        top_bar.add_widget(title)
        
        layout.add_widget(top_bar)
        
        scroll = ScrollView()
        chat_list = GridLayout(cols=1, spacing=12, size_hint_y=None, padding=[15, 10])
        chat_list.bind(minimum_height=chat_list.setter('height'))
        
        global is_admin, is_moderator, current_user
        
        if ranks.get(current_user) == 'новичок':
            training_btn = AccentButton(text='📚 ЧАТ ОБУЧЕНИЕ (обязательно)', size_hint_y=None, height=60)
            training_btn.bind(on_press=self.open_training)
            chat_list.add_widget(training_btn)
        
        channels_title = Label(text='КАНАЛЫ', color=THEMES[current_theme]['accent'], 
                               size_hint_y=None, height=40, bold=True)
        chat_list.add_widget(channels_title)
        
        for channel in channels.keys():
            channel_btn = ModernButton(text=channel, size_hint_y=None, height=55)
            channel_btn.bind(on_press=lambda x, c=channel: self.open_channel(c))
            chat_list.add_widget(channel_btn)
        
        if groups:
            groups_title = Label(text='ГРУППЫ', color=THEMES[current_theme]['accent'], 
                                 size_hint_y=None, height=40, bold=True)
            chat_list.add_widget(groups_title)
            for group in groups.keys():
                group_btn = ModernButton(text=f'👥 {group}', size_hint_y=None, height=55)
                group_btn.bind(on_press=lambda x, g=group: self.open_group(g))
                chat_list.add_widget(group_btn)
        
        if current_user and current_user in friends and len(friends[current_user]) > 0:
            friends_title = Label(text='ЛИЧНЫЕ ЧАТЫ', color=THEMES[current_theme]['accent'], 
                                 size_hint_y=None, height=40, bold=True)
            chat_list.add_widget(friends_title)
            for friend in friends[current_user]:
                friend_btn = ModernButton(text=f'💬 {friend}', size_hint_y=None, height=55)
                friend_btn.bind(on_press=lambda x, f=friend: self.open_private_chat(f))
                chat_list.add_widget(friend_btn)
        
        add_friend_btn = AccentButton(text='➕ ДОБАВИТЬ ДРУГА ПО ID', size_hint_y=None, height=50)
        add_friend_btn.bind(on_press=self.add_friend_dialog)
        chat_list.add_widget(add_friend_btn)
        
        create_group_btn = AccentButton(text='👥 СОЗДАТЬ ГРУППУ', size_hint_y=None, height=50)
        create_group_btn.bind(on_press=self.go_to_create_group)
        chat_list.add_widget(create_group_btn)
        
        create_channel_btn = AccentButton(text='📢 СОЗДАТЬ КАНАЛ', size_hint_y=None, height=50)
        create_channel_btn.bind(on_press=self.go_to_create_channel)
        chat_list.add_widget(create_channel_btn)
        
        logout_btn = DangerButton(text='🚪 ВЫЙТИ', size_hint_y=None, height=50)
        logout_btn.bind(on_press=self.logout)
        chat_list.add_widget(logout_btn)
        
        scroll.add_widget(chat_list)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def open_settings_menu(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        theme_btn = ModernButton(text='🎨 СМЕНИТЬ ТЕМУ', size_hint_y=None, height=50)
        theme_btn.bind(on_press=self.change_theme)
        content.add_widget(theme_btn)
        
        id_btn = ModernButton(text='Узнать мой ID', size_hint_y=None, height=50)
        id_btn.bind(on_press=self.show_my_id)
        content.add_widget(id_btn)
        
        profile_btn = ModernButton(text='Профиль аккаунта', size_hint_y=None, height=50)
        profile_btn.bind(on_press=self.show_profile)
        content.add_widget(profile_btn)
        
        if is_admin:
            ranks_btn = ModernButton(text='Управление рангами', size_hint_y=None, height=50)
            ranks_btn.bind(on_press=self.manage_ranks)
            content.add_widget(ranks_btn)
            
            peach_btn = ModernButton(text='🍑 ПЕРСИК ПОЛЬЗОВАТЕЛЮ', size_hint_y=None, height=50)
            peach_btn.bind(on_press=self.show_peach_to_user)
            content.add_widget(peach_btn)
        
        close_btn = DangerButton(text='Закрыть', size_hint_y=None, height=50)
        content.add_widget(close_btn)
        
        popup = Popup(title='МЕНЮ', content=content, size_hint=(0.85, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_peach_to_user(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        id_input = ModernTextInput(hint_text='Введите ID пользователя', size_hint_y=None, height=50)
        peach_url = "https://i.imgur.com/8KmQrXj.png"
        
        result_label = Label(text='', color=THEMES[current_theme]['text'], size_hint_y=None, height=50)
        image_widget = AsyncImage(source=peach_url, size_hint_y=None, height=200)
        image_widget.opacity = 0
        
        def show_peach(btn):
            user_id = id_input.text.strip()
            found = None
            for nick, data in users.items():
                if data['id'] == user_id:
                    found = nick
                    break
            
            if found:
                result_label.text = f'✅ Персик отправлен пользователю {found}! 🍑'
                image_widget.opacity = 1
            else:
                result_label.text = '❌ Пользователь не найден'
                image_widget.opacity = 0
        
        show_btn = ModernButton(text='🍑 ПОКАЗАТЬ ПЕРСИК', size_hint_y=None, height=50)
        show_btn.bind(on_press=show_peach)
        
        close_btn = DangerButton(text='Закрыть', size_hint_y=None, height=50)
        
        content.add_widget(Label(text='🍑 АДМИН ПАНЕЛЬ ПЕРСИКА 🍑', 
                                color=THEMES[current_theme]['accent'], 
                                size_hint_y=None, height=50, bold=True, font_size='18sp'))
        content.add_widget(id_input)
        content.add_widget(show_btn)
        content.add_widget(result_label)
        content.add_widget(image_widget)
        content.add_widget(close_btn)
        
        popup = Popup(title='🍑 АДМИН ПАНЕЛЬ', content=content, size_hint=(0.9, 0.85))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def change_theme(self, instance):
        global current_theme
        themes = ['dark', 'light', 'gold']
        current_index = themes.index(current_theme)
        current_theme = themes[(current_index + 1) % 3]
        app = App.get_running_app()
        app.apply_theme()
    
    def open_training(self, instance):
        self.manager.current = 'training'
    
    def open_channel(self, channel_name):
        screen = self.manager.get_screen('channel_chat')
        screen.channel_name = channel_name
        self.manager.current = 'channel_chat'
    
    def open_group(self, group_name):
        screen = self.manager.get_screen('channel_chat')
        screen.channel_name = group_name
        self.manager.current = 'channel_chat'
    
    def open_private_chat(self, friend):
        screen = self.manager.get_screen('private_chat')
        screen.friend_name = friend
        self.manager.current = 'private_chat'
    
    def go_to_create_group(self, instance):
        self.manager.current = 'create_group'
    
    def go_to_create_channel(self, instance):
        self.manager.current = 'create_channel'
    
    def show_my_id(self, instance):
        popup = Popup(title='Ваш ID', content=Label(text=str(users[current_user]['id']), color=THEMES[current_theme]['text']), 
                     size_hint=(0.5, 0.3))
        popup.open()
    
    def show_profile(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        info = f"🆔 ПРОФИЛЬ\n\nНикнейм: {current_user}\nID: {users[current_user]['id']}\nРанг: {ranks.get(current_user, 'новичок')}"
        label = Label(text=info, font_size='16sp', color=THEMES[current_theme]['text'])
        content.add_widget(label)
        close_btn = ModernButton(text='Закрыть', size_hint_y=None, height=50)
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        popup = Popup(title='Профиль', content=content, size_hint=(0.8, 0.5))
        popup.open()
    
    def manage_ranks(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        search_input = ModernTextInput(hint_text='Введите никнейм', size_hint_y=None, height=50)
        result_label = Label(text='', color=THEMES[current_theme]['text'], size_hint_y=None, height=60)
        
        dropdown = DropDown()
        for rank in ['обученный', 'развитый', 'батя', 'модератор']:
            btn = Button(text=rank.capitalize(), size_hint_y=None, height=40, 
                        background_color=THEMES[current_theme]['surface'], color=THEMES[current_theme]['text'])
            btn.bind(on_release=lambda btn: dropdown.select(btn.text.lower()))
            dropdown.add_widget(btn)
        
        main_btn = ModernButton(text='Выбрать ранг', size_hint_y=None, height=50)
        main_btn.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(main_btn, 'text', x.capitalize()))
        
        def change_rank(btn):
            nick = search_input.text.strip()
            selected_rank = main_btn.text.lower()
            if nick in users:
                ranks[nick] = selected_rank
                result_label.text = f'✅ Ранг {nick} изменён на "{selected_rank}"!'
            else:
                result_label.text = '❌ Пользователь не найден'
        
        apply_btn = AccentButton(text='ПРИМЕНИТЬ', size_hint_y=None, height=50)
        apply_btn.bind(on_press=change_rank)
        close_btn = DangerButton(text='Закрыть', size_hint_y=None, height=50)
        
        content.add_widget(search_input)
        content.add_widget(main_btn)
        content.add_widget(apply_btn)
        content.add_widget(result_label)
        content.add_widget(close_btn)
        
        popup = Popup(title='Управление рангами', content=content, size_hint=(0.9, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def add_friend_dialog(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        search_input = ModernTextInput(hint_text='Введите ID друга', size_hint_y=None, height=50)
        result_label = Label(text='', color=THEMES[current_theme]['text'], size_hint_y=None, height=60)
        
        def add_friend(btn):
            friend_id = search_input.text.strip()
            found = None
            for nick, data in users.items():
                if data['id'] == friend_id and nick != current_user:
                    found = nick
                    break
            
            if found:
                if current_user not in friends:
                    friends[current_user] = []
                if found not in friends[current_user]:
                    friends[current_user].append(found)
                    chat_key = f"{min(current_user, found)}_{max(current_user, found)}"
                    if chat_key not in private_chats:
                        private_chats[chat_key] = []
                    result_label.text = f'✅ {found} добавлен в друзья!'
                    self.build_ui()
                else:
                    result_label.text = '❌ Уже в друзьях'
            else:
                result_label.text = '❌ Пользователь не найден'
        
        search_btn = AccentButton(text='ДОБАВИТЬ', size_hint_y=None, height=50)
        search_btn.bind(on_press=add_friend)
        close_btn = DangerButton(text='Закрыть', size_hint_y=None, height=50)
        
        content.add_widget(search_input)
        content.add_widget(search_btn)
        content.add_widget(result_label)
        content.add_widget(close_btn)
        
        popup = Popup(title='Добавить друга', content=content, size_hint=(0.9, 0.5))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def logout(self, instance):
        global current_user, is_admin, is_moderator
        current_user = None
        is_admin = False
        is_moderator = False
        self.manager.current = 'login'

# КАНАЛЫ
class ChannelChatScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.channel_name = ''
    
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical')
        
        top_bar = BoxLayout(size_hint_y=None, height=60, padding=[10, 5])
        top_bar.canvas.before.clear()
        with top_bar.canvas.before:
            Color(*THEMES[current_theme]['surface'])
            Rectangle(pos=top_bar.pos, size=top_bar.size)
        
        back_btn = ModernButton(text='←', size_hint_x=None, width=60)
        back_btn.bind(on_press=self.go_back)
        
        title = Label(text=self.channel_name[:20] if self.channel_name else 'Чат', 
                     font_size='18sp', color=THEMES[current_theme]['text'], bold=True)
        
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title)
        layout.add_widget(top_bar)
        
        scroll = ScrollView()
        chat_history = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[15, 10])
        chat_history.bind(minimum_height=chat_history.setter('height'))
        
        if self.channel_name not in channels:
            channels[self.channel_name] = []
        
        for msg in channels[self.channel_name]:
            if msg not in banned_messages:
                lbl = Label(text=msg, markup=True, color=THEMES[current_theme]['text'],
                           size_hint_y=None, height=60, text_size=(Window.width - 50, None))
                chat_history.add_widget(lbl)
        
        input_layout = BoxLayout(size_hint_y=None, height=70, padding=[10, 5], spacing=10)
        self.input_msg = ModernTextInput(hint_text='Введите сообщение...', size_hint_x=0.8, height=55)
        send_btn = ModernButton(text='➤', size_hint_x=None, width=70)
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.input_msg)
        input_layout.add_widget(send_btn)
        chat_history.add_widget(input_layout)
        scroll.add_widget(chat_history)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def send_message(self, instance):
        text = self.input_msg.text.strip()
        if not text or not current_user:
            return
        
        if self.channel_name not in channels:
            channels[self.channel_name] = []
        
        msg = f'[b]{current_user}:[/b] {text}'
        
        if msg in banned_messages:
            return
        
        channels[self.channel_name].append(msg)
        
        if self.channel_name == '🤖 Дипсик AI':
            math_answer = solve_math(text)
            if math_answer:
                channels[self.channel_name].append(math_answer)
            else:
                answer = random.choice(DIPSIK_ANSWERS).format(current_user)
                channels[self.channel_name].append(answer)
        elif self.channel_name == '🔥 Новости VIP':
            answer = f"📰 Новости VIP: Спасибо за новость, {current_user}! ✅"
            channels[self.channel_name].append(answer)
        elif self.channel_name == '🎮 Игровой канал':
            answer = f"🎮 Игровой канал: Отличный геймплей, {current_user}! 🎮"
            channels[self.channel_name].append(answer)
        
        self.input_msg.text = ''
        self.build_ui()
    
    def go_back(self, instance):
        self.manager.current = 'chats'

# ЛИЧНЫЙ ЧАТ
class PrivateChatScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.friend_name = ''
    
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical')
        
        top_bar = BoxLayout(size_hint_y=None, height=60, padding=[10, 5])
        top_bar.canvas.before.clear()
        with top_bar.canvas.before:
            Color(*THEMES[current_theme]['surface'])
            Rectangle(pos=top_bar.pos, size=top_bar.size)
        
        back_btn = ModernButton(text='←', size_hint_x=None, width=60)
        back_btn.bind(on_press=self.go_back)
        
        title = Label(text=self.friend_name, font_size='18sp', color=THEMES[current_theme]['text'], bold=True)
        
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title)
        layout.add_widget(top_bar)
        
        scroll = ScrollView()
        chat_history = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[15, 10])
        chat_history.bind(minimum_height=chat_history.setter('height'))
        
        chat_key = f"{min(current_user, self.friend_name)}_{max(current_user, self.friend_name)}"
        if chat_key in private_chats:
            for msg in private_chats[chat_key]:
                if msg not in banned_messages:
                    lbl = Label(text=msg, markup=True, color=THEMES[current_theme]['text'],
                               size_hint_y=None, height=60, text_size=(Window.width - 50, None))
                    chat_history.add_widget(lbl)
        
        if is_moderator or is_admin:
            ban_btn = DangerButton(text='🚫 ЗАБАНИТЬ СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЯ', size_hint_y=None, height=50)
            ban_btn.bind(on_press=self.ban_user_messages)
            chat_history.add_widget(ban_btn)
        
        input_layout = BoxLayout(size_hint_y=None, height=70, padding=[10, 5], spacing=10)
        self.input_msg = ModernTextInput(hint_text='Введите сообщение...', size_hint_x=0.8, height=55)
        send_btn = ModernButton(text='➤', size_hint_x=None, width=70)
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.input_msg)
        input_layout.add_widget(send_btn)
        chat_history.add_widget(input_layout)
        scroll.add_widget(chat_history)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def ban_user_messages(self, instance):
        chat_key = f"{min(current_user, self.friend_name)}_{max(current_user, self.friend_name)}"
        if chat_key in private_chats:
            for msg in private_chats[chat_key]:
                banned_messages[msg] = True
            popup = Popup(title='Бан', content=Label(text=f'Сообщения от {self.friend_name} забанены!'),
                        size_hint=(0.7, 0.3))
            popup.open()
            self.build_ui()
    
    def send_message(self, instance):
        text = self.input_msg.text.strip()
        if not text or not current_user or not self.friend_name:
            return
        
        chat_key = f"{min(current_user, self.friend_name)}_{max(current_user, self.friend_name)}"
        if chat_key not in private_chats:
            private_chats[chat_key] = []
        
        msg = f'[b]{current_user}:[/b] {text}'
        
        if msg in banned_messages:
            return
        
        private_chats[chat_key].append(msg)
        self.input_msg.text = ''
        self.build_ui()
    
    def go_back(self, instance):
        self.manager.current = 'chats'

if __name__ == '__main__':
    MaxVIPApp().run()

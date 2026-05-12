import customtkinter as ctk
import random
import webbrowser
from tkinter import messagebox

# UI Sozlamalari
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class EnglifayPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RoboEnglish: Englifay Edition")
        self.geometry("1000x700")
        
        # 1. KATTA LUG'AT (Bu yerga minglab so'zlarni qo'shish mumkin)
        # Amalda buni .json yoki .txt fayldan yuklash to'g'riroq bo'ladi
        self.words_db = [
            {"en": "Accomplish", "uz": "Muvaffaqiyatli yakunlash", "ex": "You can accomplish anything."},
            {"en": "Brave", "uz": "Jasur", "ex": "He is a brave soldier."},
            {"en": "Curiosity", "uz": "Qiziquvchanlik", "ex": "Curiosity leads to knowledge."},
            {"en": "Determine", "uz": "Aniqlamoq / Qaror qilmoq", "ex": "We need to determine the cause."},
            {"en": "Enthusiasm", "uz": "G'ayrat / Ishtiyoq", "ex": "She has a lot of enthusiasm."},
            {"en": "Flexible", "uz": "Moslashuvchan", "ex": "My schedule is flexible."},
            {"en": "Grateful", "uz": "Minnatdor", "ex": "I am grateful for your help."},
            {"en": "Hesitate", "uz": "Ikkilanmoq", "ex": "Don't hesitate to ask."},
            {"en": "Inspire", "uz": "Ilhomlantirmoq", "ex": "You inspire me."},
            {"en": "Justice", "uz": "Adolat", "ex": "We seek justice for all."},
            # ... bu yerga yana 5000 ta so'z qo'shish mumkin
        ]
        
        self.user_data = {"xp": 0, "level": 1, "streak": 0}
        self.create_layout()

    def create_layout(self):
        # Chap tomondagi Navigation Bar (Modern Side Menu)
        self.nav_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1A1A1A")
        self.nav_frame.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(self.nav_frame, text="ENGLIFAY", font=("Poppins", 28, "bold"), text_color="#58CC02")
        self.logo.pack(pady=30)

        # Navigatsiya tugmalari
        self.btn_home = self.nav_button("🏠 ASOSIY", self.show_home)
        self.btn_test = self.nav_button("⚡ MASHQLAR", self.start_practice)
        self.btn_video = self.nav_button("📺 VIDEOLAR", self.show_videos)
        self.btn_profile = self.nav_button("👤 PROFIL", self.show_profile)

        # Asosiy ishchi maydon
        self.content_frame = ctk.CTkFrame(self, fg_color="#121212", corner_radius=20)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.show_home()

    def nav_button(self, text, command):
        btn = ctk.CTkButton(self.nav_frame, text=text, fg_color="transparent", 
                            text_color="white", hover_color="#2D2D2D", 
                            anchor="w", font=("Arial", 14, "bold"),
                            height=45, command=command)
        btn.pack(fill="x", padx=15, pady=5)
        return btn

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # --- EKRANLAR ---

    def show_home(self):
        self.clear_content()
        lbl = ctk.CTkLabel(self.content_frame, text="Xush kelibsiz, Student!", font=("Arial", 32, "bold"))
        lbl.pack(pady=(40, 10))

        sub_lbl = ctk.CTkLabel(self.content_frame, text="Bugungi o'rganish rejangiz tayyor.", font=("Arial", 16), text_color="gray")
        sub_lbl.pack(pady=10)

        # Daily Goal Card
        card = ctk.CTkFrame(self.content_frame, fg_color="#1E1E1E", corner_radius=15, height=150)
        card.pack(fill="x", padx=40, pady=30)
        
        ctk.CTkLabel(card, text="KUNLIK MAQSAD", font=("Arial", 12, "bold"), text_color="#58CC02").pack(pady=(15, 0))
        self.xp_progress = ctk.CTkProgressBar(card, width=400, progress_color="#58CC02")
        self.xp_progress.set(self.user_data["xp"] / 1000)
        self.xp_progress.pack(pady=20)
        
        ctk.CTkLabel(card, text=f"{self.user_data['xp']} / 1000 XP", font=("Arial", 14)).pack(pady=(0, 15))

    def start_practice(self):
        self.clear_content()
        self.current_word = random.choice(self.words_db)

        # Savol maydoni
        quest_card = ctk.CTkFrame(self.content_frame, fg_color="#1E1E1E", corner_radius=20, width=500, height=250)
        quest_card.pack(pady=40, padx=40)
        quest_card.pack_propagate(False)

        ctk.CTkLabel(quest_card, text="USHBU SO'ZNI TARJIMA QILING:", font=("Arial", 14), text_color="#A0A0A0").pack(pady=20)
        ctk.CTkLabel(quest_card, text=self.current_word["en"], font=("Arial", 48, "bold"), text_color="white").pack()
        
        # Misol (Example sentence)
        ctk.CTkLabel(quest_card, text=f"Context: {self.current_word['ex']}", font=("Arial", 12, "italic"), text_color="#58CC02").pack(pady=10)

        # Input
        self.ans_entry = ctk.CTkEntry(self.content_frame, width=400, height=55, placeholder_text="Javobni yozing...", 
                                      font=("Arial", 18), corner_radius=10, border_color="#58CC02", justify="center")
        self.ans_entry.pack(pady=20)
        self.ans_entry.focus()

        self.bind('<Return>', lambda e: self.check_answer())

        btn_check = ctk.CTkButton(self.content_frame, text="TEKSHIRISH", width=200, height=50, 
                                  fg_color="#58CC02", hover_color="#46A302", font=("Arial", 16, "bold"),
                                  command=self.check_answer)
        btn_check.pack(pady=10)

    def check_answer(self):
        user_ans = self.ans_entry.get().strip().lower()
        if user_ans == self.current_word["uz"].lower():
            self.user_data["xp"] += 50
            self.start_practice() # To'g'ri bo'lsa darhol keyingisiga
        else:
            # Xato bo'lsa pastda qizil bildirishnoma chiqarish mumkin
            self.start_practice()

    def show_videos(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="VIDEO DARSLAR (YOUTUBE)", font=("Arial", 26, "bold")).pack(pady=30)
        
        channels = [
            ("🎬 Beginner Grammar (English with Lucy)", "https://www.youtube.com/@EnglishwithLucy"),
            ("🎧 Daily Listening (BBC Learning)", "https://www.youtube.com/@bbclearningenglish"),
            ("🗣️ Speaking Secrets (Learn English with TV)", "https://www.youtube.com/@LearnEnglishWithTVSeries")
        ]

        for name, url in channels:
            v_btn = ctk.CTkButton(self.content_frame, text=name, width=500, height=60, 
                                  fg_color="#2D2D2D", anchor="w", padx=20,
                                  command=lambda u=url: webbrowser.open(u))
            v_btn.pack(pady=10)

    def show_profile(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="PROFIL STATISTIKASI", font=("Arial", 28, "bold")).pack(pady=30)
        
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=100)

        def create_stat_box(parent, title, value):
            box = ctk.CTkFrame(parent, fg_color="#1E1E1E", width=150, height=100, corner_radius=15)
            box.pack(side="left", padx=10, expand=True)
            ctk.CTkLabel(box, text=title, font=("Arial", 12), text_color="gray").pack(pady=(15,0))
            ctk.CTkLabel(box, text=value, font=("Arial", 24, "bold"), text_color="#58CC02").pack(pady=10)

        create_stat_box(stats_frame, "UMUMIY XP", str(self.user_data["xp"]))
        create_stat_box(stats_frame, "DARAJA", str(self.user_data["level"]))
        create_stat_box(stats_frame, "STREAK", str(self.user_data["streak"]) + " kun")

if __name__ == "__main__":
    app = EnglifayPro()
    app.mainloop()
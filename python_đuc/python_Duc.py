import tkinter as tk                     # Thư viện giao diện đồ họa
from tkinter import messagebox           # Hộp thoại thông báo lỗi/thông tin
import random                            # Để chọn từ ngẫu nhiên
import sys                               # Để thoát chương trình khi có lỗi

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Trò Chơi Hangman")   # Tiêu đề cửa sổ
        self.words = self.load_words()        # Tải danh sách từ từ file

        # Nếu không có từ nào, thoát chương trình
        if self.words is None:
            sys.exit(1)

        self.reset_game()  # Bắt đầu trò chơi mới

        # ======================== Giao diện ===========================

        # Hiển thị từ đang chơi với các chữ cái ẩn
        self.word_label = tk.Label(root, text=self.display_word(), font=("Arial", 24))
        self.word_label.pack(pady=20)

        # Hiển thị số lần đoán sai
        self.error_label = tk.Label(root, text=f"Số lần đoán sai: {self.errors}/6", font=("Arial", 14))
        self.error_label.pack()

        # Khung vẽ người treo cổ
        self.canvas = tk.Canvas(root, width=200, height=200)
        self.canvas.pack(pady=20)
        self.draw_hangman()

        # Ô nhập chữ cái đoán
        self.entry = tk.Entry(root, width=5, font=("Arial", 14))
        self.entry.pack()
        self.entry.bind("<Return>", self.process_guess)  # Nhấn Enter để đoán

        # Nút đoán chữ
        self.guess_button = tk.Button(root, text="Đoán", command=self.process_guess)
        self.guess_button.pack(pady=10)

        # Nút chơi lại
        self.replay_button = tk.Button(root, text="Chơi Lại", command=self.reset_game)
        self.replay_button.pack(pady=10)

    # ======================== Tải từ ===========================

    def load_words(self):
        """Tải danh sách từ từ file words.txt"""
        try:
            with open("words.txt", "r", encoding="utf-8") as file:
                words = [line.strip().upper() for line in file if line.strip()]
                if not words:
                    messagebox.showerror("Lỗi", "Không tìm thấy từ nào trong file words.txt")
                    return None
                return words
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file words.txt")
            return None
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc file: {e}")
            return None

    # ======================== Khởi động lại trò chơi ===========================

    def reset_game(self):
        """Khởi động lại trò chơi mới"""
        if not self.words:
            messagebox.showerror("Lỗi", "Không thể bắt đầu trò chơi: Không có từ nào")
            sys.exit(1)

        self.word = random.choice(self.words)  # Chọn từ ngẫu nhiên
        self.guessed_letters = set()           # Các chữ cái đã đoán
        self.errors = 0                        # Số lần đoán sai
        self.game_over = False                 # Cờ kiểm tra game kết thúc chưa

        # Nếu đã từng tạo nhãn từ trước → cập nhật lại giao diện
        if hasattr(self, 'word_label'):
            self.word_label.config(text=self.display_word())
            self.error_label.config(text=f"Số lần đoán sai: {self.errors}/6")
            self.canvas.delete("all")
            self.draw_hangman()
            self.entry.delete(0, tk.END)
            self.entry.config(state="normal")
            self.guess_button.config(state="normal")

    # ======================== Hiển thị từ ===========================

    def display_word(self):
        """Hiển thị từ hiện tại, các chữ chưa đoán được thay bằng dấu gạch dưới"""
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word)

    # ======================== Vẽ hình treo cổ ===========================

    def draw_hangman(self):
        """Vẽ giá treo cổ tùy vào số lỗi"""
        self.canvas.delete("all")

        # Vẽ giá treo
        self.canvas.create_line(20, 180, 180, 180)  # Đế
        self.canvas.create_line(50, 180, 50, 20)    # Cột dọc
        self.canvas.create_line(50, 20, 120, 20)    # Thanh ngang
        self.canvas.create_line(120, 20, 120, 40)   # Dây

        # Vẽ hình người dần dần theo số lỗi
        if self.errors > 0:
            self.canvas.create_oval(110, 40, 130, 60)      # Đầu
        if self.errors > 1:
            self.canvas.create_line(120, 60, 120, 100)     # Thân
        if self.errors > 2:
            self.canvas.create_line(120, 70, 100, 90)      # Tay trái
        if self.errors > 3:
            self.canvas.create_line(120, 70, 140, 90)      # Tay phải
        if self.errors > 4:
            self.canvas.create_line(120, 100, 100, 130)    # Chân trái
        if self.errors > 5:
            self.canvas.create_line(120, 100, 140, 130)    # Chân phải

    # ======================== Xử lý đoán chữ ===========================

    def process_guess(self, event=None):
        """Xử lý khi người chơi nhập chữ"""
        if self.game_over:
            return

        guess = self.entry.get().strip().upper()
        self.entry.delete(0, tk.END)

        # Kiểm tra đầu vào hợp lệ
        if not guess or len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Nhập Sai", "Vui lòng nhập một chữ cái.")
            return

        # Kiểm tra đã đoán rồi chưa
        if guess in self.guessed_letters:
            messagebox.showinfo("Lặp Lại", "Bạn đã đoán chữ cái này rồi!")
            return

        self.guessed_letters.add(guess)

        # Nếu đoán sai → tăng số lỗi
        if guess not in self.word:
            self.errors += 1

        # Cập nhật giao diện
        self.word_label.config(text=self.display_word())
        self.error_label.config(text=f"Số lần đoán sai: {self.errors}/6")
        self.draw_hangman()

        # Kiểm tra thua
        if self.errors >= 6:
            self.game_over = True
            messagebox.showinfo("Kết Thúc", f"Bạn đã thua! Từ là {self.word}")
            self.entry.config(state="disabled")
            self.guess_button.config(state="disabled")

        # Kiểm tra thắng
        elif all(letter in self.guessed_letters for letter in self.word):
            self.game_over = True
            messagebox.showinfo("Thắng", "Bạn đã thắng!")
            self.entry.config(state="disabled")
            self.guess_button.config(state="disabled")

# ======================== Chạy chương trình ===========================

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

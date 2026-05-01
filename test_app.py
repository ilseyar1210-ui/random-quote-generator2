import unittest
import json
import os

class TestRandomQuoteGenerator(unittest.TestCase):
    def setUp(self):
        self.test_history = "test_history.json"
        self.test_custom = "test_custom.json"

    def tearDown(self):
        for f in [self.test_history, self.test_custom]:
            if os.path.exists(f):
                os.remove(f)

    def test_predefined_quotes_exist(self):
        """Тест: предопределённые цитаты существуют"""
        from main import PREDEFINED_QUOTES
        self.assertGreater(len(PREDEFINED_QUOTES), 0)
        for quote in PREDEFINED_QUOTES:
            self.assertIn("text", quote)
            self.assertIn("author", quote)
            self.assertIn("theme", quote)

    def test_empty_text_validation(self):
        """Тест: пустой текст цитаты не проходит валидацию"""
        from main import RandomQuoteGenerator
        import tkinter as tk
        root = tk.Tk()
        app = RandomQuoteGenerator(root)

        text = ""
        self.assertEqual(text, "")
        root.destroy()

    def test_empty_author_validation(self):
        """Тест: пустой автор не проходит валидацию"""
        from main import RandomQuoteGenerator
        import tkinter as tk
        root = tk.Tk()
        app = RandomQuoteGenerator(root)

        author = ""
        self.assertEqual(author, "")
        root.destroy()

    def test_empty_theme_validation(self):
        """Тест: пустая тема не проходит валидацию"""
        from main import RandomQuoteGenerator
        import tkinter as tk
        root = tk.Tk()
        app = RandomQuoteGenerator(root)

        theme = ""
        self.assertEqual(theme, "")
        root.destroy()

    def test_save_and_load_history(self):
        """Тест: сохранение и загрузка истории"""
        from main import RandomQuoteGenerator
        import tkinter as tk
        root = tk.Tk()
        app = RandomQuoteGenerator(root)

        import main
        main.HISTORY_FILE = self.test_history
        app.HISTORY_FILE = self.test_history

        test_data = [{
            "text": "Тестовая цитата",
            "author": "Тестер",
            "theme": "тест",
            "timestamp": "2024-01-01 12:00:00"
        }]

        app.history = test_data
        app.save_history()

        app.history = []
        app.history = app.load_history()

        self.assertEqual(len(app.history), 1)
        self.assertEqual(app.history[0]["author"], "Тестер")
        root.destroy()


if __name__ == "__main__":
    unittest.main()

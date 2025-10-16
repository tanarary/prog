import sys
from lib.e01_text import tokenize, count_freq, top_n, normalize

def main():
    try:
        # Проверяем, есть ли данные в stdin
        if sys.stdin.isatty():
            print("Ожидание ввода данных...")
            print("Введите текст и нажмите Ctrl+D (Mac/Linux) для завершения ввода:")
        
        text = sys.stdin.read()
        
        if not text.strip():
            print("Нет входных данных")
            return
            
        normalized_text = normalize(text)
        tokens = tokenize(normalized_text)

        if not tokens:
            print("В тексте не найдено слов")
            return

        total_words = len(tokens) # общее количество слов
        freq_dict = count_freq(tokens) # словарь частот
        unique_words = len(freq_dict) # количество уникальных слов 
        top_words = top_n(freq_dict, 5) # самые популярные частоты
        
        print(f"Всего слов: {total_words}")
        print(f"Уникальных слов: {unique_words}")
        print("Топ-5:")
        for word, count in top_words:
            print(f"{word}: {count}")

    except EOFError:
        print("\nВвод завершен")
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":  # Исправлено здесь
    main()

## Лабораторная работа 3

### normalize
```python
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold:
        text = text.casefold()
    if yo2e:
        text = text.replace('ё','е')
        text = text.replace('Ё','Е')
    text = text.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
    text = ' '.join(text.split())
    text = text.strip()
    return text

```
![Картинка 1](scr/lab03/img/e01_normalize_img.png)

### tokenize
```python
def tokenize(text: str) -> list[str]:
    return re.findall(r'\w+(?:-\w+)*', text)

```
    
![Картинка 2](scr/lab03/img/e01_tokenize_img.png)


### count_freq + top_n
```python
def count_freq(tokens: list[str]) -> dict[str, int]:
    sl = {}
    for token in tokens:
        if token in sl:
            sl[token] += 1
        else:
            sl[token] = 1 
    return sl 

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    sorted_freq = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return sorted_freq[:n]

```
![Картинка 3](scr/lab03/img/e01_count_freq+top_n_img.png)

### src/text_stats.py 
```python
import sys
from lib.e01_text import tokenize, count_freq, top_n, normalize

def main():
    try:
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

if __name__ == "__main__": 
    main()


```
![Картинка 4](scr/lab03/img/e02_text_stats_img.png)
import os

def save_instagram_post(text, index):
    """حفظ كابشن انستا في ملف"""
    filename = f"instagram_post_{index}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"💾 حُفظ كابشن انستا: {filename}")

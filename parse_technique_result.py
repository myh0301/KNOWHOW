import re, string
from nostril import nonsense

def sanitize_string(s):
    # Translate non-ASCII character codes.
    s = s.strip().encode('ascii', errors='ignore').decode()
    if re.search(r'([0-9\.]*):([0-9]*)->([0-9\.]*):([0-9]*)',s):
        # s = s.replace('/32','')
        split_path = re.split('/|\.|,|:|-|>',s)
        split_path = [item for item in filter(lambda x:x != '',split_path)]
        split_path.pop(4)
        split_path.pop(8)
        return split_path
    # Lower-case the string & strip non-alpha.
    for i in s:
        if i in string.punctuation:
            s = s.replace(i," ")

    split_path = s.lower().split()
    # split_path = [item for item in filter(lambda x:x != '',split_path)]
    newline = []
    for item in split_path:
        if len(item) < 2 or item.isdigit():
            continue
        if len(item) <= 5 and len(item) >= 2:
            newline.append(item)
        else:
            try:
                if not nonsense(item):
                    newline.append(item)
                else:
                    newline.append('hash')
            except Exception as e:
                print(s)
    split_path = [item for item in filter(lambda x:x != '',newline)]
    return split_path

if __name__ == "__main__":
    with open('./technique_result0109.txt', 'r') as f:
        lines =  f.readlines()
        my_texts = []
        current_entry = []

        # 遍历每一行，处理并收集结果
        for i in range(0, len(lines), 3):  # 每次跳过3行
            if i + 2 < len(lines):  # 确保至少有3行
                # 保留第1行和第3行，忽略第2行
                first_line = lines[i]
                third_line = lines[i + 2]

                # 如果您想在最终结果中包含第一行（如技术编号），取消下面注释：
                # current_entry.extend(re.findall(r'\w+', first_line))

                # 分割句子为单词并添加到当前条目
                sentences = third_line.split('. ')
                for sentence in sentences:
                    if sentence:  # 忽略空句子
                        words = sanitize_string(sentence)
                        current_entry.extend(words)

                # 添加当前条目到my_texts，并重置current_entry
                my_texts.append(current_entry)
                current_entry = []
        file = open("./technique_text.txt", "w")
        file.write(str(my_texts))
        file.close()
        print(my_texts)
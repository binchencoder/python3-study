import jionlp as jio

if __name__ == "__main__":
    char_token_list = "胡静静喜欢江西红叶建筑公司"

    char_entity_list = [
        {"text": "胡静静", "offset": [0, 3], "type": "Person"},
        {"text": "江西红叶建筑公司", "offset": [5, 13], "type": "Company"},
    ]
    word_token_list = ["胡静静", "喜欢", "江西", "红叶", "建筑", "公司"]
    print(jio.ner.char2word(char_entity_list, word_token_list))

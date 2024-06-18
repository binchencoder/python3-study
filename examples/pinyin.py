from xpinyin import Pinyin

if __name__ == "__main__":
    # 实例拼音转换对象
    p = Pinyin()
    # 进行拼音转换
    ret = p.get_pinyin("汉语拼音转换", tone_marks="marks")
    ret1 = p.get_pinyin("汉语拼音转换", tone_marks="numbers")
    print(ret + "\n" + ret1)

    print(
        p.get_pinyin(
            "战场环境基础知识@#$%&军事主题知识@#$%&作战目标@#$%&有生力量@#$%&作战兵力@#$%&作战部队-驻扎-PD知识图谱@#$%&固定设施@#$%&机场",
            "",
        )
    )

    labels = [
        "作战兵力",
        "国家（地区）",
        "作战部队",
        "城市",
        "军事基地",
        "战场军事事件",
        "海上平台",
    ]
    pinyin_labels = []
    for l in labels:
        pinyin_l = p.get_pinyin(
            l,
            "",
        )
        pinyin_labels.append(pinyin_l)

    print(pinyin_labels)

import jionlp as jio

if __name__ == "__main__":

    text = "兰利号航空母舰在2022年1月1日如期靠泊了诺福克海军基地。<div><p>美军港口信息中,列克星敦号航空母舰已于2022年1月4日驶离珍珠港希卡姆联合基地。2022年1月1日，约克城号航空母舰如期到达了基察普海军基地并进行了训练。福特号航空母舰（英文USS Gerald R.Ford），国家美国，舷号CVN-78，舰级尼米兹级，母港布雷默顿，动工时间2005年8月11日，下水时间2013年11月9日，服役时间2017年7月22日，舰长332.85米，舰宽40.84米，吃水12.4米，排水量101600吨，舰员编制5260人，航速30节，续航力80万~100万海里。2019年9月2日进行战术演习，演习名称为美国东盟联合海上演习，参加演习的有美国、东盟国家，参演飞机有MH-60直升机、P-8A反潜巡逻机，演习科目包括登临和搜捕。"
    result = jio.clean_text(text, remove_parentheses=False)
    # result = jio.remove_stopwords(result)
    # result = jio.parse_time(result)
    print(result)

    # res2 = jio.pinyin(text, formater="simple")
    # print(res2)

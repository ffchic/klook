import re
import json
import datetime
import requests
import jieba
import logging
import js2py
from snownlp import SnowNLP
from bs4 import BeautifulSoup
from py_sql import Words, Comments, ScenicSpots
"""
1.实时监测 正负评论数，基本能反应客路旅行在一整年的用户评价信息。我们选取了2023年一整年的正负评论数，画出2023年的正负评论数折线图，
2.1 用户评价数据，提取出所有的标题，将它转化为字符串形式，并且去掉所有的空格，导入新的停用词，然后用精确模式对其进行结巴分词，对分词后的文本进行词频统计，输出出现次数top20的词语，词云图
2.2 现频率top20高频词的横向柱状图
4. 游客总体评论数与情感得分关系图
5.满意度与价格评论数、关键词的相关性
"""
jieba.setLogLevel(logging.INFO)
def fenci(text):
    punc = r'[^\w\s]'
    text = re.sub(punc, '', text)
    return [i for i in list(jieba.cut(text)) if len(i) > 1]

class Spider:
    def __init__(self):
        self.url = "https://www.klook.cn/zh-CN/experiences/list/cruises/cate164/?not_cal_destination=1&start={}&is_clear_flag=1&is_manual_flag=1"
        self.url = "https://www.klook.cn/zh-CN/experiences/list/cruises/cate164/?not_cal_destination=1&start={}&is_clear_flag=1&is_manual_flag=1"
        self.comment_limit = 100
        self.comment_url = "https://www.klook.cn/v1/experiencesrv/activity/component_service/activity_reviews_list?activity_id={}&page={}&limit={}&star_num=&lang=&sort_type=0&only_image=false&sub_category_id=413&k_lang=zh_CN&k_currency=CNY&preview=0"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "klk_currency=CNY; kepler_id=910f6955-f6f0-4db0-8ea9-4aa5fe8dd3ed; _gcl_au=1.1.1333879254.1712417845; KOUNT_SESSION_ID=035840EEB1C32DC426CB044A0FDFF654; clientside-cookie=264c5abfa2757642f9c4c4ea233db7aa5b8c5356c3fcc001fb8a72970c03030ac27f04e4db75ddca62970136b6d512a2539bb84994560ec155211565faf7e00a808b0e6c097115d4a0a6d66acfde57327770b47cdb857fdd2d0c311ce148663ba2268f25dd55abd787d43b54c2bff43f9dcd59d1c42994db39bb52a013e0bbe54fbec2c3cd0788291716e40fdd2c49aff12ec571942d3a172f046b; klk_rdc=CN; _gid=GA1.2.1737730366.1712560524; locale=zh-cn; _ga_FW3CMDM313=GS1.1.1712569434.3.1.1712570635.0.0.0; _ga_V8S4KC8ZXR=GS1.1.1712569447.3.1.1712570637.60.0.0; forterToken=8c80616d39494b03b3f0d263c8a56e9f_1712570637732__UDF43-m4_21ck_; datadome=qV_9sG0ygivy3GQ_b4ftN7qUopZfDrgYZoq_73~sQKKP7QzU2pJ9mfqF64X5gEeLN5qMwxwJVnaINoKz5Aw84Lexwv1AJW7PNxwOoyba3TLgYamtcOa52Y5P4E0OCkfi; _ga=GA1.2.252168503.1712417845; tfstk=fYrKYtgcV1fHFT7uAJ_gzoGKzRBgNkeUQWyXqbcHP5FTh-RnPWVuw7FIsk0oAUv8XuZiO95EZgL7t-9nO2G5fAM-62YnZym8yJ2xRW0lL0HSs-WEq72Ie0nUjyxot6o8FSmRisjcmJyE001ciYtulFiSFgc51lLgW0o5i1V3dmSo4Sxp71C-5OHoEbT7N2isfYGsdpM7NfgshxAIV0N7COH-UYTBR2g6CYkoN-f-1pGk2lJSzDfOWho-4lHK5N2I1tqLXv3KGJZpvHQtp2hbdf5c3bnt58u84L--yJa4axNBO_hzXRZQlS1M-Xaxe-48MitrQyNLf4EGUi2IvXn_ArpWVRnKO4qK8BCtGky_0cgGcte_bW2UX8v5VAVm1JrI2i6qvDGIXArl_HG85zZn80RCwbrTCkaR4fr0D9rpijHkROB9zUuIIndgka2AGV2jBjXd2U8r7OktiOB9zUuIQAhcp6LyzVWN.; klk_i_sn=8507426072..1712576175857; ssxmod_itna=YqAx2iDtG=i=0Qwx0LunDU2Q87DQdNNKDgizr/Cx0vrueGzDAxn40iDt=rLB==Bhwve7Fc0wfbDk=nTdbdoa8pTsKIDB3DEx06YaIDYYCDt4DTD34DYDixibCxi5GRD0KDFWqvz19Dm4GWWqDmDGYcYqDgDYQDGTK6D7QDIT6KtRw9lDDll0TNQ7hiPji6bCUYwMh4=0DcD0UoxBLKm=uKv6FNRL0akP0aYqGyeKGufktZB3bDCE6Zjq0sY7p4I0vxb7+K8OmeYhDmFGDWK0G54SCRNDw5m3mKtgfmUKDAQDnsUiD===; ssxmod_itna2=YqAx2iDtG=i=0Qwx0LunDU2Q87DQdNNKDgizr/DnIS90qDseq7DLWB=WTliIxVAF0sSKUiF6ec/OBF6wmW4AP44knBDiNmfoci4kmYDLrTfq5XGLnP3=nGj=9SQCjCHYdoodYaUXx8hUBOoQDfN487EwzO0f7f3VFeAUeEi7lAdtInd=Vdx7m8fxCMYXRW3oBQbqKRiWslYWVMcUAPuU9BbWc6tCZSFPT6o5G2DWsB2x4Pq8R6Kj8GeQWwjp4RiaHAEOGrEeXOjGC/vQ5iiscrcxl0Bp88qCrX95LptqMnAiLb2X7/otEmgPfxl5HPfbWqkDYGpmdp3kBKlcAbriP6iipfGGtTpxD/qXYAShirKih0E/1o1nEwPwwcpP4vSmdBOY1ofoov7hmWEb=guQgLtpoQQKEYjIj5XQpq9iEQeptuvUeBBPh6uERR8pEPjcd6Dr/GQ==O6eZec8eWqG0nba49Fi8wG+NUeWT=p8/dBx3m=ozgyv=GwO6zRxZ/t7jRm/Lq8KB=I/+GqMNXjRuZvKmG7CfrcQAZFE0pof7iCw409EI2/nXf3YE7w4Kf/emeA4DQ9aYDYbDAeM=9FhFGtRZUM1TtH=Ptn0DDFqD+gxxD==",
            "Host": "www.klook.cn",
            "If-None-Match": 'W/"21a1f-3132Ttcj0/q+TqyzXZFh/IMwPMc"',
            # "Referer": "https://www.klook.cn/zh-CN/experiences/list/cruises/cate164/?not_cal_destination=1&start=1&is_clear_flag=1&is_manual_flag=1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "sec-ch-device-memory": "8",
            "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-arch": "x86",
            "sec-ch-ua-full-version-list": '"Google Chrome";v="123.0.6312.106", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.106"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "",
            "sec-ch-ua-platform": "Windows",

        }
        self.activity_ids = set()
        self.activity_ids = set([int(line.strip()) for line in open("activity_id.txt", 'r').readlines() if line.strip()])
        self.activity_page = {}
        activity_page = set([line.strip() for line in open("activity_page.txt", 'r').readlines()])
        for i in activity_page:
            if not i:
                continue
            k, v = i.split("-")
            k,v = int(k),int(v)
            if int(v) > self.activity_page.get(k, 0):
                self.activity_page[int(k)] = int(v)

    def get_comment(self, activity_id):
        # 获取评论数据
        res = requests.get(url=self.comment_url.format(activity_id, 1, self.comment_limit), headers=self.headers)
        data = res.json()
        if not data.get("result",{}):
            print("        worring | (1)Comment data is invalid...{}".format(activity_id))
            return
        total = data.get("result",{}).get("total")
        if not total:
            print("        worring | (1)Comment data is invalid...{}".format(activity_id))
            return
        limit = data["result"]["limit"]
        total_page = (total//limit) + 1
        for page in range(1, total_page+1):
            if page < self.activity_page.get(activity_id,0):
                continue
            res = requests.get(url=self.comment_url.format(activity_id, page, self.comment_limit), headers=self.headers)
            print("        [{}/{} | COMMENT DATA STATUS CODE:[{}]]start crawl {}".format(page, total_page, res.status_code, activity_id))
            if res.status_code != 200:
                print("        [ERROR] COMMENT DATA  Status Code ERROR, start chrome for cookies ...{}".format(activity_id))
            else:
                data = res.json()
                items = []
                if not data:
                    print("        worring | (2)Comment data is invalid...{}".format(activity_id))
                    continue
                if not data.get("result",{}) or not data.get("result",{}).get("item"):
                    print("        worring | (2)Comment data is invalid...{}".format(activity_id))
                    continue
                insert_data = []
                a = 0
                for i in data["result"]["item"]:
                    translate_content = i["translate_content"]
                    date = i["date"]
                    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                    last_year = datetime.datetime.strptime("2022-12-31", "%Y-%m-%d")
                    if date < last_year:
                        # print("    worring | (3)Comment data is invalid...{}".format(activity_id))
                        continue
                    date_str = date.strftime('%Y-%m')
                    items.append(translate_content)
                    fenci_items = fenci(translate_content)
                    # 进行分词和情感分析
                    self.fenci_sql(fenci_items)
                    print("\r        分词进度:{}/{}".format(a, len(data["result"]["item"])), end="")
                    a +=1
                    score = SnowNLP(translate_content)
                    insert_data.append([activity_id, translate_content, date_str, score.sentiments])
                # 入库
                Comments().insert(tuple(insert_data))
                with open("activity_page.txt", "a+") as f:
                    f.write(str(activity_id) + "-" + str(page) + "\n")

    def fenci_sql(self, fenci_items):
        fenci_dict = {}
        for i in fenci_items:
            if i in fenci_dict.keys():
                fenci_dict[i] += 1
            else:
                fenci_dict[i] = 1

        w = Words()
        r = w.select()
        sql_data = {}
        for sql_word,sql_num in r:
            sql_data[sql_word] = sql_num
        for word,num in fenci_dict.items():

            if word in sql_data.keys():
                w.update(word, num + sql_data[word])
            else:
                w.insert(word, num)

    def Obtain(self):
        # 请求页面
        for page in range(1,418):
            res = requests.get(url=self.url.format(page), headers=self.headers )
            print("[{}/418 | PAGE DATA STATUS CODE:[{}]]start crawl attractions ".format(page, res.status_code))
            if res.status_code != 200:
                print("[ERROR] PAGE DATA  Status Code ERROR, start chrome for cookies ...")
            else:
                # 使用BeautifulSoup获取script标签内的js代码
                soup = BeautifulSoup(res.text, 'html.parser')
                search_script = soup.find_all('script', attrs={'crossorigin': True})
                # 使用js2py将获取到的js代码转化为python数据格式
                context = js2py.EvalJs()
                context.execute(search_script[3].text)
                datas = context.window.__KLOOK__.to_dict()["state"]["experience"]["searchResultActivities"]
                # 提取数据（数据清洗）
                for n,data in enumerate(datas):
                    activity_id = data["activity_id"]
                    if activity_id in self.activity_ids:
                        continue
                    print("    [{}/{} | INFO DATA STATUS CODE:[{}]]start crawl attractions ".format(n,len(datas), res.status_code))
                    if res.status_code != 200:
                        print("    [ERROR] INFO DATA  Status Code ERROR, start chrome for cookies ...")
                    title = data["title"]
                    price = data["price"]["sale_price"].replace(" ","").replace("¥","").replace(",","")
                    if not price:
                        price = data["price"]["from_price"].replace(" ", "").replace("¥", "").replace(",", "")
                    if not price:
                        price = data["price"]["underline_price"].replace(" ", "").replace("¥", "").replace(",", "")
                    try:
                        price = float(price)
                    except Exception as e:
                        price = 0
                    product_tags = []
                    for i in data["product_tags"]["attribute_tags"]:
                        text = i["text"]
                        if text:
                            product_tags.append(text)
                    score = data["review"]["score"]
                    score_number = data["review"]["number"].replace(",","")  # 参与评分人数
                    if not score:
                        score = 0
                    if not score_number:
                        score_number = 0
                    score = float(score)
                    if "K" in score_number:
                        score_number = score_number.replace("K", "")
                        score_number = score_number.replace("+", "")
                        score_number = float(score_number) * 1000
                    score_number = float(score_number)
                    booked = data["review"]["booked"].replace(" ","").replace("人参加过","").replace("+", "")  # 热度
                    if "K" in booked:
                        booked = booked.replace("K", "")
                        booked = int(booked) * 1000
                    if not booked:
                        booked = 0
                    product_tags = ",".join(product_tags)
                    self.get_comment(activity_id)
                    ScenicSpots().insert(activity_id, title, price, product_tags, score, score_number, booked)
                    with open("activity_id.txt", "a+") as f:
                        f.write(str(activity_id) + "\n")


s = Spider()
s.Obtain()
import requests
import js2py
from bs4 import BeautifulSoup

class Spider:
    def __init__(self):
        self.url = "https://www.klook.cn/zh-CN/experiences/list/day-trips/cate10/?spm=TNA_Vertical.CategorySeeAll&clickId=0095a0d6bd"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "acw_tc=2f6a1fa617124178421584507e1da37e6343e5f7ea783e1a96e86630ed1019; klk_currency=CNY; kepler_id=910f6955-f6f0-4db0-8ea9-4aa5fe8dd3ed; klk_rdc=CN; acw_sc__v2=66116c340cb291df747ed8e3a0411305dc6f0e6d; _gcl_au=1.1.1333879254.1712417845; _gid=GA1.2.1263568831.1712417846; JSESSIONID=035840EEB1C32DC426CB044A0FDFF654; KOUNT_SESSION_ID=035840EEB1C32DC426CB044A0FDFF654; clientside-cookie=264c5abfa2757642f9c4c4ea233db7aa5b8c5356c3fcc001fb8a72970c03030ac27f04e4db75ddca62970136b6d512a2539bb84994560ec155211565faf7e00a808b0e6c097115d4a0a6d66acfde57327770b47cdb857fdd2d0c311ce148663ba2268f25dd55abd787d43b54c2bff43f9dcd59d1c42994db39bb52a013e0bbe54fbec2c3cd0788291716e40fdd2c49aff12ec571942d3a172f046b; KSID=MQ.1d15028c20ec4d377654af560d1dd727; _ga=GA1.1.252168503.1712417845; _ga_V8S4KC8ZXR=GS1.1.1712417845.1.1.1712417884.21.0.0; forterToken=8c80616d39494b03b3f0d263c8a56e9f_1712417886271__UDF43-m4_21ck_; datadome=nHG3QSAeeS0cBvb85iMSwAlsOfLMemfBBnbUjHyK0NnrCwRQ5GiQO9kEsOX_7_YvPYOwzSt0dG5IpMLlAwaFBLYK~6nS7AEUu7ohmI4fnfXIvLLhIr5rq625e5prNRoT; klk_ga_sn=2931335226..1712417906621; _ga_FW3CMDM313=GS1.1.1712417844.1.1.1712417907.0.0.0; klk_i_sn=2514141974..1712417917490; tfstk=fRfIY2Y42DmCfe76qpUNlnInj3A7NMNq24TRoahEyBdK20QvbBRyTBr5CgIwv45PJhXMXiiy4yvzNbs1q9le9gPW2ZxGTU8FL3h5yhfU-3zH6ALDjg9u-3-JVg7RLPP4gwbHZQC70SP4b5CzEMGpvQUJWU8-QPGtJwbHZVcsqnoA-Y9PXJ5Jegd9BUYXweLJwfU6zUDpwHp-XALvX3dJwgd96U8q93h-9CKtNguXPJthRubA-BJIAubefbhjoe9K0wDrGj1XRp1RWh9yU1TBdnJwWled9G7RT6vgBAOl7ts5eiEZLHBXlG9VdoGCcMYRXFIUzYY1FaCDtp3jGN9WAOCpC4hRWCxpUTsQAvxdLG9DWd37iFS2XwfdCzmOJi-B9FpaMr_9eO5Hn6rtOIBc8BWRDlkevtTR43c2cmNoFV9mNFt45PMoU03mh09G6DZ9pFYBQPasvTvpSFtb5PMoHpLMRhU_5DB1.; ssxmod_itna=eqjxuDy7D=DtqAKGHLhCGKDOfAFu7DDKrfjdD/+mDnqD=GFDK40oo7vb=r=Y2KeAlOB4GC9ESvYa5HFCirWKmzr4GLDmKDyQAh+eDxrq0rD74irDDxD3DbbdDSDWKD9D0bSyuEXKGWDbo=Di4D+bkQDmqG0DDtH04G2D7UnG05r7TeD0web3AGDoedepqbBQG0xKY=DjTbD/4+H2mr7paelYeaaVqp2DB6sxBQSmdN6GeDH7TXS/T4tihqonExoGipi8AAPe2D4F0Y=K0DzYNltQBEqGAYfLR4rDDfrj7mdeD===; ssxmod_itna2=eqjxuDy7D=DtqAKGHLhCGKDOfAFu7DDKrfQG9tcDRhGDGXP4rGaQGFEcY3Gzx8rqe8qKiexiQnR=7abI8tInYx+=D+0InsqHj1AxLDZKPq00pXKmABshLO/HaBfux5oH8n5LX1BcqAFWMhiH=rnt0WK+YZKr0QmkbcD=bKBdrZwrPlbrWRa=iGexzPWt870doWOxe=ivrWgfdm8GgBF7KBe4pSaP0FfbtA8aVmpKHamjeguhb+3jaFKQ3qB41FwIegnYjU1vpKpK+e=CWva=8ArvAdIKKp/SqBBp9oaF8uOmKomfZxZGYRcAnzjyp8vTA5g/qVzaIAevn9NlbC3a7UnePpjFiA0xQCTIW9cBb28cDKOGfmHlhI/WF7EbIAtbbmRbfnW2jOb0HF/BoLWaFvI+WaWqe4Fa+7yRu=VWW8SRefSfWF84sn9YqI=Ufr7g/IEQpn5VfiOY=0wFOEFP3ONu4UcKf340q/A4i3IBUMVBSOcL9/AOXODuSVUolAxQMqzQ+9eShrEy/7YEh8tQdqQiIQetxDKd4aG8ciKN6ksIT+mDmKt+Ba1kn9An3AcKgch7cRdWy0K+Afhiz1ayKGyWtOcDxMD9a2DeixrMB3ym+B34yKWX4ciHLBahAS+Ukl4DLxD2ehDD",
            "Host": "www.klook.cn",
            "If-None-Match": 'W/"2807b-oKsWGRCQXYKfhhgrMPGiD5Drmew"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "sec-ch-device-memory": "8",
            "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-full-version-list": '"Google Chrome";v="123.0.6312.86", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.86"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "",
            "sec-ch-ua-platform": "Windows"
        }

    def Obtain(self):
        res = requests.get(url=self.url, headers=self.headers )
        soup = BeautifulSoup(res.text, 'html.parser')
        search_script = soup.find_all('script', attrs={'crossorigin': True})
        print(search_script[3])
        print(search_script[3].text)

        context = js2py.EvalJs()
        context.execute(search_script[3].text)

        # state  experience  searchResultActivities
        print(context.window.__KLOOK__)
        print(context.window.__KLOOK__.to_dict()["state"]["experience"]["searchResultActivities"])
        print(type(context.window.__KLOOK__.to_dict()))


s = Spider()
s.Obtain()
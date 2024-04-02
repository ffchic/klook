import requests
import js2py
from bs4 import BeautifulSoup

url = "https://www.klook.cn/zh-CN/experiences/list/day-trips/cate10/?spm=TNA_Vertical.CategorySeeAll&clickId=0095a0d6bd"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "kepler_id=2ee72aa0-c123-4d21-9690-93980abf9bf0; klk_currency=CNY; klk_rdc=CN; referring_domain_channel=seo; _gcl_au=1.1.710510048.1711958811; _gid=GA1.2.184826712.1711958811; KOUNT_SESSION_ID=624B2E1C7C8F5DD22F06DAE0D927AA45; clientside-cookie=bd8b03b3568280c4cc86cbfc41a10f7c94d8a9c87377a8fae63109da76f333e55c6b31159e8ddfdb95e4fbca3886a4e218793c19d211dd8f02d4422b18499567a227d9a6e547e99a9e9cdcdee0602a98b7c4e6c1d4e4b4097369c22dd5d9b087fa7eefe92769083543b22d3e8e35c3d089a545ae6be0dc10afdb90abaca733b6bc19b49936725fdd7788045953979677b5bd1e679796b5714d785e; retina_support=1; CSRF-Token=MTcxMTk1ODgzOHxndVZiWkZsZUJOOGZtWDN0Z2xJcHZ5NDY5YjZZX0dKZnw4f4mDIo_hYFymmzB0GfvD4uBtJ5IKqFFS6P07oTUbjA==; CSRF-Token-Valid=valid; device_id_new=DpqwU4zEdN00500000000000005B8Gc9qXKS00891467765WpYWiKzBGXnBSJqzXqXBix7RX3az8002q7zBvelero00000qZkTE0000024jgxgozwGEC4FlSABmQ:40::2ad4c614aba94d62; tag_fok=1711958838000; persisted_source=www.google.com; k_tff_ch=google_seo; tr_update_tt=1712037877633; campaign_tag=klc_l1%3DSEO; traffic_retain=true; _ga_V8S4KC8ZXR=GS1.1.1712037878.4.1.1712038295.35.0.0; forterToken=16a21255148344dfb519026c7535e27f_1712038295291__UDF43-m4_21ck_; datadome=w31FW6fSnBPAShKTBctRpQr0twPdFLEMr0ploJl_zdzj2g45ymjpc1ff_wQKNxdhYqt25H1gqmiEH_49iLchMBC79W6WZCSmYSJrEcNqxnmpQpyR1w2pfSZSbw6Wh5ph; _ga_FW3CMDM313=GS1.1.1712041069.6.0.1712041069.0.0.0; _ga=GA1.2.1562821377.1711958811; ssxmod_itna=iqmxcDB70QDQ=4BcDeTm4Uhb8dexYvPqIY44fpdD/AQ+DnqD=GFDK40EYSxmKuK5GGOphtIQD0IK6KQGoxetHop03IV0ex0aDbqGkdYer4GG0xBYDQxAYDGDDPCDj4ibDYfzODjBItzZCq=D3qDwDB=DmqG2KWiDA4DjCw+KFR6miqDh+LxD0Mh5A0ItDYPyULLe5CrDAkhMAG4yD0tDIqGXQDyKCqDBR1yKSMt7p6naiM0qxBQD7u2S/8rDCoUVRLjb=OGaY7GY/ofYQApPADxiz8hmDyvxl7x2jA4QFDe3b8eiUY42SXxDDf3OxOO4xD==; ssxmod_itna2=iqmxcDB70QDQ=4BcDeTm4Uhb8dexYvPqIY44fPG9WxjExGN30hKGaioF02nQ8DxwG=D6Q09D7yYUdPj1K6rrF21YzFlBaqPkOdYH+7jODK++vXUEB832ACmYCk6mx1=KOqpT2F/gR=m8Mrrsf6eYnoTsep7iLrnOV6vw07WY/r5=zAm=yQPTb=9YFUFxB7EGbPqrq=FO6byHEbKbnfc69CajBRL+23Y6Fa3tSbMicovWKLC0s8l=YyEuPsc=MemRMmCsUbl0HuCsGku919WQNHHn/cOsg2tPLHllmNChoR5t=0iOzo5H94kbWzUurCqany4SmCUr97W8APrl4j+u7RFCBb99utRTW+4j9T0WFW9P5O9ouD2DIpGRrGPWSAp4uxoGpRvkmR=Ou=UbCtTdYD4BHSlmtkWgBR4Dcbpbh3HE0DHlbdbx4mHvUKQ/HK8H7bxWwqP4YQeLQwqxP4N=9ztq4yuLbYaadrYdwK9zYMbtb1GR7U4W+BH1YQ4T+QG3D0760qdlEWBq8mdqBrrdPo8DqBQqAPNfkHKo89NXEvq7Qe0ns4x7GTN6PY75eAP80EGBinrABAfHkEd4yvr9gnDVo80/+iGQcAxYlE41D2tAwrzGAQgle=0dvDelzxt73=vqONey0DWDDLxD2bvl7GIkhDD=; klk_i_sn=9728672253..1712042398211; tfstk=fxUrDG0_-aQy9YEn3xgEbiuSxm38FVB1qyMItWVnNYDkPU93082mFYw7tvrEn7wIqTVL3eP8tuGQV_EELRNKE2ZSFX24BJRSqviC8WVnHz1-d_30ix0ovuMIFvuU9R5fCN__w73KrO615Fluvd3otX0nt6DmOfywqUm_w73pM4ilmnPJY4fFbym3Kqmm9X3nZb0noslstv0nEDvDmfDmK203Kxxm1XdkreYkoqD1iJ2JuxolFdzBO6bXipHaZx8aMrclXf7tFeY3ubP4_7x2-e4qa0UQOPtWD0Z36cU7Ow8xP5rmofNRzEugZfyShRbMuqVbiJiTD9LsP-zEbzmJtFg7wXoi-mRH-SuuVc4-SNvqMoV7xzeyTec8PPiEBm5HJDg05cqgUBCTi4c3pcUCBUHut5UTfV7XqVV4xRrF4DvKiVmbJuJHY0cxgA1Vi3HJtQclrwpHvHnVDjk161Kpv0cxgA1VgHKK0PhqC1CO.",
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
    # "Host":"www.klook.cn",
    # "Cookie": "kepler_id=2ee72aa0-c123-4d21-9690-93980abf9bf0; klk_currency=CNY; klk_rdc=CN; referring_domain_channel=seo; _gcl_au=1.1.710510048.1711958811; _gid=GA1.2.184826712.1711958811; KOUNT_SESSION_ID=624B2E1C7C8F5DD22F06DAE0D927AA45; clientside-cookie=bd8b03b3568280c4cc86cbfc41a10f7c94d8a9c87377a8fae63109da76f333e55c6b31159e8ddfdb95e4fbca3886a4e218793c19d211dd8f02d4422b18499567a227d9a6e547e99a9e9cdcdee0602a98b7c4e6c1d4e4b4097369c22dd5d9b087fa7eefe92769083543b22d3e8e35c3d089a545ae6be0dc10afdb90abaca733b6bc19b49936725fdd7788045953979677b5bd1e679796b5714d785e; retina_support=1; CSRF-Token=MTcxMTk1ODgzOHxndVZiWkZsZUJOOGZtWDN0Z2xJcHZ5NDY5YjZZX0dKZnw4f4mDIo_hYFymmzB0GfvD4uBtJ5IKqFFS6P07oTUbjA==; CSRF-Token-Valid=valid; device_id_new=DpqwU4zEdN00500000000000005B8Gc9qXKS00891467765WpYWiKzBGXnBSJqzXqXBix7RX3az8002q7zBvelero00000qZkTE0000024jgxgozwGEC4FlSABmQ:40::2ad4c614aba94d62; tag_fok=1711958838000; acw_tc=2f6a1fa017120378886314637e3ef25aa21f94c506fcc1639380ddb9986797; persisted_source=www.google.com; k_tff_ch=google_seo; acw_sc__v2=660ba0027596808a058323525918492a11d54c7a; tr_update_tt=1712037877633; campaign_tag=klc_l1%3DSEO; KSID=MQ.1090cdd0502f4e9742c7ee3b642c3981; traffic_retain=true; _dc_gtm_UA-86696233-1=1; klk_ga_sn=7433769431..1712038283428; datadome=~LkiiJsU2qKKBg1QEAkPC9HSm4VKWKKPIAwp01Kn9pLNN6jfFA36hOhbeXNH_ygweYkSOJ4T_uYBvxHI3OSh4YnuQFEeLP7wlWSV~C9m8671Hqfjnl6XTRuFDcdjJx1l; _ga_FW3CMDM313=GS1.1.1712037878.5.1.1712038283.0.0.0; _ga=GA1.1.1562821377.1711958811; _ga_V8S4KC8ZXR=GS1.1.1712037878.4.1.1712038284.46.0.0; klk_i_sn=9728672253..1712038286669; forterToken=16a21255148344dfb519026c7535e27f_1712038284627__UDF43-m4_21ck_; ssxmod_itna=eq0xgDyD9GDQFqWq0dD=wgD=DRnDui0rlZO0p=Ix0yDPGzDAxn40iDt==HrnQg2obq4YFoluXY38nfbPIwCU+iPtL7ST2eDHxY=DUZxPhoD4SKGwD0eG+DD4DWUx03DoxGASpx0+kSBcu=nDAQDQ4GyDitDKkixxG3D0R6x87oyWD=De3UKDDXK46hxfxeDb26MS32xHeDS/BUxK0=DjqGgDBLYR6xyDDt1g6h/Ud9O=1PntliDtqD9CjUXFeDH+MXl3unsf7Ptf74sWo+F/ADqzSqP4Xv34Eet0B4eQODP/Y4qRiC/kDDAfeKi2DeD=; ssxmod_itna2=eq0xgDyD9GDQFqWq0dD=wgD=DRnDui0rlZO0p=4nISR5DsdeDLWahQNCaZ4nRiUOrl2OFwOKlxeY4+xgnlv2O0m4nwREljIL2GHDoC7I4ie+=Lyv8GdfIldtU2EY/lCsgDjv4f2wmIxuCK5Zcq=vZ2rVDWbpeYksWr8qe9dyiotvPhkqD7briTNzYndppgGXe2mVAEf1+qA1tgi7/Tsv1xpLpM+atTTs7BD5gB05av0Ehq2XlxGVCeNbIK+tkALNXCf3yq1tXFNsz18DKQnDIB+TF55jFnOzIFr=oBAYZ+ADpQpCNPhVqQTr5XBY5xGbrt4lYqAt/4tDgYUkhWEx4QhCYtudaPxOtkwgfsofsxwm8W32kw=o+BkNMLGTO+Nj4q2Gano5o31QaXgYqE5Tf7/YAlei46vpbCTooD13rhAvgzzWflC=5Qd5ppVCvr1v=ev0hfrppw=GbOfjC+v=jCPIHaj7=jm=U1ZsfDDwrDP7GB2iqlxIcGKDXZKXplyDN7RlxDjKDeLx4D==; tfstk=fYFEIRcbZ6CeyDeobcGr3OlQYllKFjIbx7iSrz4oRDmHOBtuQkqiADZQr0yrjyZSKM48bQzLrJg7dwer4oa-xuzRJ4muquo7dO1bJyh-ZiZPGsaL3r0S-ukHKcxgW4uHt_bbE4c-Zis6CQDdgbEjTNoVYAbZP4iorumnS1mtz2AuqDDMjquxZ0qoZNkir20HE4D3SF0-wdquvCoZKMt4NBKDhjMEmPWvZQukGvmmmcAlmSuFDm4nbQASv4US5PzCYIUs9SZqlk1MTozY6lugm_SZwleuq4rGM3GLhkFxQk6DsPcEXxV_A_sQ77oEnWDwzaaZO4qoURI2G2lQQxPUpaKg-oiUnXUWuMaZ3RkxSAYyKXwbl7H0t6-xfx3zAcZciCliEgoH2VcmC7eeqLknWVof7NvKvUYn-6fJqLp-QO3ZcZQveLHnWVof7NJJeAPx7m_Ak",
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

res = requests.get(url=url, headers=headers )
print(res)
soup = BeautifulSoup(res.text, 'html.parser')
search_script = soup.find_all('script', attrs={'crossorigin': True})


context = js2py.EvalJs()
context.execute(search_script[3].text)

# state  experience  searchResultActivities
print(context.window.__KLOOK__.to_dict()["state"]["experience"]["searchResultActivities"])
print(type(context.window.__KLOOK__.to_dict()))



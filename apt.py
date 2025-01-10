import openpyxl
import time
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import Entry, Button, Frame, DISABLED, NORMAL, IntVar, Checkbutton, LabelFrame
from tkinter import ttk
import requests
import math
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

tableview = None

class NaverRealEstateScraper:
    def __init__(self):
        self.options = Options()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        self.options.add_argument(f"user-agent={user_agent}")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)

        self.wait = WebDriverWait(self.driver, 30)
        self.last_data = {}

    def run_tkinter_program(self):
        global tableview
        root = tk.Tk()
        root.title("Naver Real Estate Scraper")

        search_frame = Frame(root)
        search_frame.pack(side="top", fill="x", pady=10)
        # search_frame.pack(expand=True, pady=10,fill="both")

        sg_condition_frame = Frame(root)
        sg_condition_frame.pack(side="top", pady=20, fill="both")

        # 검색 입력 창
        entry = Entry(search_frame)
        entry.pack(side="left", fill="both", expand=True)
        entry.insert(0, "지역명 검색")
        # entry.configure(state='disabled')

        x_focus_in = entry.bind('<Button-1>', lambda x: focus_in(entry))
        x_focus_out = entry.bind('<FocusOut>', lambda x: focus_out(entry, '지역명 검색'))
        # 검색버튼
        btn_search = Button(search_frame, text="검색", padx=5, pady=5,
                            command=lambda: start_crawling(entry, sg_chk1.get(), sg_chk2.get(), sg_chk3.get(),
                                                           sg_chk4.get(), sg_chk5.get(), sg_chk6.get(),
                                                           sg_chk7.get(), sg_chk8.get(), sg_chk9.get(),
                                                           sg_chk10.get(), sg_chk11.get(), sg_chk12.get(),
                                                           tr_type1.get(), tr_type2.get(), tr_type3.get()))
        btn_search.pack(side="left", padx=5, fill="both")

        # btn_start = Button(search_frame, text="시작", padx=5, pady=5, command=on_start_button_click)
        # btn_start.pack(side="left", padx=5, fill="both")

        # copy_button = Button(search_frame, text="복사", padx=5, pady=5, command=copy_row)
        # copy_button.pack(side="left", padx=5, fill="both")

        # 엑셀 저장 버튼
        # btn_exportexcel = Button(search_frame, text="엑셀 저장", padx=5, pady=5, state=NORMAL, command=btnexportexcel)
        # btn_exportexcel.pack(side="left", padx=5, fill="both")

        # 프로그램 종료 버튼
        btn_exit = Button(search_frame, text="프로그램 종료", padx=5, pady=5, command=root.quit)
        btn_exit.pack(side="left", padx=5, fill="both")

        # 검색 조건 프레임
        sg_condition_frame = Frame(root)
        sg_condition_frame.pack(side="top", pady=20, fill="both")

        # 상가 구분 프레임
        frame_middle_left = LabelFrame(sg_condition_frame, text="상가 구분")
        frame_middle_left.pack(side="left", fill="both", expand=True)

        sg_chk1 = IntVar()
        sg_chk1_box = Checkbutton(frame_middle_left, text="아파트", variable=sg_chk1)
        sg_chk1_box.pack(side="left")
        sg_chk1_box.select()

        sg_chk2 = IntVar()
        sg_chk2_box = Checkbutton(frame_middle_left, text="오피스텔", variable=sg_chk2)
        sg_chk2_box.pack(side="left")

        sg_chk3 = IntVar()
        sg_chk3_box = Checkbutton(frame_middle_left, text="아파트분양권", variable=sg_chk3)
        sg_chk3_box.pack(side="left")
        sg_chk3_box.select()

        sg_chk4 = IntVar()
        sg_chk4_box = Checkbutton(frame_middle_left, text="오피스텔분양권", variable=sg_chk4)
        sg_chk4_box.pack(side="left")

        sg_chk5 = IntVar()
        sg_chk5_box = Checkbutton(frame_middle_left, text="빌라", variable=sg_chk5)
        sg_chk5_box.pack(side="left")

        sg_chk6 = IntVar()
        sg_chk6_box = Checkbutton(frame_middle_left, text="전원주택", variable=sg_chk6)
        sg_chk6_box.pack(side="left")

        sg_chk7 = IntVar()
        sg_chk7_box = Checkbutton(frame_middle_left, text="상가주택", variable=sg_chk7)
        sg_chk7_box.pack(side="left")

        sg_chk8 = IntVar()
        sg_chk8_box = Checkbutton(frame_middle_left, text="상가", variable=sg_chk8)
        sg_chk8_box.pack(side="left")

        sg_chk9 = IntVar()
        sg_chk9_box = Checkbutton(frame_middle_left, text="사무실", variable=sg_chk9)
        sg_chk9_box.pack(side="left")

        sg_chk10 = IntVar()
        sg_chk10_box = Checkbutton(frame_middle_left, text="공장/창고", variable=sg_chk10)
        sg_chk10_box.pack(side="left")

        sg_chk11 = IntVar()
        sg_chk11_box = Checkbutton(frame_middle_left, text="건물", variable=sg_chk11)
        sg_chk11_box.pack(side="left")

        sg_chk12 = IntVar()
        sg_chk12_box = Checkbutton(frame_middle_left, text="토지", variable=sg_chk12)
        sg_chk12_box.pack(side="left")

        # 거래 유형 프레임
        frame_middle_right = LabelFrame(sg_condition_frame, text="거래유형")
        frame_middle_right.pack(side="right", fill="both", expand=True)

        tr_type1 = IntVar()
        tr_type1_box = Checkbutton(frame_middle_right, text="매매", variable=tr_type1)
        tr_type1_box.pack(side="left")
        tr_type1_box.select()

        tr_type2 = IntVar()
        tr_type2_box = Checkbutton(frame_middle_right, text="전세", variable=tr_type2)
        tr_type2_box.pack(side="left")
        tr_type2_box.select()

        tr_type3 = IntVar()
        tr_type3_box = Checkbutton(frame_middle_right, text="월세", variable=tr_type3)
        tr_type3_box.pack(side="left")
        tr_type3_box.select()

        result_print_frame = LabelFrame(root, text="검색 결과")
        result_print_frame.pack(side="top", fill="both", expand=True)

        list_frame = Frame(result_print_frame)
        list_frame.pack(side="top", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        tableview = ttk.Treeview(list_frame,
                                 columns=["atclCfmYmd", "rletTpNm", "tradTpNm", "prc", "spc1", "spc2", "hanPrc",
                                          "rentPrc",
                                          "atclFetrDesc", "tagList", "detaild_information"], \
                                 displaycolumns=["atclCfmYmd", "rletTpNm", "tradTpNm", "prc", "spc1", "spc2", "hanPrc",
                                                 "rentPrc", "atclFetrDesc", "tagList", "detaild_information"], \
                                 height=20, yscrollcommand=scrollbar.set)

        tableview.pack(fill="both", expand=True)

        tableview.column("#0", width=0, stretch=tk.NO)

        tableview.column("atclCfmYmd", width=80, anchor="center")
        tableview.heading("atclCfmYmd", text="등록 일자", anchor="center")

        tableview.column("rletTpNm", width=80, anchor="center")
        tableview.heading("rletTpNm", text="상가 구분", anchor="center")

        tableview.column("tradTpNm", width=80, anchor="center")
        tableview.heading("tradTpNm", text="거래 유형", anchor="center")

        tableview.column("prc", width=80, anchor="center")
        tableview.heading("prc", text="가격", anchor="center")

        tableview.column("spc1", width=80, anchor="center")
        tableview.heading("spc1", text="계약면적(m2)", anchor="center")

        tableview.column("spc2", width=80, anchor="center")
        tableview.heading("spc2", text="전용면적(m2)", anchor="center")

        tableview.column("hanPrc", width=80, anchor="center")
        tableview.heading("hanPrc", text="보증금", anchor="center")

        tableview.column("rentPrc", width=80, anchor="center")
        tableview.heading("rentPrc", text="월세", anchor="center")

        tableview.column("atclFetrDesc", width=80, anchor="center")
        tableview.heading("atclFetrDesc", text="요약정보", anchor="center")

        tableview.column("tagList", width=80, anchor="center")
        tableview.heading("tagList", text="기타정보", anchor="center")

        tableview.column("detaild_information", width=80, anchor="center")
        tableview.heading("detaild_information", text="상세링크", anchor="center")

        scrollbar.config(command=tableview.yview)

        root.mainloop()


    def scrape_naver_real_estate(self, keyword, sg_chk1, sg_chk2, sg_chk3, sg_chk4, sg_chk5, sg_chk6, sg_chk7, sg_chk8, sg_chk9, sg_chk10, sg_chk11, sg_chk12, tr_type1, tr_type2, tr_type3):
        url = f"https://m.land.naver.com/search/result/{keyword}"
        self.driver.get(url)

        input("Enter Start!")

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        script_content = soup.find("script", string=re.compile("jsonPageData"))

        if script_content:
            script_content = script_content.string
            value = script_content.split("filter: {")[1].split("}")[0].replace(" ", "").replace("'", "")

            lat = value.split("lat:")[1].split(",")[0]
            lon = value.split("lon:")[1].split(",")[0]
            z = value.split("z:")[1].split(",")[0]
            cortarNo = value.split("cortarNo:")[1].split(",")[0]
            #rletTpCds = value.split("rletTpCds:")[1].split(",")[0]
            #tradTpCds = value.split("tradTpCds:")[1].split()[0]
            tradTpCds = []
            rletTpCds = []

            if tr_type1:
                tradTpCds.append("A1")
            if tr_type2:
                tradTpCds.append("B1")
            if tr_type3:
                tradTpCds.append("B2")

            if sg_chk1:
                rletTpCds.append("APT")
            if sg_chk2:
                rletTpCds.append("OPST")
            if sg_chk3:
                rletTpCds.append("ABYG")
            if sg_chk4:
                rletTpCds.append("OBYG")
            if sg_chk5:
                rletTpCds.append("VL")
            if sg_chk6:
                rletTpCds.append("JWJT")
            if sg_chk7:
                rletTpCds.append("SGJT")
            if sg_chk8:
                rletTpCds.append("SG")
            if sg_chk9:
                rletTpCds.append("SMS")
            if sg_chk10:
                rletTpCds.append("GJCG")
            if sg_chk11:
                rletTpCds.append("GM")
            if sg_chk12:
                rletTpCds.append("TJ")

            rletTpCds_value = ':'.join(rletTpCds)
            tradTpCds_value = ':'.join(tradTpCds)

            lat_margin = 0.118
            lon_margin = 0.111

            btm = float(lat) - lat_margin
            lft = float(lon) - lon_margin
            top = float(lat) + lat_margin
            rgt = float(lon) + lon_margin

            remaked_URL = f"https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo={cortarNo}&rletTpCd={rletTpCds_value}&tradTpCd={tradTpCds_value}&z={z}&lat={lat}&lon={lon}&btm={btm}&lft={lft}&top={top}&rgt={rgt}"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
            }
            res2 = requests.get(remaked_URL, headers=headers)
            json_str = json.loads(res2.text)

            values = json_str['data']['ARTICLE']

            for v in values:
                lgeo = v['lgeo']
                count = v['count']
                z2 = v['z']
                lat2 = v['lat']
                lon2 = v['lon']

                len_pages = count / 20 + 1
                for idx in range(1, math.ceil(len_pages)):
                    remaked_URL2 = "https://m.land.naver.com/cluster/ajax/articleList?""itemId={}&mapKey=&lgeo={}&showR0=&" \
                                   "rletTpCd={}&tradTpCd={}&z={}&lat={}&""lon={}&totCnt={}&cortarNo={}&page={}" \
                        .format(lgeo, lgeo, rletTpCds_value, tradTpCds_value, z2, lat2, lon2, count, cortarNo, idx)

                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
                    }
                    res3 = requests.get(remaked_URL2, headers=headers)

                    try:
                        json_data2 = json.loads(res3.text)

                        for item in json_data2['body']:
                            atclCfmYmd = item.get('atclCfmYmd', "")
                            if atclCfmYmd == datetime.now().strftime("%y.%m.%d."):
                                atclNo = item.get('atclNo', "")
                                atclFetrDesc = item.get('atclFetrDesc', "")
                                rletTpNm = item.get('rletTpNm', "")
                                tradTpNm = item.get('tradTpNm', "")
                                prc = item.get('prc', "")
                                spc1 = item.get('spc1', "")
                                spc2 = item.get('spc2', "")
                                hanPrc = item.get('hanPrc', "")
                                rentPrc = item.get('rentPrc', "")
                                flrInfo = item.get('flrInfo', "")
                                tagList = item.get('tagList', [])
                                rltrNm = item.get('rltrNm', "")
                                detaild_information = "https://m.land.naver.com/article/info/{}".format(atclNo)

                                spc1_in_pyung = float(spc1) / 3.3
                                spc2_in_pyung = float(spc2) / 3.3

                                tablelist = [
                                    str(format(atclCfmYmd)),
                                    str(rletTpNm),
                                    str(tradTpNm),
                                    str(format(prc, ',')) + " 만원",
                                    str(spc1) + " m² (" + str(round(spc1_in_pyung, 2)) + " 평)",
                                    str(spc2) + " m² (" + str(round(spc2_in_pyung, 2)) + " 평)",
                                    str(hanPrc) + " 만원",
                                    str(format(rentPrc, ',') + " 만원"),
                                    str(atclFetrDesc),
                                    str(tagList),
                                    str(detaild_information)
                                ]

                                tableview.insert("", 'end', values=tablelist)
                                tableview.update()  # 업데이트
                                #
                                # wb = openpyxl.Workbook()
                                #
                                # ws = wb.active
                                #
                                # ws.append(tablelist)
                                #
                                # ws.append([str(atclCfmYmd),
                                #            str(rletTpNm),
                                #            str(tradTpNm),
                                #            str(prc),  # prc가 이미 만원 단위로 되어 있다면 삭제
                                #            str(spc1) + " m² (" + str(round(spc1_in_pyung, 2)) + " 평)",
                                #            str(spc2) + " m² (" + str(round(spc2_in_pyung, 2)) + " 평)",
                                #            str(hanPrc),
                                #            str(rentPrc),  # rentPrc가 이미 만원 단위로 되어 있다면 삭제
                                #            str(flrInfo),
                                #            str(tagList),
                                #            str(rltrNm),
                                #            detaild_information])
                                #
                                # btn_exportexcel.config(state="active")

                                print(f"물건번호: {atclNo}")
                                print(f"등록날짜: {atclCfmYmd}")
                                print(f"물건요약: {atclFetrDesc}")
                                print(f"상가구분: {rletTpNm}")
                                print(f"매매/전세/월세: {tradTpNm}")
                                print(f"가격: {prc}")
                                print(f"계약면적(m2): {spc1}")
                                print(f"전용면적(m2): {spc2}")
                                print(f"보증금: {hanPrc}")
                                print(f"월세: {rentPrc}")
                                print(f"층수(물건층/전체층): {flrInfo}")
                                print(f"기타 정보: {tagList}")
                                print(f"부동산: {rltrNm}")
                                print(f"상세 정보 링크: {detaild_information}")
                                print("-" * 50)
                                time.sleep(5)

                    except json.JSONDecodeError:
                        print("JSON DECODE Error")
                        continue

def start_crawling(entry, sg_chk1, sg_chk2, sg_chk3, sg_chk4, sg_chk5, sg_chk6, sg_chk7, sg_chk8, sg_chk9, sg_chk10, sg_chk11, sg_chk12, tr_type1, tr_type2, tr_type3):
    global tableview
    if tableview is not None:
        tableview.delete(*tableview.get_children())

    keyword = entry.get()
    if not keyword:
        messagebox.showerror("오류", "지역을 입력하세요.")
        return

    tableview.delete(*tableview.get_children())

    scraper = NaverRealEstateScraper()
    scraper.scrape_naver_real_estate(keyword, sg_chk1, sg_chk2, sg_chk3, sg_chk4, sg_chk5, sg_chk6, sg_chk7, sg_chk8, sg_chk9, sg_chk10, sg_chk11, sg_chk12, tr_type1, tr_type2, tr_type3)
    scraper.driver.quit()

def focus_in(entry):
    if entry.get() == '지역명 검색':
        entry.delete(0, tk.END)
        entry.configure(state=NORMAL)


def focus_out(entry, default_text):
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.configure(state='disabled')

# def btnsearchcmd():
#     maximum_count = 0
#     keyword = entry.get()
#
#     url = "https://m.land.naver.com/search/result/{}".format(keyword)
#     res = requests.get(url, headers=headers)
#     res.raise_for_status()
#
#     # NaverRealEstateScraper 클래스의 인스턴스 생성
#     scraper = NaverRealEstateScraper()
#     scraper.scrape_naver_real_estate(keyword, sg_chk1.get(), sg_chk2.get(), sg_chk3.get(),
#                                      sg_chk4.get(), sg_chk5.get(), sg_chk6.get(), sg_chk7.get(),
#                                      sg_chk8.get(), sg_chk9.get(), sg_chk10.get(), sg_chk11.get(), sg_chk12.get(),
#                                      tr_type1.get(), tr_type2.get(), tr_type3.get())
#
#     # 브라우저 닫기
#     scraper.driver.quit()
#
# def btnexportexcel():
#     global tablelist
#     keyword = entry.get()
#
#     # 데이터가 존재하는지 확인
#     if not tablelist:
#         messagebox.showinfo("데이터 없음", "추출된 정보가 없습니다.")
#         return
#
#     now = datetime.now()
#     nowDatetime = now.strftime('%Y%m%d_%H%M%S')
#
#     file_name = keyword + "_" + nowDatetime + ".xlsx"
#     wb = openpyxl.Workbook()  # 'wb' 변수를 여기서 정의합니다.
#     ws = wb.active
#     ws.append(["등록 일자", "상가 구분", "거래 유형", "가격", "계약면적(m2)", "전용면적(m2)", "보증금", "월세", "요약정보", "기타정보", "부동산", "상세링크"])
#
#     for item in tablelist:
#         ws.append(item)
#
#     wb.save(file_name)
#
#     messagebox.showinfo("파일 저장", "'" + file_name + "' 파일로 정상적으로 추출되었습니다.")
#
# def copy_row():
#     selected_item = tableview.focus()
#
#     if selected_item:
#         values = tableview.item(selected_item, 'values')
#
#         if values:
#             row_text = '\t'.join(values)
#             root.clipboard_clear()
#             root.clipboard_append(row_text)


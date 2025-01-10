import os
from db_connector import *
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = "C:/Windows/Fonts/malgun.ttf"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

def graph_data():
    toilet = fetch_data_from_mysql()
    station_out = fetch_station_out_count()
    station_in = fetch_station_in_count()

    # 결측치 제거 및 그룹화
    toilet.dropna(how='all', inplace=True, axis=1)
    ranking = (toilet.groupby("gu")["gu"].count()) / 5
    ranking.sort_values(ascending=False, inplace=True)

    # 특정 구 제거
    exclude_districts = ['강남구', '송파구', '종로구', '강서구', '노원구', '중구', '강동구',
                         '성동구', '광진구', '용산구', '양천구', '동작구', '관악구', '서대문구',
                         '금천구', '성북구', '중랑구', '구로구', '도봉구', '강북구']
    ranking.drop(index=exclude_districts, inplace=True)

    # 순서 지정
    new_order = ['동대문구', '마포구', '서초구', '영등포구', '은평구']
    line = ranking.reindex(new_order)

    # x와 y를 Classes 순서로 정렬
    Classes = ['동대문구', '마포구', '서초구', '영등포구', '은평구']
    x = station_in.set_index("Gu").reindex(Classes)["station_in_count"].fillna(0)
    y = station_out.set_index("Gu").reindex(Classes)["station_out_count"].fillna(0)

    # 그래프 생성
    fig = plt.figure(figsize=(10, 10))
    ax = fig.subplots(1, 1)

    # 막대 그래프 그리기
    ax.bar(range(len(x)), x, label='Station In', color='blue')
    ax.bar(range(len(y)), y, bottom=x, label='Station Out', color='orange')

    # x축 설정
    ax.set_xticks(range(len(Classes)))
    ax.set_xticklabels(Classes, fontsize=12, rotation=45)

    # y축 라벨 설정
    ax.set_ylabel("Count", fontsize=12)

    # 선 그래프 추가
    ax.plot(range(len(line.index)), line.values, color='black', marker='o', label='Toilet Usage')

    # 범례 추가
    ax.legend(fontsize=12)

    # 그래프 제목
    ax.set_title("통계 데이터 분석 결과", fontsize=14)

    # static 폴더에 이미지 경로 설정
    static_folder_path = os.path.join(os.getcwd(), 'static')
    graph_image_path = os.path.join(static_folder_path, 'graph_image.png')

    # 그래프 저장
    plt.tight_layout()
    plt.savefig(graph_image_path)

    # 이미지 경로 반환 (static 경로)
    return 'graph_image.png'

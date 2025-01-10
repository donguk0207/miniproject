import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

# 한글 글꼴 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

def generate_graph():
    # 데이터 정의 (마포구와 서울시)
    categories = ['인구수', '주택', '단독주택', '아파트', '교통문화지수']
    mapo_values = [361380, 124593, 10588, 74922, 80.96]
    seoul_values = [9384512, 3047650, 287312, 1831428, 76.36]

    # 1. 마포구, 서울시 인구수 비교 (Bar Chart)
    fig, ax = plt.subplots(1, 1, figsize=(5, 3))
    x = np.arange(1)  # x는 1로 설정, 한 번에 하나의 비교 그래프만 출력
    width = 0.35  # 막대 너비

    ax.bar(x - width / 2, mapo_values[0], width, label='마포구', color='skyblue')
    ax.bar(x + width / 2, seoul_values[0], width, label='서울시', color='orange')

    ax.set_ylabel('인구수')
    ax.set_title('마포구와 서울시 인구수 비교')
    ax.set_xticks(x)
    ax.set_xticklabels(['인구수'])
    ax.legend()

    # 퍼센티지만 표시 (수치는 제외)
    mapo_percent = (mapo_values[0] / seoul_values[0]) * 100
    seoul_percent = (seoul_values[0] / seoul_values[0]) * 100
    ax.text(-0.35, mapo_values[0] + 20000, f'{mapo_percent:.1f}%', ha='center', fontsize=10)
    ax.text(0.35, seoul_values[0] + 20000, f'{seoul_percent:.1f}%', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('static/population_comparison.png')

    # 2. 주택, 단독주택, 아파트 (Bar Chart)
    housing_labels = ['전체 주택', '단독주택', '아파트']
    mapo_housing = [124593, 10588, 74922]  # 마포구 주택 수
    seoul_housing = [3047650, 287312, 1831428]  # 서울시 주택 수

    fig, ax = plt.subplots(1, 1, figsize=(5, 3))

    x_pos = np.arange(len(housing_labels))  # x 좌표
    width = 0.35

    ax.bar(x_pos - width/2, mapo_housing, width, label='마포구', color='lightcoral')
    ax.bar(x_pos + width/2, seoul_housing, width, label='서울시', color='gold')

    ax.set_ylabel('주택 수')
    ax.set_title('마포구와 서울시 주택 분포')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(housing_labels)
    ax.legend()

    # 각 항목에 대한 퍼센티지 계산 및 표시
    for i in range(3):
        mapo_percent = (mapo_housing[i] / seoul_housing[i]) * 100
        seoul_percent = 100  # 서울시 값은 100%로 고정

        # 퍼센티지 표시
        ax.text(i - 0.35, mapo_housing[i] + 2000, f'{mapo_housing[i]:,.0f} ({mapo_percent:.1f}%)', ha='center', fontsize=10)
        ax.text(i + 0.35, seoul_housing[i] + 2000, f'{seoul_housing[i]:,.0f} ({seoul_percent:.1f}%)', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('static/housing_distribution.png')

    # 3. 교통문화지수 (Bar Chart)
    fig, ax = plt.subplots(1, 1, figsize=(5, 3))
    ax.bar(x - width/2, mapo_values[4], width, label='마포구', color='lightblue')
    ax.bar(x + width/2, seoul_values[4], width, label='서울시', color='yellowgreen')

    ax.set_ylabel('교통문화지수')
    ax.set_title('마포구와 서울시 교통문화지수 비교')
    ax.set_xticks(x)
    ax.set_xticklabels(['교통문화지수'])
    ax.legend()

    # 교통문화지수 퍼센티지 표시
    mapo_percent = (mapo_values[4] / seoul_values[4]) * 100
    seoul_percent = 100  # 서울시 값은 100%로 고정
    ax.text(-0.35, mapo_values[4] + 2, f'{mapo_values[4]:.1f} ({mapo_percent:.1f}%)', ha='center', fontsize=10)
    ax.text(0.35, seoul_values[4] + 2, f'{seoul_values[4]:.1f} ({seoul_percent:.1f}%)', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('static/traffic_culture_index.png')

    print("그래프 생성 완료")

# 서초구 데이터 추가 (새로운 함수로 생성)
def generate_seocho_graph():
    # 서초구 데이터 정의
    seocho_values = [437739, 128230, 4909, 91574, 76.15]  # 서초구 데이터
    seoul_values = [9384512, 3047650, 287312, 1831428, 76.36]  # 서울시 데이터

    # 1. 서초구와 서울시 인구수 비교 (Bar Chart)
    fig, ax = plt.subplots(1, 1, figsize=(5, 3))
    x = np.arange(1)  # x는 1로 설정, 한 번에 하나의 비교 그래프만 출력
    width = 0.35  # 막대 너비

    ax.bar(x - width/2, seocho_values[0], width, label='서초구', color='lightgreen')
    ax.bar(x + width/2, seoul_values[0], width, label='서울시', color='orange')

    ax.set_ylabel('인구수')
    ax.set_title('서초구와 서울시 인구수 비교')
    ax.set_xticks(x)
    ax.set_xticklabels(['인구수'])
    ax.legend()

    # 퍼센티지만 표시 (수치는 제외)
    seocho_percent = (seocho_values[0] / seoul_values[0]) * 100
    seoul_percent = (seoul_values[0] / seoul_values[0]) * 100
    ax.text(-0.35, seocho_values[0] + 20000, f'{seocho_percent:.1f}%', ha='center', fontsize=10)
    ax.text(0.35, seoul_values[0] + 20000, f'{seoul_percent:.1f}%', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('static/seocho_population_comparison.png')

    # 2. 서초구 주택, 단독주택, 아파트 (Bar Chart)
    housing_labels = ['전체 주택', '단독주택', '아파트']
    seocho_housing = [128230, 4909, 91574]  # 서초구 주택 수
    seoul_housing = [3047650, 287312, 1831428]  # 서울시 주택 수

    fig, ax = plt.subplots(1, 1, figsize=(5, 3))

    x_pos = np.arange(len(housing_labels))  # x 좌표
    width = 0.35

    ax.bar(x_pos - width/2, seocho_housing, width, label='서초구', color='lightgreen')
    ax.bar(x_pos + width/2, seoul_housing, width, label='서울시', color='gold')

    ax.set_ylabel('주택 수')
    ax.set_title('서초구와 서울시 주택 분포')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(housing_labels)
    ax.legend()

    # 각 항목에 대한 퍼센티지 계산 및 표시
    for i in range(3):
        seocho_percent = (seocho_housing[i] / seoul_housing[i]) * 100
        seoul_percent = 100  # 서울시 값은 100%로 고정

        # 퍼센티지 표시
        ax.text(i - 0.35, seocho_housing[i] + 2000, f'{seocho_housing[i]:,.0f} ({seocho_percent:.1f}%)', ha='center', fontsize=10)
        ax.text(i + 0.35, seoul_housing[i] + 2000, f'{seoul_housing[i]:,.0f} ({seoul_percent:.1f}%)', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('static/seocho_housing_distribution.png')

    # 3. 서초구 교통문화지수 (Bar Chart)
    fig, ax = plt.subplots(1, 1, figsize=(5, 3))
    ax.bar(x - width/2, seocho_values[4], width, label='서초구', color='lightgreen')
    ax.bar(x + width/2, seoul_values[4], width, label='서울시', color='yellowgreen')

    ax.set_ylabel('교통문화지수')
    ax.set_title('서초구와 서울시 교통문화지수 비교')
    ax.set_xticks(x)
    ax.set_xticklabels(['교통문화지수'])
    ax.legend()

    # 교통문화지수 퍼센티지 표시
    seocho_percent = (seocho_values[4] / seoul_values[4]) * 100
    seoul_percent = 100  # 서울시 값은 100%로 고정
    ax.text(-0.35, seocho_values[4] + 2, f'{seocho_values[4]:.1f} ({seocho_percent:.1f}%)', ha='center', fontsize=10)
    ax.text(0.35, seoul_values[4] + 2, f'{seoul_values[4]:.1f} ({seoul_percent:.1f}%)', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('static/seocho_traffic_culture_index.png')

    print("서초구 그래프 생성 완료")

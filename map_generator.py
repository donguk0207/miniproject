import folium
from folium.plugins import MarkerCluster
import pandas as pd
import requests
from db_connector import fetch_data_from_mysql, fetch_bike_usage_with_station_info


def create_map(data_seoul):
    # 기본 지도 생성 (서울 중심)
    map_object = folium.Map(location=[37.5665, 126.9780], zoom_start=12,
                            tiles='OpenStreetMap',
                            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')

    # 서울 행정구역 GeoJSON 데이터 불러오기
    r = requests.get(
        'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
    seoul_geo = r.json()

    # 서울 행정구역 GeoJson 레이어 추가
    geojson_layer = folium.GeoJson(
        seoul_geo,
        name='서울 행정구역',
        style_function=lambda x: {'fillColor': 'blue', 'color': 'blue', 'weight': 2, 'fillOpacity': 0.4}
    ).add_to(map_object)

    # 공중화장실 데이터 클러스터링
    marker_cluster = MarkerCluster(name='공중화장실').add_to(map_object)

    for _, row in data_seoul.iterrows():
        try:
            lat = float(row['Latitude'])
            lon = float(row['Longitude'])

            # 공중화장실 마커를 추가 (기존 클러스터링 유지)
            folium.Marker(
                location=[lat, lon],
                popup=f"""
                <b>{row['Name']}</b><br>
                <b>운영 시간:</b> {row['time']}<br>
                <b>비고:</b> {row['ohoh']}</b>
                """,
                icon=folium.Icon(color="blue", icon="info-sign"),  # 공중화장실은 파란색 아이콘
            ).add_to(marker_cluster)  # MarkerCluster에 추가

        except ValueError:
            pass  # Invalid latitude or longitude를 무시하고 넘어갑니다

    # 따릉이 대여/반납 데이터 추가
    bike_usage_data = fetch_bike_usage_with_station_info()

    # 따릉이 대여/반납 데이터 출력 (확인용)
    print("### Bike Usage Data ###")
    print(bike_usage_data.head())  # 데이터의 처음 5개 행 출력

    # 따릉이 대여/반납 카운트 계산
    rental_counts = bike_usage_data['Station_out'].value_counts().to_dict()
    return_counts = bike_usage_data['Station_in'].value_counts().to_dict()

    # 따릉이 대여/반납 데이터 레이어 (원형 표기)
    feature_group_bike = folium.FeatureGroup(name='따릉이 대여/반납').add_to(map_object)

    for _, row in bike_usage_data.iterrows():
        try:
            lat_out = float(row['Latitude_out'])
            lon_out = float(row['Longitude_out'])

            # 대여 지점 카운트
            station_out = row['Station_out']
            rental_count = rental_counts.get(station_out, 0)

            # 대여 지점에 대한 정보 출력 (확인용)
            print(
                f"Daeo Station: {station_out}, Latitude: {lat_out}, Longitude: {lon_out}, Rental Count: {rental_count}")

            # 따릉이 대여 지점은 원형 아이콘으로 표시
            folium.CircleMarker(
                location=[lat_out, lon_out],
                radius=8,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.6,
                popup=f"""
                <b>대여 지점:</b> {station_out}<br>
                <b>소모 탄소량:</b> {row['Carbon_amount']} kg<br>
                <b>대여 횟수:</b> {rental_count}회
                """
            ).add_to(feature_group_bike)  # FeatureGroup에 추가

        except ValueError:
            pass  # Invalid latitude or longitude를 무시하고 넘어갑니다

    # 따릉이 반납 지점은 원형 아이콘으로 표시
    for _, row in bike_usage_data.iterrows():
        try:
            lat_in = float(row['Latitude_in'])
            lon_in = float(row['Longitude_in'])

            # 반납 지점 카운트
            station_in = row['Station_in']
            return_count = return_counts.get(station_in, 0)

            # 반납 지점에 대한 정보 출력 (확인용)
            print(
                f"Return Station: {station_in}, Latitude: {lat_in}, Longitude: {lon_in}, Return Count: {return_count}")

            folium.CircleMarker(
                location=[lat_in, lon_in],
                radius=8,
                color='yellow',
                fill=True,
                fill_color='yellow',
                fill_opacity=0.6,
                popup=f"""
                <b>반납 지점:</b> {station_in}<br>
                <b>소모 탄소량:</b> {row['Carbon_amount']} kg<br>
                <b>반납 횟수:</b> {return_count}회
                """
            ).add_to(feature_group_bike)

        except ValueError:
            pass

    # 레이어 컨트롤 추가
    folium.LayerControl().add_to(map_object)

    # 지도 저장
    map_object.save('templates/map.html')


# 데이터 불러오기 및 지도 생성
if __name__ == "__main__":
    data_seoul = fetch_data_from_mysql()  # 서울시 공중화장실 데이터 가져오기
    create_map(data_seoul)  # 지도 생성

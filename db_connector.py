from sqlalchemy import create_engine
import pandas as pd

def fetch_data_from_mysql():
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/bike')

    #서울시 따릉이 정보
    query = """
    SELECT 
        Name, gu, detail, detail2, Longitude, Latitude, phone, gubun, gubun2, time, ohoh
    FROM seoul
    """
    data = pd.read_sql(query, con=engine)
    #print("Seoul 데이터:")
    return data


def fetch_bike_usage_with_station_info():
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/bike')

    query = """
    SELECT 
        bu.Date_out, 
        bu.Time_out, 
        bu.Station_no_out, 
        bu.Station_out, 
        bu.Membership_type,
        bu.Gender, 
        bu.Age_Group, 
        bu.Momentum, 
        bu.Station_no_in, 
        bu.Station_in, 
        bu.Date_in, 
        bu.AMPM, 
        bu.TIME_in, 
        bu.Bike_no, 
        bu.Carbon_amount, 
        bu.Distance, 
        bu.Duration, 
        s_out.Latitude AS Latitude_out, 
        s_out.Longitude AS Longitude_out, 
        s_in.Latitude AS Latitude_in, 
        s_in.Longitude AS Longitude_in
    FROM bike_usage bu
    LEFT JOIN stations s_out ON bu.Station_no_out = s_out.ID  -- 대여 station 정보
    LEFT JOIN stations s_in ON bu.Station_no_in = s_in.ID    -- 반납 station 정보
    """
    # SQL 쿼리 실행하여 데이터 가져오기
    data = pd.read_sql(query, con=engine)
    #print("Bike Usage + Station 정보:")
    return data

def graph_mysql():
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/bike')

    #graph정보
    query = """
    SELECT 
        Station_out, Station_no_out, Station_in, Station_no_in
    FROM bike_usage
    """
    data = pd.read_sql(query, con=engine)
    #print("Graph 데이터:")
    return data

def fetch_station_out_count():
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/bike')

    query = """
    SELECT 
        s.Gu,
        COUNT(b.station_no_out) AS station_out_count
    FROM stations s
    LEFT JOIN bike_usage b ON b.station_no_out = s.ID
    GROUP BY s.Gu
    ORDER BY station_out_count DESC    
    """
    data = pd.read_sql(query, con=engine)
    return data

def fetch_station_in_count():
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/bike')

    query = """
    SELECT 
        s.Gu,
        COUNT(b.station_no_in) AS station_in_count
    FROM stations s
    LEFT JOIN bike_usage b ON b.station_no_in = s.ID
    GROUP BY s.Gu
    ORDER BY station_in_count DESC
    """
    data = pd.read_sql(query, con=engine)
    return data

# if __name__ == "__main__":
#     # 각 함수 호출 및 데이터 출력
#     seoul_data = fetch_data_from_mysql()
#     print("서울 데이터:\n", seoul_data.head())
#
#     bike_usage_data = fetch_bike_usage_with_station_info()
#     print("Bike Usage 데이터:\n", bike_usage_data.head())
#
#     graph_data = graph_mysql()
#     print("Graph 데이터:\n", graph_data.head())
#
#     x = fetch_station_in_count()
#     print("x 데이터:\n", fetch_station_in_count())
#     y = fetch_station_out_count()
#     print("y 데이터:\n", fetch_station_out_count())
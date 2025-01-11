import requests

import gpxpy
import gpxpy.gpx

import math
from datetime import timedelta

# 트랙 데이터 출력
# TODO: 데이터를 pandas 형태로 반환
def extract_track_data(gpx_data):
    for track in gpx_data.tracks:
        for segment in track.segments:
            prev_point = None
            i = 0
            for point in segment.points:
                latitude = point.latitude
                longitude = point.longitude
                elevation = point.elevation
                time = point.time
                
                # 각 트랙 포인트 출력
                print(f"Point {i}: Latitude: {latitude}, Longitude: {longitude}, Elevation: {elevation}, Time: {time}")
                if prev_point != None:
                    print(f"Speed from {i-1} -> {i}: {calculate_speed(prev_point, point)} km/h")
                
                prev_point = point
                i += 1

# 위도, 경도를 하버사인 공식을 이용해서 거리로 변환
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

# 수평경로와 수직경로, 시간차를 이용해서 속도를 계산
def calculate_speed(point1, point2):
    latlng_distance = haversine(point1.latitude, point1.longitude, point2.latitude, point2.longitude) # km
    final_distance = math.sqrt(latlng_distance ** 2 + ((point1.elevation - point2.elevation) / 1000) ** 2) # km
    time = (point2.time - point1.time).total_seconds() / 3600 # hour
    if time > 0:
        return round(final_distance / time, 4) # km/h
    else:
        return 0

# 위도, 경도 정보로 도로 위치를 반환하는 함수
def request_road_data(latitude: float, longitude: float):
    url = "http://overpass-api.de/api/interpreter"

    # Overpass QL 쿼리, 반경 20미터 내의 모든 도로 정보를 가져온다
    overpass_query = f"""
    [out:json];
    way["highway"](around:20, {latitude}, {longitude});
    out body;
    """

    params = {
        "data": overpass_query
    }

    response = requests.get(url, params=params)
    return response.json()

# TODO: pandas 정보로 변환하기
def print_road_data(data):
    for element in data['elements']:
        if 'tags' in element and 'highway' in element['tags']:
            print(f"도로 정보: {element}")
            # print(f"도로 ID: {element['id']}, 도로 종류: {element['tags']['highway']}")
            # print("도로 태그:", element['tags'])

if __name__ == "__main__":
    '''
    with open('sample.gpx', 'r') as f:
        gpx = gpxpy.parse(f)
    
    extract_track_data(gpx)
    '''

    print_road_data(request_road_data(37.57034709741047, 126.97866257296211))

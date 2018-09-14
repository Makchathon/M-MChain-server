# M-MChain-server
HYCON HACKS

## API

### /post
장소에 사진 등록하고 토큰 얻기. 5 Maro Token이 지급됩니다.

#### request
POST

**Body**

- user: hycon wallet address
- longitude: 경도
- latitude: 위도
- tags: 태그, list
- img: 사진, file
- memo

#### response

```json
{
    "latitude": "0.1234566",
    "longitude": "0.6543211",
    "memo": "여기가 KBS 아레나홀의 정문입니다.",
    "place_id": 7,  # 등록된 장소 번호
    "tags": [ "입구", "정문" ],
    "transaction_hash": "생성된 트랜잭션의 해시값"
}
```



### /get
입력된 위치의 반경 범위 내에 등록된 장소 목록 조회

#### request
GET

**Query String**

- longitude: 경도
- latitude: 위도
- range: 반경 범위, float

```
decimal  degrees    distance
-------------------------------
0        1.0        111 km
1        0.1        11.1 km
2        0.01       1.11 km
3        0.001      111 m
4        0.0001     11.1 m
5        0.00001    1.11 m
6        0.000001   0.111 m
7        0.0000001  1.11 cm
8        0.00000001 1.11 mm
```

#### response

```json
{
    "places": [
        {
            "create_time": "Fri, 14 Sep 2018 12:48:40 GMT",
            "id": 6,  # 장소 번호
            "img_name": "moon.jpg",  # 이미지 이름
            "latitude": 0.123457,
            "longitude": 0.654321,
            "memo": "memo",
            "tags": "one,two",
            "user_address": "hycon wallet address"
        }, ...
}
```



### /img/$place_id
장소에 저장된 이미지를 조회한다

#### request
GET

- $place_id: 장소 번호

#### response

img

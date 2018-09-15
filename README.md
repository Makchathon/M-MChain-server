# M-MChain-server
HYCON HACKS


## HYCON configuration

```
$ cd bundle-linux
$ vim data/config.json
{
    "os":"linux",
    "dataGenesis":"./data/genesis.dat",
    "dataRaw":"./data/raw",
    "dataRoot":"./data",
    "dataWallet":"./wallet",
    "minerAddress":"H2Mcy6LBFmiEzp3C1bed9VV6UEDd6CNCg",
    "txPoolMaxAddresses":36000,
    "txPoolMaxTxsPerAddress":64
}

$ ./hycon --api --api_port=2442 --cpuMiners=1 --bootstrap --networkid=marofan --nonLocal --port=8148 $@
```

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

```
{
    "latitude": "0.1234566",
    "longitude": "0.6543211",
    "memo": "여기가 KBS 아레나홀의 정문입니다.",
    "place_id": 7,  # 등록된 장소 번호
    "tags": [ "입구", "정문" ],
    "transaction_hash": "생성된 트랜잭션의 해시값"
}
```


---


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

```
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


---


### /img/$place_id
장소에 저장된 이미지를 조회한다

#### request
GET

- $place_id: 장소 번호

#### response

img


---


### /tags
태그 자동완성을 위해 태그 검색한다

#### request
GET

**Query String**

- q: 검색할 태그

#### response

```
{
    "tags": [
        {
            "id": 10,  # 태그 번호
            "tag": "입구"
        }
    ]
}
```


---


### /balance
잔액 조회하기

#### request
POST

**Body**

- address: hycon wallet address

#### response

```
{
    "balance": "296639.999999954"
}
```


---


### /vote
장소에 투표하기

#### request

**Body**

- place_id: 장소 번호
- from: 투표하는 hycon wallet address
- vote_type: 0: 조항요, 1: 싫어요
- memo: 메모

#### response

```
{
    "from_txHash": "6GdzX5njAPQQ39NdMxgwWWu1PAzWzX6o4ZJcdrqd6H9x",
    "from_user": "Hx6uqLefV1pK8CiLuFtHQGcdPaRq7mP9",
    "vote_id": 2,
    "memo": "사진 예쁘네요~",
    "place_id": "24",
    "to_txHash": null,
    "to_user": null,
    "vote_type": "0"
}
```

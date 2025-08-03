# 챔피언 이름 데이터

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHAMPIONS = [
    {"ko": "가렌", "en": "Garen"}, {"ko": "갈리오", "en": "Galio"}, {"ko": "갱플랭크", "en": "Gangplank"},
    {"ko": "그라가스", "en": "Gragas"}, {"ko": "그레이브즈", "en": "Graves"}, {"ko": "그웬", "en": "Gwen"},
    {"ko": "나르", "en": "Gnar"}, {"ko": "나미", "en": "Nami"}, {"ko": "나서스", "en": "Nasus"}, {"ko": "나피리", "en": "Naafiri"},
    {"ko": "노틸러스", "en": "Nautilus"}, {"ko": "녹턴", "en": "Nocturne"}, {"ko": "누누와 윌럼프", "en": "Nunu"},
    {"ko": "니달리", "en": "Nidalee"}, {"ko": "니코", "en": "Neeko"}, {"ko": "닐라", "en": "Nilah"},
    {"ko": "다리우스", "en": "Darius"}, {"ko": "다이애나", "en": "Diana"}, {"ko": "드레이븐", "en": "Draven"},
    {"ko": "라이즈", "en": "Ryze"}, {"ko": "라칸", "en": "Rakan"}, {"ko": "람머스", "en": "Rammus"},
    {"ko": "럭스", "en": "Lux"}, {"ko": "럼블", "en": "Rumble"}, {"ko": "레나타 글라스크", "en": "Renata"},
    {"ko": "레넥톤", "en": "Renekton"}, {"ko": "레오나", "en": "Leona"}, {"ko": "렉사이", "en": "RekSai"},
    {"ko": "렐", "en": "Rell"}, {"ko": "렝가", "en": "Rengar"}, {"ko": "루시안", "en": "Lucian"},
    {"ko": "룰루", "en": "Lulu"}, {"ko": "르블랑", "en": "Leblanc"}, {"ko": "리 신", "en": "LeeSin"},
    {"ko": "리븐", "en": "Riven"}, {"ko": "리산드라", "en": "Lissandra"}, {"ko": "릴리아", "en": "Lillia"},
    {"ko": "마스터 이", "en": "MasterYi"}, {"ko": "마오카이", "en": "Maokai"}, {"ko": "말자하", "en": "Malzahar"},
    {"ko": "말파이트", "en": "Malphite"}, {"ko": "멜", "en": "Mel"}, {"ko": "모데카이저", "en": "Mordekaiser"},
    {"ko": "모르가나", "en": "Morgana"}, {"ko": "문도 박사", "en": "DrMundo"}, {"ko": "미스 포츈", "en": "MissFortune"},
    {"ko": "밀리오", "en": "Milio"}, {"ko": "바드", "en": "Bard"}, {"ko": "바루스", "en": "Varus"},
    {"ko": "바이", "en": "Vi"}, {"ko": "베이가", "en": "Veigar"}, {"ko": "베인", "en": "Vayne"},
    {"ko": "벡스", "en": "Vex"}, {"ko": "벨베스", "en": "Belveth"}, {"ko": "벨코즈", "en": "Velkoz"},
    {"ko": "볼리베어", "en": "Volibear"}, {"ko": "브라움", "en": "Braum"}, {"ko": "브라이어", "en": "Briar"},
    {"ko": "브랜드", "en": "Brand"}, {"ko": "블라디미르", "en": "Vladimir"}, {"ko": "블리츠크랭크", "en": "Blitzcrank"},
    {"ko": "비에고", "en": "Viego"}, {"ko": "빅토르", "en": "Viktor"}, {"ko": "뽀삐", "en": "Poppy"},
    {"ko": "사미라", "en": "Samira"}, {"ko": "사이온", "en": "Sion"}, {"ko": "사일러스", "en": "Sylas"},
    {"ko": "샤코", "en": "Shaco"}, {"ko": "세나", "en": "Senna"}, {"ko": "세라핀", "en": "Seraphine"},
    {"ko": "세주아니", "en": "Sejuani"}, {"ko": "세트", "en": "Sett"}, {"ko": "소나", "en": "Sona"},
    {"ko": "소라카", "en": "Soraka"}, {"ko": "쉔", "en": "Shen"}, {"ko": "쉬바나", "en": "Shyvana"},
    {"ko": "스몰더", "en": "Smolder"}, {"ko": "스웨인", "en": "Swain"}, {"ko": "스카너", "en": "Skarner"},
    {"ko": "시비르", "en": "Sivir"}, {"ko": "신 짜오", "en": "XinZhao"}, {"ko": "신드라", "en": "Syndra"},
    {"ko": "신지드", "en": "Singed"}, {"ko": "쓰레쉬", "en": "Thresh"}, {"ko": "아리", "en": "Ahri"},
    {"ko": "아무무", "en": "Amumu"}, {"ko": "아우렐리온 솔", "en": "AurelionSol"}, {"ko": "아이번", "en": "Ivern"},
    {"ko": "아지르", "en": "Azir"}, {"ko": "아칼리", "en": "Akali"}, {"ko": "아크샨", "en": "Akshan"},
    {"ko": "아트록스", "en": "Aatrox"}, {"ko": "아펠리오스", "en": "Aphelios"}, {"ko": "알리스타", "en": "Alistar"},
    {"ko": "암베사", "en": "Ambessa"}, {"ko": "애니", "en": "Annie"}, {"ko": "애니비아", "en": "Anivia"},
    {"ko": "애쉬", "en": "Ashe"}, {"ko": "야스오", "en": "Yasuo"}, {"ko": "에코", "en": "Ekko"},
    {"ko": "엘리스", "en": "Elise"}, {"ko": "오공", "en": "MonkeyKing"}, {"ko": "오로라", "en": "Aurora"},
    {"ko": "오른", "en": "Ornn"}, {"ko": "오리아나", "en": "Orianna"}, {"ko": "올라프", "en": "Olaf"},
    {"ko": "요네", "en": "Yone"}, {"ko": "요릭", "en": "Yorick"}, {"ko": "우디르", "en": "Udyr"},
    {"ko": "우르곳", "en": "Urgot"}, {"ko": "워윅", "en": "Warwick"}, {"ko": "유나라", "en": "Yunara"},
    {"ko": "유미", "en": "Yuumi"}, {"ko": "이렐리아", "en": "Irelia"}, {"ko": "이블린", "en": "Evelynn"},
    {"ko": "이즈리얼", "en": "Ezreal"}, {"ko": "일라오이", "en": "Illaoi"}, {"ko": "자르반 4세", "en": "JarvanIV"},
    {"ko": "자야", "en": "Xayah"}, {"ko": "자이라", "en": "Zyra"}, {"ko": "자크", "en": "Zac"},
    {"ko": "잔나", "en": "Janna"}, {"ko": "잭스", "en": "Jax"}, {"ko": "제드", "en": "Zed"},
    {"ko": "제라스", "en": "Xerath"}, {"ko": "제리", "en": "Zeri"}, {"ko": "제이스", "en": "Jayce"},
    {"ko": "조이", "en": "Zoe"}, {"ko": "직스", "en": "Ziggs"}, {"ko": "진", "en": "Jhin"},
    {"ko": "질리언", "en": "Zilean"}, {"ko": "징크스", "en": "Jinx"}, {"ko": "초가스", "en": "Chogath"},
    {"ko": "카르마", "en": "Karma"}, {"ko": "카밀", "en": "Camille"}, {"ko": "카사딘", "en": "Kassadin"},
    {"ko": "카서스", "en": "Karthus"}, {"ko": "카시오페아", "en": "Cassiopeia"}, {"ko": "카이사", "en": "Kaisa"},
    {"ko": "카직스", "en": "Khazix"}, {"ko": "카타리나", "en": "Katarina"}, {"ko": "칼리스타", "en": "Kalista"},
    {"ko": "케넨", "en": "Kennen"}, {"ko": "케이틀린", "en": "Caitlyn"}, {"ko": "케인", "en": "Kayn"},
    {"ko": "케일", "en": "Kayle"}, {"ko": "코그모", "en": "KogMaw"}, {"ko": "코르키", "en": "Corki"},
    {"ko": "퀸", "en": "Quinn"}, {"ko": "크산테", "en": "KSante"}, {"ko": "클레드", "en": "Kled"},
    {"ko": "키아나", "en": "Qiyana"}, {"ko": "킨드레드", "en": "Kindred"}, {"ko": "타릭", "en": "Taric"},
    {"ko": "탈론", "en": "Talon"}, {"ko": "탈리야", "en": "Taliyah"}, {"ko": "탐 켄치", "en": "TahmKench"},
    {"ko": "트런들", "en": "Trundle"}, {"ko": "트리스타나", "en": "Tristana"}, {"ko": "트린다미어", "en": "Tryndamere"},
    {"ko": "트위스티드 페이트", "en": "TwistedFate"}, {"ko": "트위치", "en": "Twitch"}, {"ko": "티모", "en": "Teemo"},
    {"ko": "파이크", "en": "Pyke"}, {"ko": "판테온", "en": "Pantheon"}, {"ko": "피들스틱", "en": "Fiddlesticks"},
    {"ko": "피오라", "en": "Fiora"}, {"ko": "피즈", "en": "Fizz"}, {"ko": "하이머딩거", "en": "Heimerdinger"},
    {"ko": "헤카림", "en": "Hecarim"}, {"ko": "흐웨이", "en": "Hwei"}
]

def get_champion_image_path(champion_en_name):
    """
    챔피언의 영문 이름으로부터 이미지 경로를 생성합니다.
    절대 경로를 반환합니다.
    """
    return os.path.join(PROJECT_ROOT, "resources", "images", "champions", f"{champion_en_name}.png")

def get_champion_by_ko(ko_name):
    """
    한글 이름으로 챔피언 정보를 찾습니다.
    """
    for champion in CHAMPIONS:
        if champion["ko"] == ko_name:
            return champion
    return None

def get_champion_by_en(en_name):
    """
    영문 이름으로 챔피언 정보를 찾습니다.
    """
    for champion in CHAMPIONS:
        if champion["en"] == en_name:
            return champion
    return None

def get_champion_data():
    """
    모든 챔피언의 데이터를 반환합니다.
    반환 형식: [(한글이름, 영문이름, 이미지경로), ...]
    """
    return [(champ["ko"], champ["en"], get_champion_image_path(champ["en"])) 
            for champ in CHAMPIONS]
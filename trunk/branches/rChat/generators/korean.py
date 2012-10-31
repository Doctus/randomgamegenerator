import random

def _getKoreanMaleName():
  names = ["An", "Anjo", "An-Kor", "Bawoo", "Bihn", "Bok", "Bon", "Bong-Chol", "Byung", "Chae", "Chae-Ku", "Chang", "Chang-Sun", "Chayoon", "Cheol", "Chiwoong", "Chol", "Chong", "Chong-Il", "Chong-Sik", "Choong-Kyu", "Chul", "Chul-Soo", "Chung-Hee", "Chungsong", "Dae", "Daehyun", "Daein", "Daejung", "Daesuk", "Dahn", "Daijon", "Dohnbi", "Dokyun", "Don", "Dong", "Donghyun", "Dongju", "Dongmoon", "Dongsoo", "Dong-uk", "Doohwan", "Duhbean", "Eujin (Eugene)", "Eun", "Gil", "Gi-Su", "Haein", "Haesup", "Hahn", "Han", "Ha-Ung", "Hee", "Hejoon", "Ho-Bong", "Hongchol", "Hongdo", "Hong-Gil", "Hong-Il", "Hoon", "Hosu", "Hunwoo", "Hwankul", "Hwansuk", "Hyangsoon", "Hyon", "Hyonho", "Hyoung-Zoo", "Hyun", "Hyung", "Hyun-Gi", "Hyun-Ki", "Hyunshik", "Hyunwoo", "Inchul", "In-Jung", "Innsu", "Insoo", "In-Tak", "Jae", "Jaehwa", "Jaehyun", "Jaekyung", "Jaesun", "Jaeyup", "Jay", "Jayhoon", "Jayon", "Jea", "Jeanhwan", "Jee", "Jeeyoung", "Jeonghwa", "Jeyong", "Ji", "Jiho", "Jihoon", "Jiin", "Jikwang", "Jimin", "Jin (Gene)", "Jinho", "Jinsoo", "Jinsoon", "Jinsu", "Jinsung", "Jinwu", "Jinyong", "Jinyoung", "Jisung", "Jitae", "Jiwoong", "Jiyoung", "Jon", "Jong", "Jongkyu", "Joo", "Joon", "Joonho", "Joonil", "Joonyeop", "Joosub", "Joung", "Jun", "Jung", "Jung-Keun", "Jung-Mo", "Jungsiek", "Jungho", "Junil", "Junoh", "Keehowan", "Ki", "Kihyuk", "Kim", "Kisang", "Kokwan", "Kon", "Ku", "Kum-Shik", "Kunhae", "Kunwoo", "Kwan", "Kwang", "Kwangjoon", "Kwangsu", "Kyong", "Kyoungjoo", "Kyu", "Kyu-Hwang", "Kyu-Hyuk", "Kwulyon", "Kwungtae", "Mahnsei", "Manyoung", "Mein", "Min", "Minjoong", "Minsok", "Minsoo", "Mo", "Myon", "Myongbok", "My-Sung", "Myung", "Myungdae", "Myungsok", "Pyung", "Rany", "Re-il", "Saechul", "Saejung", "Sang", "Seeneun", "Sehun", "Sejin", "Sel", "Seo", "Seon", "Seung", "Seunghae", "Seunghwa", "Seung-Lip", "Seungmee", "Shun", "Sihyun", "Siwoo", "Sohn", "Soksan", "Sol", "Son", "Song", "Songchol", "Song-gye", "Song-ho", "Song-Won", "Sonyung", "Soo-Ann", "Soohwan", "Soo-Hyun", "Soon", "Soon-Jin", "Soon-Ok", "Soon-Yul", "So-Young", "Subin", "Suck", "Sun", "Sung", "Sunghan", "Sunghyun", "Sungjin", "Sungmin", "Sungwon", "Sungwoo", "Sunkyu", "Tae", "Taegene", "Taeho", "Taehyun", "Taesong", "Taewan", "Taewoo", "Te", "Tong-Lim", "Unee", "Wah-Bo", "Wen-Mu", "Weon", "Won", "Wonmyong", "Won-Shik", "Woo", "Woo-il", "Woun", "Yeonjin", "Yeonsoo", "Yihwan", "Yon", "Yong", "Yongcheol", "Yongdong", "Yongjin", "Yongjun", "Yongsun", "Yoo", "Yoojim", "Yosup", "Young", "Young-Bum", "Youngchul", "Youngha", "Younghan", "Youngho", "Younghoon", "Youngjae", "Youngjun", "Youngmin", "Youngsam", "Young-uk", "Youngsoo", "Yu", "Yun", "Yun-Bok", "Yungbin", "Yung-il", "Yun-man"]
  return random.choice(names)

def _getKoreanFemaleName():
  names = ["Aei-young", "Ae-Sook", "Aesun", "Bo", "Bohyun", "Boksoon", "Bong", "Boyoung", "Byungsoon", "Chanhee", "Chanri", "Chansook", "Chee", "Cheng", "Cho", "Choe", "Chong", "Chongkak", "Choonyei", "Chunja", "Dahee", "Danbee", "Dasom", "Dayoung", "Dooree", "E", "Eujin", "Eun", "Euna", "Eunie", "Eunio", "Eunjee", "Eunmi", "Eunseong", "Eunsook", "Eunyoung", "Eurie", "Fun", "Geesun", "Gihei", "Gitte", "Giwon", "Hae", "Haein", "Haimi", "Han", "Hana", "Hanh", "Heae", "Hee", "Heesok", "Heewon", "Heyne", "Hong", "Hwa", "Hwan", "Hwasoo", "Hwasoon", "Hyaejoo", "Hyang", "Hyangsoon", "Hye", "Hye-young", "Hyo", "Hyoisoon", "Hyojin", "Hyun", "Hyungsook", "Hyunji", "Hyunjoo", "Hyunjung", "Hyunsil", "In", "Jae", "Jaemi", "Jaemin", "Jaeun", "Jaewon", "Jeahyoun", "Jean", "Jeanyoung", "Jee", "Jeehee", "Jeeyen", "Jene", "Ji", "Jieun", "Jihye", "Jihyun", "Jimin", "Jin", "Jina", "Jinseon", "Jinyoung", "Ji-Soo", "Jisun", "Jiyeon", "Jongeun", "Jonghui", "Joo", "Joohee", "Ju", "Juk", "Jumi", "Junghye", "Jungjun", "Jungming", "Jungpark", "Juni", "Jurie", "Ki", "Kimi", "Kiyoun", "Kunhee", "Kwansook", "Kyunghee", "Kyungja", "Kyungmin", "Kyungsil", "Kyungwook", "Kyu-Soo", "Kyuunghwa", "Lim", "Mija", "Meehoy", "Mehee", "Mi", "Mijin", "Min", "Mina", "Minee", "Minjeong", "Minji", "Minkyom", "Minna", "Misook", "Misoon", "Miyeon", "Moon", "Moonkyung", "Moonsun", "Mynjy", "Myongsuk", "Myung", "Myunghee", "Myungsun", "Nahmjin", "Nahre", "Namsin", "Nara", "Naree", "Nary", "Nayon", "Nook-Soo", "Ok", "Ok-Hee", "Okhwa", "Okjim", "Okmyung", "Oksun", "Rina", "Saehyun", "Sanghee", "Sangjin", "Sangme", "Sary", "Se", "Seami", "Seo", "Seongshin", "Seonhwa", "Seonkoo", "Shin", "Sina", "So", "Somy", "Son", "Sonyong", "Soo", "Soo-ai", "Soohyun", "Soojean", "Soojin", "Soojung", "Sookyung", "Soon", "Soonae", "Soonbok", "Soon-ei", "Sooneun", "Soon-Yi", "Soorah", "Sooyeon", "Soo-Yun", "Soyoung", "Su", "Suejean", "Sugee", "Suji", "Sujin", "Sumi", "Sun", "Sung", "Sung-hee", "Sung-hyon", "Sunhee", "Sunmi", "Sun-Young", "Syungsoon", "Taemi", "Taeseon", "Un", "Unie", "Wann", "Wanntha", "Woju", "Won", "Woonhe", "Woosoon", "Yaerim", "Yane", "Yanggae", "Yena", "Yeonjoo", "Yeun", "Yeunja", "Yisu", "Yong", "Yongsook", "Yongsuk", "Yoojin", "Yoomee", "Yoonah", "Yoonmi", "Young", "Younghee", "Young-Hi", "Youngja", "Youngkyung", "Youngmi", "Youngnae", "Yu", "Yumee", "Yumi", "Yumin", "Yun", "Yuna", "Yunee", "Yung-li", "Yuni", "Yunji", "Yunkyung", "Yuri", "Zung-Bok"]
  return random.choice(names)

def _getKoreanRandomName():
  if random.choice([True, False]):
    return _getKoreanMaleName()
  return _getKoreanFemaleName()

def _getKoreanSurname():
  names = ["Kim", "Lee", "Park", "Choi", "Chung", "Ae", "Ahn", "An", "Aum", "Back", "Bae", "Baek", "Bahk", "Bahng", "Bai", "Baik", "Bak", "Ban", "Bang", "Bann", "Bong", "Boo", "Bou", "Bu", "Byon", "Byun", "Cha", "Chae", "Chang", "Chay", "Cheng", "Cheon", "Cheun", "Chey", "Chin", "Cho", "Choe", "Choie", "Chol", "Chon", "Chong", "Choo", "Chou", "Chough", "Choung", "Choy", "Chu", "Chuey", "Chun", "Chwae", "Chweh", "Chyu", "Coh", "Doh", "Dong", "Duk", "Ehn", "Eu", "Eum", "Eun", "Gang", "Gen", "Gil", "Goe", "Goh", "Gook", "Gu", "Gwang", "Gwon", "Ha", "Hahm", "Hahn", "Han", "Hee", "Heo", "Ho", "Hong", "Houng", "Huh", "Hung", "Hwang", "Hye", "Hyon", "Hyun", "Hyung", "I", "Ihm", "Ihn", "Il", "Im", "Imm", "Jang", "Jee", "Jeon", "Jeong", "Jeung", "Jhin", "Jhung", "Ji", "Jin", "Jo", "Jon", "Jong", "Joung", "Jun", "Jung", "Kae", "Kah", "Kahm", "Kahng", "Kan", "Kang", "Kay", "Kei", "Keung", "Key", "Ki", "Kil", "Kimm", "Ko", "Koh", "Kong", "Koo", "Ku", "Kuk", "Kwaak", "Kwak", "Kwang", "Kwon", "Kwun", "Kye", "Kyeung", "Kym", "Kyu", "Kyung", "Lah", "Leen", "Lew", "Lho", "Li", "Lim", "Lyung", "Ma", "Maeng", "Marh", "Min", "Mo", "Moh", "Moon", "Mun", "Myong", "Myung", "Na", "Nah", "Nahm", "Nam", "Namkoong", "Namkung", "Ngai", "Nho", "No", "Noh", "O", "Ock", "Oh", "Ohm", "Ohn", "Ok", "Owh", "Pae", "Paeck", "Paek", "Paick", "Paik", "Pak", "Pong", "Pyo", "Pyon", "Pyun", "Ra", "Ree", "Rha", "Rhee", "Rheem", "Rhim", "Rho", "Rhough", "Ri", "Rim", "Ro", "Roe", "Roh", "Ron", "Row", "Ryom", "Ryoo", "Ryu", "Sam", "San", "Sang", "Seo", "Seol", "Ser", "Seul", "Sheen", "Shim", "Shin", "Shon", "Shyn", "Si", "Sik", "Sin", "Sinn", "So", "Soh", "Sohn", "Sohnn", "Son", "Sone", "Song", "Soo", "Sook", "Soon", "Suh", "Suhr", "Suk", "Sul", "Sull", "Sung", "Sunoo", "Sur", "Sye", "Sym", "Synn", "Tack", "Tae", "Tak", "Thyu", "Tok", "Tsai", "Tse", "Uh", "Uhm", "Um", "Un", "Ung", "Wang", "Weon", "Whang", "Whangbo", "Whong", "Wi", "Wohn", "Won", "Woo", "Worr", "Yang", "Ye", "Yee", "Yeo", "Yeon", "Yi", "Yim", "Yom", "Yon", "Yong", "Yoo", "Yook", "Yoon", "You", "Youj", "Youk", "Youn", "Young", "Yu", "Yum", "Yun", "Zew", "Zo"]
  return random.choice(names)

def _getKoreanMaleFullName():
  return (_getKoreanSurname() + " " + _getKoreanMaleName())

def _getKoreanFemaleFullName():
  return (_getKoreanSurname() + " " + _getKoreanFemaleName())

def _getKoreanRandomFullName():
  return (_getKoreanSurname() + " " + _getKoreanRandomName())

def getName(args):
    if args == "help": return "Generates a Korean name. Valid arguments are 'full' or 'surname' (given-only will be assumed if neither is passed) and 'male' or 'female'."
    elif "female" in args and "full" in args:
        return _getKoreanFemaleFullName()
    elif "male" in args and "full" in args:
        return _getKoreanMaleFullName()
    elif "male" in args:
        return _getKoreanMaleName()
    elif "female" in args:
        return _getKoreanFemaleName()
    elif "surname" in args:
        return _getKoreanSurname()
    elif "full" in args:
        return _getKoreanRandomFullName()
    else:
        return _getKoreanRandomName()

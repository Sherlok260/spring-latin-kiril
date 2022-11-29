# This Python file uses the following encoding: utf-8
import os, sys
import string
import re

# from trie import trie_from_words

class Trie():
	"""Regex::Trie in Python. Creates a Trie out of a list of words. The trie can be exported to a Regex pattern.
    The corresponding Regex should match much faster than a simple Regex union."""

	def __init__(self):
		self.data = {}

	def add(self, word):
		ref = self.data
		for char in word:
			ref[char] = char in ref and ref[char] or {}
			ref = ref[char]
		ref[''] = 1

	def dump(self):
		return self.data

	def quote(self, char):
		return re.escape(char)

	def _pattern(self, pData):
		data = pData
		if "" in data and len(data.keys()) == 1:
			return None

		alt = []
		cc = []
		q = 0
		for char in sorted(data.keys()):
			if isinstance(data[char], dict):
				try:
					recurse = self._pattern(data[char])
					alt.append(self.quote(char) + recurse)
				except:
					cc.append(self.quote(char))
			else:
				q = 1
		cconly = not len(alt) > 0

		if len(cc) > 0:
			if len(cc) == 1:
				alt.append(cc[0])
			else:
				alt.append('[' + ''.join(cc) + ']')

		if len(alt) == 1:
			result = alt[0]
		else:
			result = "(?:" + "|".join(alt) + ")"

		if q:
			if cconly:
				result += "?"
			else:
				result = "(?:%s)?" % result
		return result

	def pattern(self):
		return self._pattern(self.dump())

def trie_from_words(words):
	trie = Trie()
	for word in words:
		trie.add(word)
	return trie.pattern()


LATIN_TO_CYRILLIC = {
    'a': 'а', 
    'b': 'б', 
    'd': 'д', 
    'e': 'е', 
    'f': 'ф', 
    'g': 'г', 
    'h': 'ҳ', 
    'i': 'и', 
    'j': 'ж', 
    'k': 'к', 
    'l': 'л', 
    'm': 'м',
    'n': 'н', 
    'o': 'о', 
    'p': 'п', 
    'q': 'қ',   
    'r': 'р',
    's': 'с', 
    't': 'т', 
    'u': 'у', 
    'v': 'в', 
    'x': 'х',
    'y': 'й', 
    'z': 'з', 
    # TODO: case?  ’
}
LATIN_VOWELS = (
    'a',  'e', 'i',  'o',  'u',  "oㄹ",
)

# These words cannot be reliably converted to cyrillic because of the lossy
# nature of the to_latin converter.
TS_WORDS = {
    "sirka" : "сирка",
    "fris" : "фриц",
    "ranes" : "ранец",
    "nenes" : "ненец",
    "abzas" : "абзац",
    "slanes" : "сланец",
    "shpris" : "шприц",
    "ensefal" : "энцефал",
    "esmines" : "эсминец",
    "marganes" : "марганец",
    "konsentr" : "концентр",
    "batsilla" : "бацилла" ,
    "konferens" : "конференц",
    "konfutsiy" : "конфуций",
    "minonoses" : "миноносец",
    "ordinares" : "ординарец",
    "pestitsid" : "пестицид",
    "kompanyon" : "компаньон",
    "avianoses" : "авианосец",
    "biomitsin" : "биомицин" ,
    "ssintigraf" : "сцинтиграф",
    "munitsipal" : "муниципал" ,
    "bronenoses" : "броненосец",
    "penitsillin" : "пенициллин",
    "месенат" : "меценат" ,
    "avtopritsep" : "автоприцеп",
	'aberratsion':'аберрацион',
	'abzats':'абзац',
	'abstraksionizm':'абстракционизм',
	'abstraksionist':'абстракционист',
	'abssess':'абсцесс',
	'avianosets':'авианосец',
	'avtoprsep':'автопрцеп',
	'agitatsion':'агитацион',
	'agnostitsizm':'агностицизм',
	'aksent':'акцент',
	'aksiz':'акциз',
	'aksioner':'акционер',
	'aksionerlik':'акционерлик',
	'aksiyadorlik':'акциядорлик',
	'antitsiklon':'антициклон',
	'antratsit':'антрацит',
	'appenditsit':'аппендицит',
	'attestatsion':'аттестацион',
	'atsetilen':'ацетилен',
	'atseton':'ацетон',
	'azitromitsin':'azitromitsin',
	'bakteritsid':'бактерицид',
	'batsillar':'бациллар',
	'biolyuminessensiya':'биолюминесценция',
	'botsman':'боцман',
	'bronenosets':'броненосец',
	'brutsellyoz':'бруцеллёз',
	'vaksina':'вакцина',
	'vegetatsion':'вегетацион',
	'ventilyatsion':'вентиляцион',
	'vitse-':'вице-',
	'vitse-admiral':'вице-адмирал',
	'vitse-prezident':'вице-президент',
	'gallitsizm':'галлицизм',
	'gastrol-konsert':'гастроль-концерт',
	'gaubitsa':'гаубица',
	'geliotsentrik':'гелиоцентрик',
	'genotsid':'геноцид',
	'geotsentrik':'геоцентрик',
	'gerbitsidlar':'гербицидлар',
	'gers':'герц',
	'gersog':'герцог',
	'giatsint':'гиацинт',
	'gipotsentr':'гипоцентр',
	'glitserin':'глицерин',
	'glyatsiolog':'гляциолог',
	'glyatsiologiya':'гляциология',
	'gorchitsa':'горчица',
	'gusenitsa':'гусеница',
	'dezinfeksiyalamoq':'дезинфекцияламоқ',
	'deklamatsiyachi':'декламациячи',
	'derivatsion':'деривацион',
	'detsigramm':'дециграмм',
	'detsilitr':'децилитр',
	'detsimetr':'дециметр',
	'differensial':'дифференциал',
	'differensiyalamoq':'дифференцияламоқ',
	'dotsent':'доцент',
	'jinoiy-protsessual':'жиноий-процессуал',
	'izolyatsion':'изоляцион',
	'izolyatsiyalamoq':'изоляцияламоқ',
	'inersiyali':'инерцияли',
	'inssenirovka':'инсценировка',
	'intervensiyachi':'интервенциячи',
	'internatsional':'интернационал',
	'internatsionalizm':'интернационализм',
	'internatsionalist':'интернационалист',
	'intonatsion':'интонацион',
	'informatsion':'информацион',
	'irratsional':'иррационал',
	'irrigatsion':'ирригацион',
	'kalsiy':'кальций',
	'kanseliyariya':'канцелиярия',
	'kanserogen':'канцероген',
	'kansler':'канцлер',
	'katolsizm':'католцизм',
	'kvars':'кварц',
	'kvarsit':'кварцит',
	'kinokonsert':'киноконцерт',
	'kinossenariy':'киносценарий',
	'klassitsizm':'классицизм',
	'koalitsion':'коалицион',
	'kolleksioner':'коллекционер',
	'kolleksiyachchi':'коллекцияччи',
	'kolonsifra':'колонцифра',
	'kompozitsion':'композицион',
	'konditsioner':'кондиционер',
	'konsorsium':'консорциум',
	'konstitutsion':'конституцион',
	'konstitutsiyaviy':'конституциявий',
	'kontrrevolyutsion':'контрреволюцион',
	'kontrrevolyutsioner':'контрреволюционер',
	'konferens-zal':'конференц-зал',
	'konfutsiylik':'конфуцийлик',
	'konfutsiychilik':'конфуцийчилик',
	'konsentrat':'концентрат',
	'konsentratli':'концентратли',
	'konsentratsion':'концентрацион',
	'konsentratsiyalashmoq':'концентрациялашмоқ',
	'konsentrik':'концентрик',
	'konsern':'концерн',
	'konsert':'концерт',
	'konsertmeyster':'концертмейстер',
	'konsessiya':'концессия',
	'konslager':'концлагерь',
	'koordinatsion':'координацион',
	'koeffitsiyent':'коэффициент',
	'kulminatsion':'кульминацион',
	'lanset':'ланцет',
	'levomitsetin':'левомицетин',
	'leykotsitlar':'лейкоцитлар',
	'leykotsitoz':'лейкоцитоз',
	'litsey':'лицей',
	'litsenziya':'лицензия',
	'lotsman':'лоцман',
	'lyutetsiy':'лютеций',
	'marganets':'марганец',
	'matritsa':'матрица',
	'meditsina':'медицина',
	'mexanizatsiyalash':'механизациялаш',
	'mexanizatsiyalashmoq':'механизациялашмоқ',
	'mexanitsizm':'механицизм',
	'mizanssena':'мизансцена',
	'militsioner':'милиционер',
	'militsiyaxona':'милицияхона',
	'mineralizatsiya':'минерализация',
	'minonosets':'миноносец',
	'mistitsizm':'мистицизм',
	'modernizatsiyalamoq':'модернизацияламоқ',
	'mototsiklet':'мотоциклет',
	'mototsikletchi':'мотоциклетчи',
	'mototsiklli':'мотоциклли',
	'mototsiklchi':'мотоциклчи',
	'multiplikatsion':'мультипликацион',
	'munitsipalitet':'муниципалитет',
	'nenets':'ненец',
	'nenetslar':'ненецлар',
	'neomitsin':'неомицин',
	'nitroglitserin':'нитроглицерин',
	'okkupatsion':'оккупацион',
	'okkupatsiyachi':'оккупациячи',
	'operatsiyaviy':'операциявий',
	'oppozotsion':'оппозоцион',
	'oppozitsiyachi':'оппозициячи',
	'ordinarets':'ординарец',
	'ofitser':'офицер',
	'ofitsiant':'официант',
	'ofitsiantka':'официантка',
	'parasetamol':'парацетамол',
	'patsiyent':'пациент',
	'patsifizm':'пацифизм',
	'patsifist':'пацифист',
	'penitssilin':'пениццилин',
	'pestitsidlar':'пестицидлар',
	'petlitsa':'петлица',
	'pinset':'пинцет',
	'pitssa':'пицца',
	'platsdarm':'плацдарм',
	'platskart':'плацкарт',
	'platskarta':'плацкарта',
	'platskartali':'плацкартали',
	'plebissit':'плебисцит',
	'pozitsion':'позицион',
	'politsiyachi':'полициячи',
	'politsmeyster':'полицмейстер',
	'potensial':'потенциал',
	'prinsip':'принцип',
	'prinsipial':'принципиал',
	'prinsipiallik':'принципиаллик',
	'prinsipli':'принципли',
	'prinsipsiz':'принципсиз',
	'pritsep':'прицеп',
	'provinsializm':'провинциализм',
	'provinsiya':'провинция',
	'proyeksiyalamoq':'проекцияламоқ',
	'proporsional':'пропорционал',
	'proporsionallik':'пропорционаллик',
	'proteksionizm':'протекционизм',
	'protsent':'процент',
	'protsentli':'процентли',
	'protsentchi':'процентчи',
	'protsess':'процесс',
	'protsessor':'процессор',
	'protsessual':'процессуал',
	'publitsist':'публицист',
	'publitsistik':'публицистик',
	'publitsistika':'публицистика',
	'punktuatsion':'пунктуацион',
	'radiatsion':'радиацион',
	'ranets':'ранец',
	'rafinatsiyalash':'рафинациялаш',
	'ratsion':'рацион',
	'ratsional':'рационал',
	'ratsionalizator':'рационализатор',
	'ratsionalizatorlik':'рационализаторлик',
	'ratsionalizatsiya':'рационализация',
	'ratsionalizm':'рационализм',
	'ratsionalist':'рационалист',
	'ratsionlallashmoq':'рационлаллашмоқ',
	'reaksion':'реакцион',
	'reaksioner':'реакционер',
	'reaksiya':'реакция',
	'reaksiyachi':'реакциячи',
	'revolyutsion':'революцион',
	'revolyutsioner':'революционер',
	'rekognossirovka':'рекогносцировка',
	'rekonstruksiyalamoq':'реконструкцияламоқ',
	'retsenzent':'рецензент',
	'retsenziya':'рецензия',
	'retsept':'рецепт',
	'retseptorlar':'рецепторлар',
	'retsidiv':'рецидив',
	'retsidivist':'рецидивист',
	'retsipiyent':'реципиент',
	'ritsarlik':'рицарлик',
	'ritsar':'рицарь',
	'rotatsion':'ротацион',
	'sanatsiyalash':'санациялаш',
	'seleksiyachi':'селекциячи',
	'seleksiyachilik':'селекциячилик',
	'silitsiy':'силиций',
	'skeptitsizm':'скептицизм',
	'slanets':'сланец',
	'sotsial':'социал',
	'sotsial-demokrat':'социал-демократ',
	'sotsial-demokratik':'социал-демократик',
	'sotsial-demokratiya':'социал-демократия',
	'sotsializm':'социализм',
	'sotsialist':'социалист',
	'sotsialistik':'социалистик',
	'sotsiolingvistika':'социолингвистика',
	'sotsiolog':'социолог',
	'sotsiologik':'социологик',
	'sotsiologiya':'социология',
	'spetsifik':'специфик',
	'spetsifika':'специфика',
	'statsionar':'стационар',
	'stoitsizm':'стоицизм',
	'stronsiy':'стронций',
	'ssenariy':'сценарий',
	'ssenariychi':'сценарийчи',
	'ssenarist':'сценарист',
	'tablitsa':'таблица',
	'tansa':'танца',
	'teleinssenirovka':'телеинсценировка',
	'tendensioz':'тенденциоз',
	'tendensiozlik':'тенденциозлик',
	'teplitsa':'теплица',
	'terset':'терцет',
	'texnetsiy':'технеций',
	'traditsion':'традицион',
	'transkripsion':'транскрипцион',
	'transkripsiyalamoq':'транскрипцияламоқ',
	'translyatsion':'трансляцион',
	'transformatsiyalamoq':'трансформацияламоқ',
	'uborshitsa':'уборшица',
	'unifikatsiyalashtirmoq':'унификациялаштирмоқ',
	'farmatsevtika':'фармацевтика',
	'film-konsert':'фильм-концерт',
	'fitonsid':'фитонцид',
	'fraksiooner':'фракциоонер',
	'fransuz':'француз',
	'fransuzlar':'французлар',
	'fransuzcha':'французча',
	'frits':'фриц',
	'funksional':'функционал',
	'furatsilin':'фурацилин',
	'xoletsistit':'холецистит',
	'sanga':'цанга',
	'sapfa':'цапфа',
	'sedra':'цедра',
	'seziy':'цезий',
	'seytnot':'цейтнот',
	'sellofan':'целлофан',
	'selluloid':'целлулоид',
	'sellyuloza':'целлюлоза',
	'selsiy':'цельсий',
	'sement':'цемент',
	'sementlamoq':'цементламоқ',
	'senz':'ценз',
	'senzor':'цензор',
	'senzura':'цензура',
	'sent':'цент',
	'sentner':'центнер',
	'sentnerli':'центнерли',
	'sentnerchi':'центнерчи',
	'sentralizm':'централизм',
	'sentrizm':'центризм',
	'sentrist':'центрист',
	'sentrifuga':'центрифуга',
	'seriy':'церий',
	'sesarka':'цесарка',
	'sex':'цех',
	'sian':'циан',
	'sianli':'цианли',
	'sivilizatsiya':'цивилизация',
	'sigara':'цигара',
	'sikl':'цикл',
	'siklik':'циклик',
	'sikllashtirmoq':'цикллаштирмоқ',
	'siklli':'циклли',
	'siklon':'циклон',
	'siklotron':'циклотрон',
	'silindr':'цилиндр',
	'silindrik':'цилиндрик',
	'silindrli':'цилиндрли',
	'sink':'цинк',
	'sinkograf':'цинкограф',
	'sinkografiya':'цинкография',
	'sirk':'цирк',
	'sirkoniy':'цирконий',
	'sirkul':'циркуль',
	'sirkulyar':'циркуляр',
	'sirkchi':'циркчи',
	'sirroz':'цирроз',
	'sisterna':'цистерна',
	'sisternali':'цистернали',
	'sistit':'цистит',
	'sitata':'цитата',
	'sitatabozlik':'цитатабозлик',
	'sito-':'цито-',
	'sitodiagnostika':'цитодиагностика',
	'sitokimyo':'цитокимё',
	'sitoliz':'цитолиз',
	'sitologiya':'цитология',
	'sitrus':'цитрус',
	'siferblat':'циферблат',
	'siferblatli':'циферблатли',
	'sokol':'цоколь',
	'sunami':'цунами',
	'cherepitsa':'черепица',
	'shveysar':'швейцар',
	'shmutstitul':'шмуцтитул',
	'shnitsel':'шницель',
	'shprits':'шприц',
	'shtangensirkul':'штангенциркуль',
    "shveytsariya":"швейцария",
    "sitsiliya":"сицилия",
    "syerra-leone":"сьерра-леоне",
	'evolyutsion':'эволюцион',
	'egotsentrizm':'эгоцентризм',
	'ekspeditsion':'экспедицион',
	'ekspeditsiyachi':'экспедициячи',
	'ekspluatatsiyachi':'эксплуатациячи',
	'emotsional':'эмоционал',
	'emotsionallik':'эмоционаллик',
	'empiriokrititsizm':'эмпириокритицизм',
	'ensefalit':'энцефалит',
	'ensefalogramma':'энцефалограмма',
	'ensiklopedik':'энциклопедик',
	'ensiklopedist':'энциклопедист',
	'ensiklopediya':'энциклопедия',
	'ensiklopediyachi':'энциклопедиячи',
	'epitsentr':'эпицентр',
    'eritrotsit':'эритроцит',
	'eritrotsitlar':'эритроцитлар',
	'eritrotsitoliz':'эритроцитолиз',
	'eritrotsitopatiya':'эритроцитопатия',
	'esminets':'эсминец',
   
}
# These words cannot be reliably transliterated into cyrillic
OTHER_WORDS = {
    "tarjimayi" : "таржимаи",
    "nuqtayi" : "нуқтаи",
    "sahobayi" : "саҳобаи",
    "press-papye" : "пресс-папье",
    'beletaj': 'бельэтаж',
    'bugun-erta': 'бугун-эрта',
    "diqqat-eㄹtibor": 'диққат-эътибор',
    'ich-et': 'ич-эт',
    'karate': 'каратэ',
    "obroㄹ-eㄹtibor": "обрў-эътибор",
    'omon-eson': 'омон-эсон',
    'reket': 'рэкет',
    'sutemizuvchilar': 'сутэмизувчилар',
    'upa-elik': 'упа-элик',
    'xayr-ehson': 'хайр-эҳсон',
    'qaynegachi': 'қайнэгачи',
    'ishoq' : 'исҳоқ',
    'jarayon' : 'жараён',
    'mushaf': 'мусҳаф',
    "mer":"мэр",
    'general-mayor': 'генерал-майор',
    "yogㄹ": 'йог',
    'yoga': 'йога',
    "kalendar":"календарь",
    'yogurt': 'йогурт',
    'yod': 'йод',
    'yodlamoq': 'йодламоқ',
    'yodli': 'йодли',
    'mayonez': 'майонез',
    'mikrorayon': 'микрорайон',
    'mayor': 'майор',
    'rayon': 'район',
    'moyupa': 'мойупа',
    'singa':'цинга',
    'poyustun': 'пойустун',
    'poyabzal': 'пойабзал',
    'poyandoz': 'пойандоз',
    'poyafzal': 'пойафзал',
    'iye': 'ийе',
    'konveyer': 'конвейер',
    'pleyer': 'плейер',
    'stayer': 'стайер',
    'foye': 'фойе',
#      == > 
    "mil" : "миль",
    "vimpel" : "вимпель",
    "sirkul" : "циркуль",
    "shtepsel" : "штепсель",
    "rentabel" : "рентабель",
    "feldyeger" : "фельдъегерь",
    "avtomagistral" : "автомагистраль",
    'aviamodel': 'авиамодель',
    'avtomobil': 'автомобиль',
    'akvarel': 'акварель',
    'alkogol': 'алкоголь',
    'ansambl': 'ансамбль',
    'aprel': 'апрель',
    'artel': 'артель',
    'barrel': 'баррель',
    'banderol': 'бандероль',
    'binokl': 'бинокль',
    'verf': 'верфь',
    'vestibyul': 'вестибюль',
    'broneavtomobil': 'бронеавтомобиль',
    'bron': 'бронь',    
    'byulleten': 'бюллетень',
    'vanil': 'ваниль',    
    'vedomost': 'ведомость',
    'veksel': 'вексель',
    'ventil': 'вентиль',
    'vermishel': 'вермишель',    
    'violonchel': 'виолончель',
    'vklyuchatel': 'включатель',
    'vodevil': 'водевиль',
    'volost': 'волость',    
    'viklyuchatel': 'виключатель',    
    'gavan': 'гавань',    
    'gantel': 'гантель',
    'garmon': 'гармонь',
    'gastrol': 'гастроль',    
    'gorizontal': 'горизонталь',
    'gospital': 'госпиталь',
    'grifel': 'грифель',
    'guash': 'гуашь',    
    'dvigatel': 'двигатель',    
    'dekabr': 'декабрь',    
    'detal': 'деталь',
    'diagonal': 'диагональ',    
    'dizel': 'дизель',
    'dirijabl': 'дирижабль',
    'drel': 'дрель',
    'duel': 'дуэль',
    'inventar': 'инвентарь',    
    'iyul': 'июль',
    'iyun': 'июнь',
    'kabel': 'кабель',
    'kalendar': 'календарь',    
    'kanifol': 'канифоль',    
    'kapsyul': 'капсюль',
    'karamel': 'карамель',
    'kartel': 'картель',
    'kartech': 'картечь',
    'karusel': 'карусель',    
    'kastryul': 'кастрюль',    
    'kafel': 'кафель',    
    'kisel': 'кисель',
    'kitel': 'китель',
    'knyaz': 'князь',    
    'kokil': 'кокиль',
    'kokteyl': 'коктейль',    
    'kontrol': 'контроль',    
    'konslager': 'концлагерь',
    'kon': 'конь',    
    'korol': 'король',
    'kreml': 'кремль',
    'krovat': 'кровать',
    'lager': 'лагерь',
    'latun': 'латунь',
    'losos': 'лосось',    
    'magistral': 'магистраль',    
    'mebel': 'мебель',
    'medal': 'медаль',    
    'migren': 'мигрень',    
    'model': 'модель',    
    'monastir': 'монастирь',    
    'motel': 'мотель',    
    'neft': 'нефть',
    'nikel': 'никель',
    'nippel': 'ниппель',
    'nol': 'ноль',
    'normal': 'нормаль',
    'noyabr': 'ноябрь',
    'oblast': 'область',    
    'otel': 'отель',    
    'ochered': 'очередь',    
    'panel': 'панель',
    'parallel': 'параллель',
    'parol': 'пароль',
    'patrul': 'патруль',
    'pedal': 'педаль',    
    'pechat': 'печать',
    'pech': 'печь',    
    'plastir': 'пластирь',
    'povest': 'повесть',
    'portfel': 'портфель',
    'porshen': 'поршень',    
    'predoxranitel': 'предохранитель',    
    'press-sekretar': 'пресс-секретарь',
    'pristan': 'пристань',
    'profil': 'профиль',
    'radiospektakl': 'радиоспектакль',    
    'retush': 'ретушь',
    'riyel': 'риель',
    'ritsar': 'рицарь',
    'rol': 'роль',
    'royal': 'рояль',    
    'rubl': 'рубль',
    'rul': 'руль',    
    'sekretar': 'секретарь',    
    'seld': 'сельдь',
    'siren': 'сирень',
    'skalpel': 'скальпель',
    'slesar': 'слесарь',
    'sobol': 'соболь',
    'spektakl': 'спектакль',
    'spiral': 'спираль',    
    'sterjen': 'стержень',
    'stil': 'стиль',
    'tabel': 'табель',    
    'tekstil': 'текстиль',    
    'tigel': 'тигель',
    'tokar': 'токарь',
    'tol': 'толь',
    'tonnel': 'тоннель',
    'tunnel': 'туннель',
    'tush': 'тушь',
    'tyulen': 'тюлень',
    'tyul': 'тюль',    
    'util': 'утиль',    
    'fevral': 'февраль',    
    "feldㄹeger": 'фельдъегерь',    
    'festival': 'фестиваль',    
    'fonar': 'фонарь',
    'sirkul': 'циркуль',
    'sokol': 'цоколь',
    'chizel': 'чизель',
    'shagren': 'шагрень',
    'shampun': 'шампунь',
    'sherst': 'шерсть',
    'shinel': 'шинель',    
    'xrustal': 'хрусталь',    
    'shnitsel': 'шницель',
    'shpatel': 'шпатель',    
    'shpindel': 'шпиндель',
    'shtangensirkul': 'штангенциркуль',
    'shtapel': 'штапель',
    'shtempel': 'штемпель',
    'emal': 'эмаль',    
    'endshpil': 'эндшпиль',    
    'yakor': 'якорь',
    'yuan': 'юань'
  
}
SOFT_SIGN_WORDS = {
    "ultra" : "ультра",
    "syezd" : "съезд",
    "pyesa" : "пьеса",
    "multi" : "мульти",
    "subyekt" : "субъект",
    "letyete" : "варьете",
    "vernyer" : "верньер",
    "atelye" : "ателье",
    "balneo" : "бальнео",
    "baryer" : "барьер",
    "bulyon" : "бульон",
    "bullet" : "бульвар",
    "fakult" : "факульт",
    "galvan" : "гальван",
    "karyer" : "карьер",
    "kuryer" : "курьер",
    "losyon" : "лосьон",
    "obyekt" : "объект",
    "rantye" : "рантье",
    "relyef" : "рельеф",
    "senyor" : "сеньор",
    "konyunktura" : "коньюнктура",
    "konyuktivit" : "коньюктивит",
    "kulmina" : "кульмина",
    "kultiva" : "культива",
    "partyer" : "партьер",
    "premyer" : "премьер",
    "razyezd" : "разъезд",
    "belgiya" : "бельгия",
    "medalyon" : "медальон",
    "modelyer" : "модельер",
    "pavilyon" : "павильон",
    "pechenye" : "печенье",
    "konsulta" : "консульта",
    "brakoner" : "браконьер",
    "falsifik" : "фальсифик",
    "kalkulya" : "калькуля",
    "barelyef" : "барельеф",
    "batalyon" : "батальон",
    "fotoalbom" : "фотоальбом",
    "aryergard" : "арьергард",
    "oftalmolog" : "офтальмолог",
    "pochtalyon" : "почтальон",
    "pulmonolog" : "пульмонолог",
    "fotoatelye" : "фотоателье",
    "gotovalniy" : "готовальний",
    "marselyeza" : "марсельеза",
    "adyunktura" : "адъюнктура",
    "konferansye" : "конферансье",
    "monokultura" : "монокультура",
    "sutemizuvchi" : "сутэмизувчи",
    'sentabr': 'сентябрь',  
    'jenshen': 'женьшень',
    'yanvar': 'январь',
    'oktabr': 'октябрь',
    'avtomagistralavtomat': 'автомагистральавтомат',
    'albatros': 'альбатрос',
    'albom': 'альбом',
    'alpinizm': 'альпинизм',
    'alpinist': 'альпинист',
    'alt': 'альт',
    'alternativ': 'альтернатив',
    'alternativa': 'альтернатива',
    'altimetr': 'альтиметр',
    'altchi': 'альтчи',
    'alfa': 'альфа',
    'alfa-zarralar': 'альфа-зарралар',
    'alma-terapiya': 'альма-терапия',
    'alyans': 'альянс',
    'amalgama': 'амальгама',
    'apelsin': 'апельсин',
    'artikl': 'артикль',
    'arergard': 'арьергард',
    'asfalt': 'асфальт',
    'asfaltlamoq': 'асфальтламоқ',
    'asfaltli': 'асфальтли',
    'atele': 'ателье',
    'bazalt': 'базальт',
    'balzam': 'бальзам',
    'balzamlash': 'бальзамлаш',
    'balneolog': 'бальнеолог',
    'balneologik': 'бальнеологик',
    'balneologiya': 'бальнеология',
    'balneoterapiya': 'бальнеотерапия',
    'balneotexnika': 'бальнеотехника',
    'barelef': 'барельеф',
    'barer': 'барьер',
    'batalon': 'батальон',
    'belveder': 'бельведер',
    'belgiyalik': 'бельгиялик',
    'belting': 'бельтинг',
    'beletaj': 'бельэтаж',
    'bilyard': 'бильярд',
    'biofiltr': 'биофильтр',
    'bolonya': 'болонья',
    'bolshevizm': 'большевизм',
    'bolshevik': 'большевик',
    'brakonerlik': 'браконьерлик',
    'budilnik': 'будильник',
    'bulvar': 'бульвар',
    'buldenej': 'бульденеж',
    'buldog': 'бульдог',
    'buldozer': 'бульдозер',
    'buldozerlar':'бульдозерлар',
    'bulonlar':'булонлар',
    'buldozerchi': 'бульдозерчи',
    'bulon': 'бульон',
    'valeryanka': 'валерьянка',
    'valvatsiya': 'вальвация',
    'vals': 'вальс',
    'varete': 'варьете',
    'verner': 'верньер',
    'videofilm': 'видеофильм',
    'vinetka': 'виньетка',
    'volt': 'вольт',
    'volta': 'вольта',
    'voltli': 'вольтли',
    'voltmetr': 'вольтметр',
    'volfram': 'вольфрам',
    'vulgar': 'вульгар',
    'vulgarizm': 'вульгаризм',
    'vulgarlashtirmoq': 'вульгарлаштирмоқ',
    'galvanizatsiya': 'гальванизация',
    'galvanik': 'гальваник',
    'galvanometr': 'гальванометр',
    'gastrol-konsert': 'гастроль-концерт',
    'gelmint': 'гельминт',
    'gelmintoz': 'гельминтоз',
    'gelmintologiya': 'гельминтология',
    'geraldika': 'геральдика',
    'gilza': 'гильза',
    'giposulfit': 'гипосульфит',
    'golf': 'гольф',
    'golfchi' : 'гольфчи',
    'gorelef': 'горельеф',  
    'dalton': 'дальтон',
    'daltonik': 'дальтоник',
    'daltonizm': 'дальтонизм',
    'devalvatsiya': 'девальвация',
    'delta': 'дельта',
    'delfin': 'дельфин',
    'delfinariy': 'дельфинарий',
    'delfinsimonlar': 'дельфинсимонлар',
    'diafilm': 'диафильм',
    'dizel-motor': 'дизель-мотор',
    'impuls': 'импульс',
    'insult': 'инсульт',
    'intervyu': 'интервью',
    'interer': 'интерьер',
    'italyan': 'итальян',
    'italyanlar': 'итальянлар',
    'italyancha': 'итальянча',
    'kalka': 'калька',
    'kalkalamoq': 'калькаламоқ',
    'kalkulyator': 'калькулятор',
    'kalkulyatsiya': 'калькуляция',
    'kalsiy': 'кальций',
    'kapelmeyster': 'капельмейстер',
    'karer': 'карьер',
    'karyera': 'карьера',
    'kastryulka': 'кастрюлька',
    'katapulta': 'катапульта',
    'kinofestival': 'кинофестиваль',
    'kinofilm': 'кинофильм',
    'kobalt': 'кобальт',
    'kompyuter': 'компьютер',
    'kompyuterlashtirmoq': 'компьютерлаштирмоқ',
    'konsultant': 'консультант',
    'konsultativ': 'консультатив',
    'konsultatsiya': 'консультация',
    'konferanse': 'конферансье',
    'konki': 'коньки',
    'konkichi': 'конькичи',
    'konyunktiva': 'коньюнктива',
    'konyunktivit': 'коньюнктивит',
    'konyunktura': 'коньюнктура',
    'konyak': 'коньяк',
    'kulminatsion': 'кульминацион',
    'kulminatsiya': 'кульминация',
    'kultivator': 'культиватор',
    'kultivatsiya': 'культивация',
    'kultivatlash' : 'культиватлаш',
    'kulturizm': 'культуризм',
    'kurer': 'курьер',
    'kyat': 'кьят',
    'loson': 'лосьон',
    'marseleza': 'марсельеза',
    'medalon': 'медальон',
    'melxior': 'мельхиор',
    'menshevizm': 'меньшевизм',
    'menshevik': 'меньшевик',
    'mikroinsult': 'микроинсульт',
    'mikrofilm': 'микрофильм',
    'modeler': 'модельер',
    'molbert': 'мольберт',
    'monokultoura': 'монокультоура',
    'multi-': 'мульти-',
    'multimediya': 'мультимедия',
    'multimillioner': 'мультимиллионер',
    'multiplikatsion': 'мультипликацион',
    'multiplikator': 'мультипликатор',
    'multiplikatsiya': 'мультипликация',
    'nimpalto': 'нимпальто',
    'okkultizm': 'оккультизм',
    'oftalmologiya': 'офтальмология',
    'pavilon': 'павильон',
    'palma': 'пальма',
    'palmazor': 'пальмазор',
    'palpatsiya': 'пальпация',
    'palto': 'пальто',
    'paltobop': 'пальтобоп',
    'paltolik': 'пальтолик',
    'penalti': 'пенальти',
    'pechene': 'печенье',
    'polka': 'полька',
    'pochtalon': 'почтальон',
    'premera': 'премьера',
    'premer-ministr': 'премьер-министр',
    'press-pape': 'пресс-папье',
    'pulverizator': 'пульверизатор',
    'pulmonologiya': 'пульмонология',
    'pulpa': 'пульпа',
    'pulpit': 'пульпит',
    'puls': 'пульс',
    'pult': 'пульт',
    'pesa': 'пьеса',
    'rante': 'рантье',
    'revalvatsiya': 'ревальвация',
    'revolver': 'револьвер',
    'rezba': 'резьба',
    'rezbali': 'резьбали',
    'relef': 'рельеф',
    'rels': 'рельс',
    'relsli': 'рельсли',
    'relssiz': 'рельссиз',
    'rubilnik': 'рубильник',
    'saldo': 'сальдо',
    'salto': 'сальто',
    'selderey': 'сельдерей',
    'senor': 'сеньор',
    'senora': 'сеньора',
    'sinka': 'синька',
    'sinkalamoq': 'синькаламоқ',
    'statya': 'статья',
    'stelka': 'стелька',
    'sudya': 'судья',
    'sudyalik': 'судьялик',
    'sulfat': 'сульфат',
    'sulfatlar': 'сульфатлар',
    'subyektiv' : 'субъектив',
    'talk': 'тальк',
    'telefilm': 'телефильм',
    'ultimatum': 'ультиматум',
    'ultra-': 'ультра-',
    'ultrabinafsha': 'ультрабинафша',
    'ultramikroskop': 'ультрамикроскоп',
    'ultratovush': 'ультратовуш',
    'ultraqisqa': 'ультрақисқа',
    'umivalnik': 'умивальник',
    'fakultativ': 'факультатив',
    'fakultet': 'факультет',
    'fakultetlalaro': 'факультетлаларо',
    'falsifikator': 'фальсификатор',
    'falsifikatsiya': 'фальсификация',
    'feldmarshal': 'фельдмаршал',
    'feldsher': 'фельдшер',
    'feleton': 'фельетон',
    'feletonchi': 'фельетончи',
    'fizkultura': 'физкультура',
    'fizkulturachi': 'физкультурачи',
    'film': 'фильм',
    'film-konsert': 'фильм-концерт',
    'filmoskop': 'фильмоскоп',
    'filmoteka': 'фильмотека',
    'filtr': 'фильтр',
    'filtratsiya': 'фильтрация',
    'filtrlamoq': 'фильтрламоқ',
    'filtrli': 'фильтрли',
    'folga': 'фольга',
    'folklor': 'фольклор',
    'folklorist': 'фольклорист',
    'folkloristika': 'фольклористика',
    'folklorchi': 'фольклорчи',
    'folklorshunos': 'фольклоршунос',
    'folklorshunoslik': 'фольклоршунослик',
    'fortepyano': 'фортепьяно',
    'xolodilnik': 'холодильник',
    'selsiy': 'цельсий',
    'shifoner': 'шифоньер',
    'shpilka': 'шпилька',
    'emulsiya': 'эмульсия',
    'eskadrilya': 'эскадрилья',
    'yuriskonsult': 'юрисконсульт',


}

LAST_WORDS = {
    "yeva" : "ева",
    "bsiya":"бция",
    "bsion":"бцион",
    "ksiya":"кция",
    "ksion":"кцион",
    "nsiya":"нция",
    "nsion":"нцион",
    "rsiya":"рция",
    "rsion":"рцион",
    "psiya":"пция",
    "psion":"пцион",
    "tsiya":"ция",
    "tsist":"цист",
    "tsizm":"цизм",
    "tsit":"цит",
    "tsevt":"цевт",
    "tsept":"цепт",
    "tser":"цер",
    "tsia":"циа",
    "sia":"циа",
    "tsikl":"цикл",
    "tsio":"цио",
    "tsiu":"циу",
    "siu":"циу",
}

CYRILLIC_TO_LATIN = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'j',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'x',
    'ц': 's', 
    'ч': 'ch',
    'ш': 'sh',
    'ъ': 'ʼ',
    'ь': '', 
    'э': 'e',
    'ю': 'yu',
    'я': 'ya', 
    'ў': 'o’',
    'қ': 'q',
    'ғ': 'g’',
    'ҳ': 'h', 
}

CYRILLIC_VOWELS = (
    'а', 'е','ё', 'и', 'о', 'у', 'э', 'ю', 'я', 'ў',
)


SOFT_SIGN_WORDS_TRIE = re.compile(r"\b" + trie_from_words(SOFT_SIGN_WORDS), re.U)
TS_WORDS_TRIE = re.compile(r"\b" + trie_from_words(TS_WORDS), re.U)
OTHER_WORDS_TRIE = re.compile(r"\b" + trie_from_words(OTHER_WORDS) + r"\b", re.U)
LAST_WORDS_TRIE = re.compile(trie_from_words(LAST_WORDS) + r"\b", re.U)

def to_cyrillic(text):

    text = re.sub(r"(ʻ|‘|`|ʼ|’|')" , "ㄹ" , text)
    text = re.sub(r"(“|”)" , "ㄱ" , text)

#    ==>  ʻ  = ㅎ  ’   = ㄹ  
    text = re.sub(
            r"\bㄱ",
            "ㅎ",
            text,
            flags = re.U      
        ) 

    
#    ==>  ʻ  = ㅎ  ’   = ㄹ  
    for i in range(len(text)-1):
        if text[i] in """[{(^#.ㅎ""":
            text = text[:i+1] + " " + text[i+1:]
            
    text2 = []
    first = ''
    for i in text:
        if i in [' ' , "\n" , "\t"]:
            if first != '':
                text2.append(first)
                first = ''
            text2.append(i)
        else:
            first += i
    if first != '':
        text2.append(first)

    text = text.lower()
    
    text = re.sub(r"\bmoㄹj" , "мўъж" , text)
    text = re.sub(r"\bmoㄹt" , "мўът" , text)
    
    text = re.sub(r"-da\b", r"da" , text)
    text = re.sub(r"-ku\b" , r"ku" , text)
    text = re.sub(r"-chi\b" , r"chi" , text)
    text = re.sub(r"-yu\b" , r"yu" , text)
    text = re.sub(r"-u\b" , r"u" , text)

    text = SOFT_SIGN_WORDS_TRIE.sub(lambda x: SOFT_SIGN_WORDS[x.group()], text)
    text = TS_WORDS_TRIE.sub(lambda x: TS_WORDS[x.group()], text)
    text = OTHER_WORDS_TRIE.sub(lambda x: OTHER_WORDS[x.group()], text)
    text = LAST_WORDS_TRIE.sub(lambda x: LAST_WORDS[x.group()], text)

#      < ===
    """Transliterate latin text to cyrillic  using the following rules:
    1. ye = е in the beginning of a word or after a vowel
    2. e = э in the beginning of a word or after a vowel
    3. ц exception words
    4. э exception words
    """
    
    # These compounds must be converted before other letters
    compounds_first = {                                                                 
        'ch': 'ч',
        # this line must come before 's' because it has an 'h'
        'sh': 'ш', 
        # This line must come before 'yo' because of it's apostrophe
        "yoㄹ" : "йў" 
        
    }

#    ==>  ʻ  = ㅎ  ’   = ㄹ  
    
    compounds_second = {
        'yo': 'ё',
       #'ts': 'ц', 'Ts': 'Ц', 'TS': 'Ц',  # No need for this, see TS_WORDS
        'yu': 'ю',
        'ya': 'я',
        'ye': 'е',
        # different kinds of apostrophes
        "oㄹ" : "ў" ,  
        "gㄹ" : "ғ"
    }
    
    beginning_rules = {
        'ye': 'е',
        'e': 'э'
    }
    
    after_vowel_rules = {
        'ye': 'е',
        'e': 'э'
    }
    
    exception_words_rules = {
        's': 'ц',
        'ts': 'ц', 
        'e': 'э', 
        'sh': 'сҳ',
        'yo': 'йо',
        'yu': 'йу', 
        'ya': 'йа'
    }

    # compounds
    text = re.sub(
        r'(%s)' % '|'.join(compounds_first.keys()),
        lambda x: compounds_first[x.group(1)],
        text,
        flags=re.U
    )
    text = re.sub(
        r"(%s)" % '|'.join(compounds_second.keys()),
        lambda x: compounds_second[x.group(1)],
        text,
        flags=re.U
    )
    text = re.sub(
        r"\b(%s)" % '|'.join(beginning_rules.keys()),
        lambda x: beginning_rules[x.group(1)],
        text,
        flags=re.U
    )
    text = re.sub(
        r"(%s)(%s)" % ('|'.join(LATIN_VOWELS),
                       '|'.join(after_vowel_rules.keys())),
        lambda x: '%s%s' % (x.group(1), after_vowel_rules[x.group(2)]),
        text,
        flags=re.U
    )
    text = re.sub(
        r"(%s)" % '|'.join(LATIN_TO_CYRILLIC.keys()),
        lambda x: LATIN_TO_CYRILLIC[x.group(1)],
        text,
        flags=re.U
    )
    
    a = ""
    text1 = []
    first = ''
    for i in text:
        if i in [' ' , "\n" , "\t"]:
            if first != '':
                text1.append(first)
                first = ''
            text1.append(i)
        else:
            first += i
    if first != '':
        text1.append(first)

    i = 0
    while i < len(text2):
        if text2[i] == ' ' and i!=0 and (re.match(r"\w+\.$",text2[i-1]) or (text2[i-1] in "[{(^#.ㅎ\"")):
            i+=1
            continue
        if text2[i]  == ' ':
            a += ' '
        elif i+1 < len(text2) and text2[i] + text2[i+1] == '\n':
            a += '\n'
            i+=1
        elif i+1 < len(text2) and text2[i] + text2[i+1] == '\t':
            a += '\t'
            i+=1
        else:
            if text2[i].isupper():
                a+=text1[i].upper()
            elif text2[i].islower():
                a += text1[i]
            else:
                a += text1[i][0].upper()+text1[i][1:]
            if a[-1] == " " and a[-2] in """[{(^#ㅎ""":
                a = a[:-1]
        i += 1

    a = re.sub(
        r"\bㅎ",
        "«",
        a,
        flags = re.U
    )
    a = re.sub(r"[аоу]эв" , "[аоу]ев" , a)
    a = re.sub(r"(\d+)-(йил|ЙИЛ|й|Й)" , r"\1 \2" , a)
    a = re.sub(r"(\d+)-(январ|феврал|март|апрел|май|июн|июл|август|сентябр|октябр|ноябр|декабр|ЯНВАР|ФЕВРАЛ|\
    МАРТ|АПРЕЛ|МАЙ|ИЮН|ИЮЛ|АВГУСТ|СЕНТЯБР|ОКТЯБР|НОЯБР|ДЕКАБР)" , r"\1 \2",a)
    
    
    a = re.sub(r"ㄱ" , "»" , a)
    a = re.sub(r"ㄹ" , "ъ" , a)

    return a



def to_latin(text):
    """Transliterate cyrillic text to latin using the following rules:
    1. ц = s at the beginning of a word.
    ц = ts in the middle of a word after a vowel.
    ц = s in the middle of a word after consonant (DEFAULT in CYRILLIC_TO_LATIN)
        цирк = sirk
        цех = sex
        федерация = federatsiya
        функция = funksiya
    2. е = ye at the beginning of a word or after a vowel.
    е = e in the middle of a word after a consonant (DEFAULT).
    """
    beginning_rules = {
        'ц': 's',
        'е': 'ye',
    }
    after_vowel_rules = {
        'ц': 'ts', 
        'е': 'ye',
    }
    
    text2 = []
    first = ''
    for i in text:
        if i in [' ' , "\n" , "\t"]:
            if first != '':
                text2.append(first)
                first = ''
            text2.append(i)
        else:
            first += i
    if first != '':
        text2.append(first)
    
    text = text.lower()
    
    text = re.sub(
        r'\b(%s)' % '|'.join(beginning_rules.keys()),
        lambda x: beginning_rules[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)(%s)' % ('|'.join(CYRILLIC_VOWELS),
                       '|'.join(after_vowel_rules.keys())),
        lambda x: '%s%s' % (x.group(1), after_vowel_rules[x.group(2)]),
        text,
        flags=re.U
    )
    
    text = re.sub(
        r'(%s)' % '|'.join(CYRILLIC_TO_LATIN.keys()),
        lambda x: CYRILLIC_TO_LATIN[x.group(1)],
        text,
        flags=re.U
    )
    text = re.sub(r"\byanada\b" , "yana-da" , text)
    a = ""
    text1 = []
    first = ''
    for i in text:
        if i in [' ' , "\n" , "\t"]:
            if first != '':
                text1.append(first)
                first = ''
            text1.append(i)
        else:
            first += i
    if first != '':
        text1.append(first)

    i = 0
    while i < len(text2):
        if text2[i]  == ' ':
            a += ' '
        elif i+1 < len(text2) and text2[i] + text2[i+1] == '\n':
            a += '\n'
            i+=1
        elif i+1 < len(text2) and text2[i] + text2[i+1] == '\t':
            a += '\t'
            i+=1
        else:
            if text2[i].isupper():
                a+=text1[i].upper()
            elif text2[i].islower():
                a += text1[i]
            else:
                a += text1[i][0].upper()+text1[i][1:]
        i += 1
    
    
    a = re.sub(r"(\d+) (yil|YIL|y|Y)" , r"\1-\2" , a)
    a = re.sub(r"(\d+) (yanvar|fevral|mart|aprel|may|iyun|iyul|avgust|sentabr|oktabr|noyabr|dekabr|YANVAR|FEVRAL|\
    MART|APREL|MAY|IYUN|IYUL|AVGUST|SENTABR|OKTABR|NOYABR|DEKABR)" , r"\1-\2",a)
    a = a.replace("«" , "“")
    a = a.replace("»" , "”")

    
    return a

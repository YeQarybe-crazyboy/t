import cv2, pytesseract
from requests import post, get
from urllib.parse import urlencode
from random import choice, randint
from json import load, dump
from string import ascii_letters, digits
from threading import Thread

for i in ['one', 'two', 'three', 'four']:
    with open(i+'.json', 'w') as n:
        dump({'count': 0}, n)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class BypassCaptcha:
    def __init__(self, check_count):
        self.count = check_count

    def get_path(self, url):
        return str(url[url.find('captcha=') + 8:url.find('&alias')])[-5::]

    def bypass_captcha(self, captcha):
        url = 'https://eform.tehran.ir/ImageChallenge.captcha.aspx?captcha={}&alias=eform.tehran.ir'.format(captcha)
        with open(f'./imgs/' + self.get_path(url) + '.jpg', 'wb') as f:
            f.write(get(url).content)
        image = cv2.imread('./imgs/' + self.get_path(url) + '.jpg')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(gray, lang='eng').strip().lower()
        return text if (len(text) == 6 and all([i in ascii_letters+digits for i in text])) else self.bypass_captcha(captcha)

    def _get_captcha(self):
        url = "https://eform.tehran.ir:443/API/DnnSharp/ActionForm//settings/initializeForm?_portalId=0&referrer=&openMode=Always&_tabId=84&_alias=eform.tehran.ir&_mid=455&_url=https%3A%2F%2Feform.tehran.ir%2Fsport-Champion%2FIndividual-competition-nologin&language=fa-IR"
        cookies = {".ASPXANONYMOUS": "hzvXmV0sODFFkoUwZaKC5fxpd0tdMhulak7dOSW3hubhI9otCmezG2x3nPeQ-b_4aeyeKh99tHQIOaHwMam-tQpkETH4KpltZ2JGAaiS-vWZbxpO0", "dnn_IsMobile": "False", "language": "fa-IR", "__RequestVerificationToken": "9B43UEWZ7JzTLB7_ZRjzo0X5SoHJM--uiMIefQX32HT9TlcTUf8LbQygzheAe74a1nav5Q2"}
        headers = {"Sec-Ch-Ua": "\"Not;A=Brand\";v=\"24\", \"Chromium\";v=\"128\"", "Requestverificationtoken": "GHEOvP2rOzxISaAJY0eBa06CI7aWqWIZyfVb9u0pmrFdMVuC1hNYRjTdcuxPcg3xYxjudA2", "Accept-Language": "en-US,en;q=0.9", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36", "Accept": "*/*", "X-Requested-With": "XMLHttpRequest", "Dnnsf-Time-Offset": "-210", "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://eform.tehran.ir", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://eform.tehran.ir/sport-Champion/Individual-competition-nologin", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
        req = post(url, headers=headers, cookies=cookies).text
        return req[req.find('/ImageChallenge.captcha.aspx?captcha='):].split('=')[1].split('\\')[0]

    def Create(self):
        captcha = self._get_captcha()
        lst = list()
        x = int()
        y = int()

        for i in range(self.count):
            lst.append(self.bypass_captcha(captcha))

        for index, i in enumerate(lst):
            if lst.count(i) > x:
                x = lst.count(i)
                y = index
        return {'CAPTCHAcaptchaenc': captcha ,'CAPTCHA': lst[y]}

class Enferadi:
    def __init__(self, validation_cookie, validation_header, CaptchaInstance, how_much=1000):
        with open('family.json') as i:
            self.family = load(i)
        with open('name_p.json') as i:
            self.name_p = load(i)
        with open('name_d.json') as i:
            self.name_d = load(i)

        self.instance = CaptchaInstance

        self.__stop = how_much
        self.__start = int()

        self.url = 'https://eform.tehran.ir:443/DesktopModules/DnnSharp/ActionForm/Submit.ashx?_portalId=0&openMode=Always&_tabId=84&_alias=eform.tehran.ir&_mid=455&language=fa-IR&event=click&b=1433&referrer=&_url=https%3A%2F%2Feform.tehran.ir%2Fsport-Champion%2FIndividual-competition-nologin'
        self.headers = {
            "Sec-Ch-Ua": "\"Not;A=Brand\";v=\"24\", \"Chromium\";v=\"128\"", 
            "Requestverificationtoken": validation_header, 
            "Accept-Language": "en-US,en;q=0.9", 
            "Sec-Ch-Ua-Mobile": "?0", 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36", 
            "Content-Type": "application/x-www-form-urlencoded", 
            "Dnnsf-Time-Offset": "-210", 
            "Sec-Ch-Ua-Platform": "\"Windows\"", 
            "Accept": "*/*", 
            "Origin": "https://eform.tehran.ir", 
            "Sec-Fetch-Site": "same-origin", 
            "Sec-Fetch-Mode": "cors", 
            "Sec-Fetch-Dest": "empty", 
            "Referer": "https://eform.tehran.ir/sport-Champion/Individual-competition-nologin", 
            "Accept-Encoding": "gzip, deflate, br", 
            "Priority": "u=1, i"
        }
        self.data = {
            "StaticText": "<div class=\"header\"> <h2> <img src=\"/Portals/0/Images/form-icons/icons-form.png\">قهرمان شهر (مسابقه انفرادی)</h2></div>", 
            # "q1": "مرد",
            "q1": '',  
            # "q2": "/مرد/بدمینتون", 
            "q2": '', 
            # "q3": "/مرد/بدمینتون/زیر 15 سال", 
            "q3": '', 
            # "q4": "محمد",
            "q4": '',  
            # "q5": "احمدی",
            "q5": '', 
            "codemeli": '', 
            # "q12": "1390/04/30",
            "q12": '',  
            # "q7": "09105876451",
            "q7": '',  
            "q8": '', 
            "q9": "/2", 
            # "q10": "/3/3",
            "q10": "",  
            # "q11": "/3/3/اختیاریه - رستم آباد", 
            "q11": "", 
            "q14": "True", 
            "Submit": ''
        }
        self._update_data()
        self.cookie = {'__RequestVerificationToken': validation_cookie}
    
    def _update_data(self):
        self.data.update(self.instance.Create())

    def generate_codemeli(self):
        B = int()
        codes = ['169', '170', '149', '150', '171', '168', '136', '137', '138', '545', '505', '636', '164', '165', '172', '623', '506', '519', '154', '155', '567', '173', '159', '160', '604', '274', '275', '295', '637', '292', '492', '289', '677', '294', '493', '279', '280', '288', '284', '285', '638', '291', '640', '293', '675', '282', '283', '286', '287', '296', '297', '290', '400', '401', '404', '405', '397', '398', '399', '647', '502', '584', '402', '403', '392', '393', '395', '396', '386', '387', '503', '444', '551', '447', '561', '445', '718', '083', '446', '448', '552', '543', '442', '443', '051', '052', '053', '058', '055', '617', '057', '618', '059', '060', '061', '062', '544', '056', '571', '593', '667', '348', '586', '338', '339', '343', '344', '346', '337', '554', '469', '537', '345', '470', '341', '342', '557', '418', '416', '417', '412', '413', '592', '612', '613', '406', '407', '421', '598', '419', '385', '420', '528', '213', '214', '205', '206', '498', '568', '711', '217', '218', '221', '582', '483', '625', '576', '578', '227', '208', '209', '225', '577', '712', '215', '216', '626', '627', '579', '713', '499', '222', '219', '220', '500', '501', '623', '497', '223', '689', '487', '226', '224', '486', '211', '212', '628', '202', '203', '531', '488', '261', '273', '630', '264', '518', '631', '258', '259', '570', '265', '268', '269', '653', '517', '569', '267', '262', '263', '593', '266', '693', '271', '272', '694', '270', '516', '333', '334', '691', '323', '322', '595', '395', '641', '596', '336', '335', '496', '337', '324', '325', '394', '330', '332', '331', '687', '422', '423', '599', '600', '688', '424', '425', '426', '550', '697', '384', '377', '378', '558', '385', '646', '375', '376', '372', '373', '379', '380', '674', '381', '382', '676', '722', '542', '312', '313', '317', '310', '311', '302', '303', '583', '321', '382', '304', '305', '536', '605', '308', '309', '306', '307', '319', '313', '314', '606', '320', '698', '298', '299', '535', '315', '316', '318', '607', '608', '508', '538', '728', '509', '438', '439', '580', '590', '559', '588', '431', '432', '037', '038', '702', '240', '241', '670', '648', '252', '678', '253', '649', '513', '546', '671', '246', '247', '654', '548', '547', '655', '248', '249', '253', '514', '665', '673', '228', '229', '230', '679', '256', '257', '244', '245', '681', '723', '236', '237', '683', '656', '250', '251', '515', '238', '239', '657', '255', '684', '700', '642', '457', '456', '458', '459', '460', '530', '520', '358', '359', '682', '703', '364', '365', '371', '701', '720', '366', '367', '704', '361', '362', '369', '370', '635', '668', '533', '705', '699', '669', '725', '597', '611', '525', '181', '527', '585', '685', '663', '192', '193', '174', '175', '183', '184', '481', '706', '194', '195', '185', '186', '182', '199', '200', '198', '662', '190', '191', '692', '189', '707', '526', '187', '188', '729', '730', '196', '197', '661', '680', '643', '562', '572', '074', '644', '072', '073', '069', '070', '521', '573', '522', '724', '076', '077', '650', '574', '078', '079', '081', '084', '651', '086', '087', '089', '090', '553', '091', '092', '093', '094', '097', '098', '096', '105', '106', '063', '067', '068', '075', '591', '082', '635', '524', '468', '465', '461', '462', '467', '632', '555', '633', '629', '466', '696', '721', '064', '065', '523', '652', '719', '716', '085', '088', '563', '529', '353', '349', '350', '355', '609', '351', '352', '354', '732', '357', '532', '610', '356', '556', '658', '011', '020', '025', '015', '043', '666', '489', '044', '045', '048', '049', '490', '491', '695', '659', '031', '032', '664', '717', '041', '042', '471', '472', '454', '581', '449', '450', '616', '534', '455', '451', '726', '634', '453', '727', '452', '145', '146', '731', '690', '601', '504', '163', '714', '715', '566', '166', '167', '161', '162', '686', '603', '619', '118', '127', '128', '129', '620', '621', '549', '564', '575', '113', '114', '122', '540', '660', '120', '512', '510', '511', '119', '115', '112', '110', '111', '125', '126', '565', '121', '116', '117', '541', '622', '124', '108', '109', '123', '507', '158', '615']
        code_meli = choice(codes)+str(randint(100000,999999))
        for index, value in enumerate(code_meli):
            B += int(value)*range(10,1,-1)[index]
        C = B-(B//11)*11
        A = 11-C
        if A < 9:
            code_meli += str(A)
            return code_meli
        return self.generate_codemeli()
    
    def _get_new_token(self):
        try:
            cookies = get('https://eform.tehran.ir/sport-Champion/Individual-competition-nologin').cookies.get_dict()
            del cookies['__RequestVerificationToken']
            return cookies
        except:
            return self._get_new_token()

    def _gender(self):
        return choice(['زن', 'مرد'])
    def _sport(self, gender):
        man = ['بدمینتون', 'تنیس روی میز', 'کشتی', 'دارت', 'فوتبال روی میز', 'شنا', 'شطرنج']
        woman = ['بدمینتون', 'تنیس روی میز', 'بومی ومحلی', 'دارت', 'آمادگی جسمانی', 'شنا', 'ژیمناستیک']
        if gender == 'مرد':
            return '/مرد/'+choice(man)
        else:
            return '/زن/'+choice(woman)
    def _age_range(self, gender, sport):
        if gender == 'مرد':
            data = {
                'بدمینتون': '/مرد/بدمینتون/16 تا 18 سال',
                'تنیس روی میز': '/مرد/تنیس روی میز/زیر 18 سال', 
                'کشتی': '/مرد/کشتی/14 تا 15 سال (نونهالان)', 
                'دارت': '/مرد/دارت/13 تا 18 سال', 
                'فوتبال روی میز': '/مرد/فوتبال روی میز/17 تا 20 سال',
                'شنا': '/مرد/شنا/18 تا 24 سال',
                'شطرنج': '/مرد/شطرنج/19 سال به بالا'
            }
            return data[sport]
        elif gender == 'زن':
            data = {
                'دارت' : '/زن/دارت/16 تا 25 سال',
                'بومی ومحلی': '/زن/بومی ومحلی/20-17 سال',
                'بدمینتون': '/زن/بدمینتون/23-16 سال',
                'آمادگی جسمانی': '/زن/آمادگی جسمانی/20-16 سال',
                'تنیس روی میز': '/زن/تنیس روی میز/19-15 سال',
                'شنا': '/زن/شنا/24-18 سال',
                'ژیمناستیک': '/زن/ژیمناستیک/10 سال'
            }
            return data[sport]
    def _date(self, gender, sport):
        if gender == 'مرد':
            match sport:
                case 'بدمینتون':
                    return '1386/03/20'
                case 'تنیس روی میز':
                    return '1387/04/10'
                case 'کشتی':
                    return '1389/06/21'
                case 'دارت':
                    return '1386/01/15'
                case 'فوتبال روی میز':
                    return '1384/04/18'
                case 'شنا':
                    return '1383/02/16'
                case 'شطرنج':
                    return '1382/03/19'
        elif gender == 'زن':
            match sport:
                case 'دارت':
                    return '1384/05/12'
                case 'بومی ومحلی':
                    return '1385/03/19'
                case 'بدمینتون':
                    return '1387/01/20'
                case 'آمادگی جسمانی':
                    return '1383/05/11'
                case 'تنیس روی میز':
                    return '1386/03/26'
                case 'شنا':
                    return '1382/04/21'
                case 'ژیمناستیک':
                    return '1393/01/12'

    def _area(self):
        return '/2/'+str(randint(1,9))

    def _mahale(self, area):
        match int(area):
            case 1:
                return choice(['/2/1/دریا', '/2/1/سعادت آباد'])
            case 2:
                return choice(['/2/2/پونک', '/2/2/مرزداران(قبلا مرزداران غربی )'])
            case 3:
                return choice(['/2/3/تهران ویلا', '/2/3/شهرآرا', '/2/3/کوی نصر'])
            case 4:
                return choice(['/2/4/ستارخان ( قبلا برق آلستوم )', '/2/4/شهرک آزمایش ( قبلا مرزداران شرقی )'])
            case 5:
                return choice(['/2/5/شریف(م 2)', '/2/5/صادقیه  (م 2 )', '/2/5/طرشت'])
            case 6:
                return choice(['/2/6/توحید', '/2/6/دریان نو'])
            case 7:
                return choice(['/2/7/ایوانک', '/2/7/شهرک قدس'])
            case 8:
                return choice(['/2/8/آسمانها', '/2/8/سپهر'])
            case 9:
                return choice(['/2/9/فراز (قبلا بهرود )', '/2/9/پرواز', '/2/9/فرحزاد'])

    def Submit(self):
        cookie = self._get_new_token()
        cookie.update(self.cookie)
        data = self.data
        data['codemeli'] = self.generate_codemeli()
        data['q1'] = self._gender()
        data['q2'] = self._sport(data['q1'])
        data['q3'] = self._age_range(*data['q2'].split('/')[1:])
        if data['q1'] == 'زن':
            data['q4'] = choice(self.name_d)
        elif data['q1'] == 'مرد':
            data['q4'] = choice(self.name_p)
        data['q5'] = choice(self.family)
        data['q12'] = self._date(*data['q2'].split('/')[1:])
        data['q7'] = '0913'+str(randint(1000000, 9999999))
        data['q10'] = self._area()
        data['q11'] = self._mahale(data['q10'].split('/')[2])

        result = post(self.url, headers=self.headers, data=urlencode(data), cookies=cookie)
        if 'کد امنیتی' in result.text:
            self._update_data()
            return self.Submit()
        print(result.text)
        print(data)
        print('-'*20)
        return result

    def __iter__(self):
        return self

    def __next__(self):
        if self.__start < self.__stop:
            self.__start += 1
            return self.Submit()
        raise StopIteration


def start(stop, task):
    x = Enferadi('Up2tXUxyC7td6y3myHS6drE9bFVp-irjNX5CQFwt-aC8gsvvSKnQQR5_q20gnO05ufOKNg2', 'V-GJffSOd0we_RncwueBgTYIeNXClBo5N6T2mqe7WTgWkItxDfifXDbwAZlft9NfgJ3WvA2', BypassCaptcha(20), stop)
    for i in x:
        if 'ثبت نام شما با موفقیت انجام شد' in i.text:
            with open(task+'.json') as f:
                count = load(f)
            count['count'] += 1
            with open(task+'.json', 'w') as f:
                dump(count, f) 

one = Thread(target=start, args=(450,'one',))
two = Thread(target=start, args=(450,'two',))
three = Thread(target=start, args=(450,'three',))
four = Thread(target=start, args=(450,'four',))

one.start()
two.start()
three.start()
four.start()
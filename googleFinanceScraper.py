import requests, bs4, time, re, array, sqlite3, marshal
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


##Google Finance real time data

browser = webdriver.Firefox()
browser.get("https://www.google.com/finance")

##Locate the search box
searchBox = browser.find_element_by_class_name("fjfe-searchbox-input")

companyTickers = ["AMEAS", "CGCBV", "NOKIA", "CTY1S", "ELISA", "FIS1V", "FUM1V",
                  "HUH1V", "KCR1V", "KESAV", "KESBV", "KNEBV", "KEMIRA", "MEO1V",
                  "METSA", "METSB", "NDA1V", "NESTE", "NRE1V", "ORNAV", "ORNBV",
                  "OUT1V", "SAMAS", "SDA1V", "SSABAH", "SSABBH", "STEAV", "STERV",
                  "TELIA1", "TIE1V", "UPM1V", "VALMT", "WRT1V", "AHL1V", "AKTAV",
                  "AKTRV", "ALBAV", "ALN1V", "ASU1V", "ATG1V", "ATRAV", "BAS1V",
                  "BITTI", "CAV1V", "CRA1V", "FIA1S", "FLG1S", "FSC1V", "HKSAV",
                  "LAT1V", "LEHTO", "LEM1S", "MUNK1", "OKDAV", "OKDBV", "OLVAS",
                  "OTE1V", "PIHLIS", "PKC1V", "PON1V", "POY1V", "RAIVV", "RAP1V",
                  "REG1V", "RMR1V", "SAA1V", "SRV1V", "STCAS", "STCBV", "SUY1V",
                  "TAALA", "TIK1V", "TOKMAN", "TPS1V", "UNR1V", "VAIAS", "VIK1V",
                  "YTY1V", "ACG1V", "AFAGR", "AFE1V", "APETI", "BIOBV", "BTH1V",
                  "CONSTI", "CPMBV", "CTH1V", "CTL1V", "DIG1V", "DOV1V", "EFO1V",
                  "ELEAV", "ENDOM", "EQV1V", "ETT1V", "EVLI", "EXL1V", "GLA1V",
                  "HONBS", "ICP1V", "IFA1V", "ILK2S", "INVEST", "KELAS", "KSLAV",
                  "MARAS", "MMO1V", "NEO1V", "NLG1V", "NORVE", "OKM1V", "OREIT",
                  "PIZZA", "PKK1V", "PNA1V", "QPR1V", "QTCOM", "RESTA", "RUTAV",
                  "SAGCV", "SCI1V", "SCL1V", "SIILI", "SOPRA", "SOSI1", "SSH1V",
                  "STQ1V", "TAM1V", "TEM1V", "TLT1V", "TLV1V", "TRH1V", "TULAV",
                  "UUTEC", "VALOE", "WUF1V", "XNS1V", "YLEPS"]

class Company:
    
    def __init__(self, name, ticker, price, dayLow, dayHigh, volume):

        self.name = name
        self.ticker
        self.price

        self.dayLow
        self.dayHigh
        self.volume

db = sqlite3.connect("E:/Käyttäjät/Tiedostot/Python/porssiDataAPI/porssidata.db")

for i in range(len(companyTickers)):

    searchBox = browser.find_element_by_class_name("fjfe-searchbox-input")

    searchBox.clear()

    
    search = "HEL:" + companyTickers[i]
    searchBox.send_keys(search)
    searchBox.send_keys(Keys.ENTER)


    ##When the market is open
    
    elems = browser.find_elements_by_class_name("pr")
    price = 0
    
    if (len(elems) > 0):
        price = elems[0].text

    prices = []

    price = float(price)
    prices.append(price)

    
    companyName = browser.find_element_by_class_name("appbar-snippet-primary").text
    
    print(companyName + ": ")
    print(price)

    dayLowAndHigh = 0
    try:

        dayLowAndHigh = browser.find_element_by_css_selector(".snap-data tr td:nth-child(2)").text
    except NoSuchElementException:
        
        print("Price range not found!")

    dayLow = 0
    dayHigh = 0
    
    if (len(dayLowAndHigh) > 6):
        
        dayLow = re.search("\d+\D\d+", dayLowAndHigh).group()

        dayHigh = dayLowAndHigh[len(dayLow) + 3:]

    
    print(dayLowAndHigh, dayLow, dayHigh)

    volume = 0
    try:
        
        volElement = browser.find_element_by_css_selector(".snap-data tr:nth-child(4) td:nth-child(2)")

        volumeUnparsed = volElement.text

        if (len(volumeUnparsed) > 13):

            volume = re.search("\d+\D\d+\D\d+", volumeUnparsed).group()
        else:

            volume = re.search("\d+\D\d+\w", volumeUnparsed).group()

        if volume.find('/') != -1:

            index = volume.index('/')
            volume = volume[:index]
            
    except NoSuchElementException:
        print("No volume found!")

    print(volume)
    

    cursor = db.cursor()

    cursor.execute('''SELECT prices FROM companies WHERE ticker=?''', (companyTickers[i],))

    pricesString = cursor.fetchone()

    priceArr = marshal.loads(pricesString[0])

    priceArr.append(price)

    cursor = db.cursor()

    priceArr = marshal.dumps(priceArr)
    cursor.execute('''UPDATE companies SET prices = ? WHERE ticker = ?''', (priceArr, companyTickers[i]))
    
    db.commit()
    
browser.close()

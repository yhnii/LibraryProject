from bs4 import BeautifulSoup
import requests
import time
import json
import pymongo
import re
import pandas as pd
def main():
    session = requests.session()

# 한글 철자 모음 리스트
    with open("korean.txt","r",encoding="utf-8") as f:
        char = f.read()
        list_kor = []
        for i in char:
            list_kor.append(i)

    list_kor = list_kor[1:len(list_kor)]

    #영어 철자 모음 리스트
    list_eng_s = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

    list_eng_l = []
    for c in list_eng_s:
        list_eng_l.append(c.upper())

    #숫자 모음 리스트
    list_dig = ["0","1","2","3","4","5","6","7","8","9"]
    #--------------------------------------------------------------------------------------------------------------------
    lists = list_kor + list_eng_s + list_eng_l + list_dig

    API_KEY = 'CA4B20C10CE7B07B8A0376F898EA32F24C0B956EFB0E5E7422A6886902CD8A21'
    mainurl = 'http://book.interpark.com/api/search.api?key='
    #besturl = 'http://book.interpark.com/api/bestSeller.api?key='
    #recmurl = 'http://book.interpark.com/api/recommend.api?key='
    #newburl = 'http://book.interpark.com/api/newBook.api?key='


    
    #list 형식으로 카테고리 가져오기
    category = pd.read_csv('category.csv', header=None)
    category = category[0].tolist()

    urls = scrape_list_page(lists, category, mainurl, API_KEY) #123574개

    library_book_list = []
    for url in urls:
        time.sleep(1)
        response = session.get(url)
        bookInfo = scrape_detail_page(response)
        #print(bookInfo)
        library_book_list.append(bookInfo)
        break

    library_book_list_new = list_clear(library_book_list)

    categorized_book_list = categorization(library_book_list_new)
    #print(categorized_book_list[1])
   
    with open("publicLibrary.json", "w", encoding="utf-8-sig") as f:
        json.dump(categorized_book_list, fp=f, ensure_ascii=False, indent=3)

    insertMongDB(categorized_book_list)

    

def scrape_list_page(lists, category, mainurl, API_KEY):
    for x in lists:
        for y in category:
            url = "{}{}&query={}&categoryId={}&maxResults=100&soldOut=n".format(mainurl, API_KEY, x, y)
            
            print(url)
            yield url

def scrape_detail_page(response):
    try:
        soup = BeautifulSoup(response.text,'html.parser') 
        bookInfo = []
        count = 1
        for i in range(len(soup.select("item"))):
            title = soup.select("item title")[i].string
            desc = soup.select("item description")[i].string
            date = soup.select("item pubdate")[i].string
            categoryname = soup.select("item categoryname")[i].string
            author =soup.select("item author")[i].string
            publisher = soup.select("item publisher")[i].string
            isbn = soup.select("item isbn")[i].string
            translator = soup.select("item translator")[i].string
            id = soup.select("item itemid")[i].string
            count+=1
        
            dict = {
                'title' : title,
                'desc' : desc,
                'date' : date,
                'categoryname' : categoryname,
                'author' : author,
                'publisher' : publisher,
                'isbn' : isbn,
                'translator' : translator,
                'id' : id,
                'count' : count
             }
            bookInfo.append(dict)
        return bookInfo
    except Exception as e:
        print("페이지 파싱 에러", e)


def list_clear(list):
    id_list = []
    lists= []
    for x in (list):
        for y in x:
            if y['id'] and y['id'] not in id_list:
                id_list.append(y['id'])
                lists.append(y)
            else:
                pass
    return lists

def categorization(list):
    novel = [] #소설
    poem = [] #시/에세이
    art = [] #예술/대중문화
    social = [] #사회과학
    culture = [] #역사문화
    comic = [] # 만화
    baby = [] #유아
    life = []#가정과 생활
    language = []#국어/외국어/사전
    science = [] #자연과 과학
    economy = [] #경제경영
    improve = [] #자기계발
    human = [] #인문
    region = []#종교/역학
    computer = []#컴퓨터/인터넷
    license = [] #자격서/수험서
    hobby = []#취미/레저
    major = []#전공도서/대학교재
    health = []#건강/뷰티
    travel = [] #여행
    tresh = []

    for n in list:
    #print(n)
        if n['categoryname'] == '국내도서>소설':
            novel.append(n)
        elif n['categoryname'] == '국내도서>시/에세이':
            poem.append(n)
        elif n['categoryname'] =='국내도서>예술/대중문화':
            art.append(n)
        elif n['categoryname'] =='국내도서>사회과학':
            social.append(n)
        elif n['categoryname'] =='국내도서>역사와 문화':
            culture.append(n)
        elif n['categoryname'] =='국내도서>만화':
            comic.append(n)
        elif n['categoryname'] =='국내도서>유아':
            baby.append(n)
        elif n['categoryname'] =='국내도서>가정과 생활':
            life.append(n)

        elif n['categoryname'] =='국내도서>국어/외국어/사전':
            language.append(n)

        elif n['categoryname'] =='국내도서>자연과 과학':
            science.append(n)

        elif n['categoryname'] =='국내도서>경제경영':
            economy.append(n)

        elif n['categoryname'] =='국내도서>자기계발':
            improve.append(n)

        elif n['categoryname'] =='국내도서>인문':
            human.append(n)

        elif n['categoryname'] =='국내도서>종교/역학':
            region.append(n)

        elif n['categoryname'] =='국내도서>컴퓨터/인터넷':
            computer.append(n)

        elif n['categoryname'] =='국내도서>자격서/수험서':
            license.append(n)

        elif n['categoryname'] =='국내도서>취미/레저':
            hobby.append(n)

        elif n['categoryname'] =='국내도서>전공도서/대학교재':
            major.append(n)

        elif n['categoryname'] =='국내도서>건강/뷰티':
            health.append(n)

        elif n['categoryname'] =='국내도서>여행':
            travel.append(n)
        else:
            tresh.append(n)


    totlal_list =  [novel,poem,art,social,culture,comic,baby,life,language,science,economy,improve,human,region,computer,license,hobby,major,health,travel,tresh]    
    return totlal_list

def insertMongDB(list):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    #database 생성
    mydb = myclient['libraryBooks']  #libraryBooks
    #print(myclient.list_database_names())

    '''
    #데이터베이스 존재 여부 확인
    dblist = myclient.list_database_names()
    
    if 'libraryBooks' in dblist:
        print("The database exists.")
    else:
        print("The database does not exist")
    '''
    #collection 생성
    kdc_list = ['novel',
                'poem',
                'art',
                'social',
                'culture',
                'comic',
                'baby',
                'life',
                'language',
                'science',
                'economy',
                'improve',
                'human',
                'region',
                'computer',
                'license',
                'hobby',
                'major',
                'health',
                'travel',
                'tresh']

    i = 0
    for a in kdc_list:
        a = mydb[a] 
        a.insert_many(list[i])
        i += 1      
        #print("********************************", a ,"************************************")
        for b in a.find():
            print(b)
        
if __name__ == "__main__":
    main()
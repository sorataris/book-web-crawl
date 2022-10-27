
import csv

import urllib.request
import bs4


'''




책 이름:goods_name
저자:goods_auth
출판사:goods_pub
발행일:goods_date
가격: goods_price/yes_b

1. csv,bs4,request import
2. html,bs4객체 생성
3. 태그를 찾음
4. while문을 돌려 계속 찾기
5. for문을 사용하여 한페이지 내에 여러개 책 내용을 찾음.
6. 함수호출(태그)


'''


def getdata(tag): #태그 찾기 함수
    book = tag.find("div",{'class':"goods_name"}) #제목 태그
    bookname = book.find("a").text #a태그에서의 텍스트 값
    authtotal = tag.find("div",{"class":"goods_pubGrp"}) #저자 태그
    
    auth = authtotal.find("span",{"class":"goods_auth"}) #저자
   
    if (auth.find("a")==None): #만약 하이퍼 링크가 걸려있지 않으면
          authreal = authtotal.find("span",{"class":"goods_auth"}).text #저자
       
    else: #걸려있으면
        authreal = auth.find("a").text

    
    if(authtotal.find("span",{"class":"goods_pub"}))==None: #만약 출판사가 없다면
        com="없음"
    else:
        com = authtotal.find("span",{"class":"goods_pub"}).text #출판사

    date = authtotal.find("span",{"class":"goods_date"}).text #발행일
    goodsprice =tag.find("div",{"class":"goods_price"}) #가격 태그
    price = goodsprice.find("em",{"class":"yes_b"}).text #가격
    return [bookname,authreal,com,date,price]

url = "http://www.yes24.com/24/Category/Display/001001047010?ParamSortTp=05&PageNumber="
csvname = "./book.csv"

with open(csvname,"w",newline="")as csvfp:
            csvWriter= csv.writer(csvfp)
            csvWriter.writerow(["도서명","저자","출판사","발행일자","가격"])
k=1
while(True):
    realurl = url+str(k) #url+숫자가 웹 페이지의 순서
    print(realurl) 
    htmlobject = urllib.request.urlopen(realurl) #html객체 생성
    webpage = htmlobject.read() #html문서 읽어옴
    bsobject = bs4.BeautifulSoup(webpage,"html.parser") #bsobjec 생성
    tag = bsobject.find("ul",{"class":"clearfix"}) #큰 틀 찾기
    all_book=tag.findAll('div',{'class':'goods_info'}) #책 내용 모두 찾기
    #print(tag)
    if tag=="": #만약 데이터가 없으면
        break
    for i in all_book:
        list=[]
        result = getdata(i) #배열로 값을 받음

        #특수문자가 제목에 있을경우 db에 저장되지 않은 문제가 발생함
        for i in result:
            s = i.replace(',','')
            s = s.replace(':','')
            s = s.replace('"','')
            s = s.replace('\n','')
            s = s.replace('\r','')
            s = s.replace('                    ','')
            list.append(s) #리스트에 결과를 붙혀넣음



        print(list) #한줄을 읽어왔다.
        with open(csvname,"a",newline="")as csvfp: #파일 내용추가
            csvWriter= csv.writer(csvfp) #라이터 선언
            csvWriter.writerow(list) #내용쓰기
    

    k=k+1 #페이지 증가







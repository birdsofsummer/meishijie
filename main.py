"""
美食杰
https://www.meishij.net/
"""

import requests
from bs4 import BeautifulSoup
import re
import pymongo
import time
import json
import pymongo
from bson.json_util import dumps,loads,RELAXED_JSON_OPTIONS


def conn(u="mongodb://localhost:27017/"):
    myclient = pymongo.MongoClient(u)
    #dblist = myclient.list_database_names()
    mydb = myclient["meishijie"]
    #collist = mydb. list_collection_names()
    mycol = mydb["caipu"]
    return mycol

mycol=conn()
#mycol.delete_many({})

h={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en;q=0.3,en-US;q=0.2",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "referrer": "https://www.meishij.net/shicai/",
}


def get(u=""):
    base='https://www.meishij.net'
    if re.match('^http',u) :
        u0=u
    else:
        u0=base+u
    u1=requests.utils.requote_uri(u0)
    h.update({"referrer":u1})
    r=requests.get(u1,headers=h)
    return r.text

def sub_last(u="",n=1) :
    #re.sub('\d+',str(n),u,1)
    a=re.findall('\d+',u)[-1]
    return u.replace(a,str(n))


"""
u='https://www.meishij.net/shicaizuofa/humayou/p2/'
u='https://www.meishij.net/weishengsu/weishengsub1/?page=4'
sub(u,299)

"""
def sub(u="",n=1):
    u1=u.split('/')[::-1]
    z=[]
    found=False
    for x in u1:
        if re.match('.*\d+',x) != None  and not(found):
            x1=re.sub('\d+',str(n),x,1)
            z.append(x1)
            found=True
        else:
            z.append(x)
    z1="/".join(z[::-1])
    return z1


def find_page(u=""):
    try:
        z=u.split('/')[::-1]
        r=filter(lambda x:re.match(".*\d+",x),z)
        l=list(r)
        n=re.findall('\d+',l[0])
        s=int(n[0])
        return s
    except:
        print("???")
        return 0



'''
# 1级类

{
 '家常菜谱': 'https://www.meishij.net/chufang/diy/',
 '中华菜系': 'https://www.meishij.net/china-food/caixi/',
 '各地小吃': 'https://www.meishij.net/china-food/xiaochi/',
 '外国菜谱': 'https://www.meishij.net/chufang/diy/guowaicaipu1/',
 '烘焙': 'https://www.meishij.net/hongpei/',
 '厨房百科': 'https://www.meishij.net/pengren/',
 '食材百科': 'https://www.meishij.net/shicai/',
}
'''

def get_cat1():
    base='https://www.meishij.net'
    u="https://www.meishij.net/chufang/diy/guowaicaipu1/"
    r=get(u)
    soup = BeautifulSoup(r, 'html.parser')
    links = [(x.text,x.attrs['href']) for x in soup.find(class_="listnav_ul").findAll('a') if 'href' in x.attrs]
    return [(x, base+y if re.match('^/.*',y)  else y) for x,y in links]

"""
2级类

外国菜谱
https://www.meishij.net/chufang/diy/guowaicaipu1/
[
   (
      "国家",
      [
         [ "韩国料理", "https://www.meishij.net/chufang/diy/guowaicaipu1/hanguo/" ],
         [ "日本料理", "https://www.meishij.net/chufang/diy/guowaicaipu1/japan/" ],
         [ "西餐面点", "https://www.meishij.net/chufang/diy/guowaicaipu1/ccmd/" ],
         [ "法国菜", "https://www.meishij.net/chufang/diy/guowaicaipu1/faguo/" ],
         [ "意大利餐", "https://www.meishij.net/chufang/diy/guowaicaipu1/yidali/" ],
         [ "美国家常菜", "https://www.meishij.net/chufang/diy/guowaicaipu1/usa/" ],
         [ "东南亚菜", "https://www.meishij.net/chufang/diy/guowaicaipu1/dongnanya/" ],
         [ "墨西哥菜", "https://www.meishij.net/chufang/diy/guowaicaipu1/moxige/" ],
         [ "澳大利亚菜", "https://www.meishij.net/chufang/diy/guowaicaipu1/aozhou/" ],
         [ "其他国家", "https://www.meishij.net/chufang/diy/guowaicaipu1/other/" ]
      ]
   ),
   (
      "上菜顺序",
      [
         [ "餐前小吃", "https://www.meishij.net/chufang/diy/guowaicaipu1/canqianxiaochi/" ],
         [ "汤品", "https://www.meishij.net/chufang/diy/guowaicaipu1/tangpin/" ],
         [ "主菜", "https://www.meishij.net/chufang/diy/guowaicaipu1/zhucai/" ],
         [ "主食", "https://www.meishij.net/chufang/diy/guowaicaipu1/zhushi/" ],
         [ "饮品", "https://www.meishij.net/chufang/diy/guowaicaipu1/yinpin/" ],
         [ "甜点", "https://www.meishij.net/chufang/diy/guowaicaipu1/tiandian/" ]
      ]
   )
]
"""
def get_cat2(u):
    #u="https://www.meishij.net/chufang/diy/{}/".format(cat)
    r=get(u)
    soup = BeautifulSoup(r, 'html.parser')
    dls=soup.find(class_='listnav_con').findAll('dl')
    z=[]
    for dl in dls:
       title= dl.find('dt').text
       content=[(x.text,x.attrs['href']) for x in dl.findAll('a')]
       o=(title,content)
       z.append(o)
    return z


def parse_li(li):
    img=li.find('img').attrs['src'] if li.find('img') else ""
    author=li.find('em').text if li.find('em') else ""
    z=list(map(int,re.findall("(\d+)",li.find(class_="c1").find('span').text))) if li.find(class_="c1") and li.find(class_="c1").find('span') else [0,0]
    comment=z[0] if len(z)>0 else 0
    like=z[1] if len(z)>1 else 0
    url=li.find('a').attrs['href'] if li.find('a') else ""
    name=li.find('a').attrs['title'] if li.find('a') else ""
    #name=li.find(class_="c1").find('strong').text
    step=li.find(class_="li1").text if li.find(class_="li1") else ""
    gongyi=li.find(class_="li2").text if li.find(class_="li2") else ""
    tag=li.find(class_="gx").text if li.find(class_="gx")  else ""
    o={
        "name":name,
        "img":img,
        "author":author,
        "url":url,
        "step":step,
        "gongyi":gongyi,
        "comment":comment,
        "like":like,
      }
    return o


'''
https://www.meishij.net/chufang/diy/guowaicaipu1/yinpin/
{
 'name': '牛奶布丁',
 'img': 'http://s1.ig.meishij.net/p/20120907/3a67053e09badf8d91fb4a79e8727765.jpg',
 'author': 'Baron49',
 'url': 'http://www.meishij.net/zuofa/niunaibuding_2.html',
 'step': '9步',
 'gongyi': '其它工艺 / 其它口味',
 'comment': 26,
 'like': 28826
 }

'''
def parse_cat3(r=""):
    soup = BeautifulSoup(r, 'html.parser')
    tt=soup.find(class_="gopage").find('form').text if soup.find(class_="gopage") else ""
    total=int(re.findall('共(\d+).*',tt)[0]) if tt!="" else 0
    z=[]
    lis=soup.findAll(class_="listtyle1")
    for li in lis:
        o=parse_li(li)
        z.append(o)
    return total,z

def find_next(r=""):
    soup = BeautifulSoup(r, 'html.parser')
    return soup.find(class_="next").attrs['href'] if soup.find(class_="next") else ""






"""
https://www.meishij.net/shicaizuofa/humayou/
https://www.meishij.net/shicaizuofa/humayou/p2/
https://www.meishij.net/shicaizuofa/humayou/p49/

https://www.meishij.net/weishengsu/weishengsub1/
https://www.meishij.net/weishengsu/weishengsub1/?page=4

https://www.meishij.net/weishengsu/weishengsub2/
https://www.meishij.net/weishengsu/weishengsub6/
https://www.meishij.net/weishengsu/weishengsub12/


https://www.meishij.net/shicaizuofa/humayou/p49/
https://www.meishij.net/shicaizuofa/humayou/p{}/

'https://www.meishij.net/weishengsu/weishengsub1/?page=4'
'https://www.meishij.net/weishengsu/weishengsub1/?page={}'

"""

def get_max1(u="https://www.meishij.net/shicaizuofa/humayou/",n=1):
    #print("--->",u,n)
    r=get(u)
    soup = BeautifulSoup(r, 'html.parser')
    if soup.find(class_="listtyle1_page_w") != None:
       # [
       #  'https://www.meishij.net/shicaizuofa/humayou/',
       #  'https://www.meishij.net/shicaizuofa/humayou/p2/',
       #  'https://www.meishij.net/shicaizuofa/humayou/p3/',
       #  'https://www.meishij.net/shicaizuofa/humayou/p4/',
       #  'https://www.meishij.net/shicaizuofa/humayou/p5/',
       #  'https://www.meishij.net/shicaizuofa/humayou/p2/'
       # ]
       # ['?page=3', '?page=2', '?page=3', '', '?page=5', '?page=6', '?page=5']
        a=[x.attrs['href'] for x in soup.find(class_="listtyle1_page_w").findAll('a')]
        step=len(a)-1
        #uu=re.sub('\d+','{}',a[1])
        if soup.find(class_="next") == None:
            page=int(re.findall('\d+',a[-1])[0])
            print('find',page)
            return page
        else:
            uu=soup.find(class_="next").findPreviousSibling('a').attrs['href']
            #n=int(soup.find(class_="next").findPreviousSibling('a').text)
            n1=n+step
            #u1=re.sub('\d+',str(n1),uu)
            u1=sub(uu,n1)
            if re.match("^http.*",u1):
                print(u1)
            else:
                base=u.split('?')[0]
                u1=base+u1
            print("too small,try +5",n1,u1)
            return get_max1(u1,n1)
    elif n==1:
        raise "????"
    else:
        n1=n-1
        u1=sub(u,n1)
        print(n,"too big try -1",n1,u1)
        return get_max1(u1,n1)

"""
两种分页规则

https://www.meishij.net/shicaizuofa/humayou/
https://www.meishij.net/shicaizuofa/humayou/p12

https://www.meishij.net/chufang/diy/sushi/
https://www.meishij.net/chufang/diy/sushi/?&page=2

食材百科
https://www.meishij.net/shicai/
https://www.meishij.net/shicai/jianguozhongzi_list?page=5

https://www.meishij.net/抹茶粉?page=50
"""
def get_cat3(u0="https://www.meishij.net/shicaizuofa/humayou/",page=1):
    u1="{}?&page={}"
    u=u1.format(u0,page) if not(re.match(".*\?.*",u0)) else u0
    r=get(u)
    total,d=parse_cat3(r)
    print("total :",total)
    if total == 0 :
       #total=get_max1(u0)
       total=2        ####################################################################
       print("real total :",total)
       next_=find_next(r)
       for x in range(1,total):
            u=sub(next_,x) if re.match('^http.*',next_) else u0.split('?')[0]+next_
            print("start {}/{} {}".format(x,total,uu))
            try:
                uu=sub(u,x)
                total,d=parse_cat3(get(uu))
                print("end {}/{} {}".format(x,total,uu))
                #x1 = mycol.insert_many(d)
                #print(x1.inserted_ids)
                yield d
            except:
                print("eee",u0,x)
            #time.sleep(1)
    else:
        for x in range(1,total):
            try:
                print("start {}/{}".format(x,total))
                u=u1.format(u0,x)
                total,d=parse_cat3(get(u))
                print("end {}/{}".format(x,total))
                #x1 = mycol.insert_many(d)
                #print(x1.inserted_ids)
                yield d
            except:
                print("eee",u0,x)
            #time.sleep(1)




"""
https://www.meishij.net/抹茶粉?page=1
{
 'name': '抹茶水果凉粉',
 'img': 'https://s1.ig.meishij.net/p/20130812/c7c04bf91b8a8d6ee0ff69e3c5dd0e64_150x150.jpg',
 'author': '潘@玲子',
 'url': 'https://www.meishij.net/zuofa/mochashuiguoliangfen.html',
 'step': '7步 / 大概数小时',
 'gongyi': '煮 / 甜味',
 'comment': 13,
 'like': 14213
}
"""
def parse_shicaibaike(r=""):
    soup = BeautifulSoup(r, 'html.parser')
    desc=soup.find(class_="sccon_right_con").find('p').text
    lis=soup.findAll(class_="listtyle1")
    d=[parse_li(x) for x in  lis]
    return desc,d

def get_shicaibaike_max(cat="抹茶粉",n=1000_0):
    u0="https://www.meishij.net/{}?page={}"
    u=u0.format(cat,n)
    r=get(u)
    soup = BeautifulSoup(r, 'html.parser')
    next=soup.find(class_="next")
    if next == None:
        t=soup.find(class_="listtyle1_page_w").findAll('a')[-1].text
        m=int(t if t!="下一页" else str(n))
        return m
    else:
        return get_shicaibaike(cat,n+1000)

def get_shicaibaike1(cat="抹茶粉",n=5):
    u0="https://www.meishij.net/{}?page={}"
    n1=get_shicaibaike_max(cat,1000)
    print('{} : {}'.format(cat,n1))
    to=min(n,n1)
    for i in range(1,to):
        print('start {} {}/{}'.format(cat,i,n1))
        u=u0.format(cat,i)
        r=get(u)
        desc,d=parse_shicaibaike(r)
        print('end {} {}/{}'.format(cat,i,n1))
        yield desc,d
        #time.sleep(1)

def main():
    list1=get_cat1()
    for n1,u1 in list1:
        print("start",n1,u1)
        c1=get_cat2(u1)
        for name,urls in c1:
            for n2,u2 in urls:
                print("start",n1,name,n2,u2)
                for x in get_cat3(u2):
                    print("start",n1,name,n2,u2,x)
                #    ids=[mycol.insert_many(x1) for x1 in x]
                #    for ii in ids:
                #        print(ii.inserted_ids)


main()

import requests
import re
import pymongo
import matplotlib.pyplot as plt


def getHTMLText(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # 抛出异常
        response.encoding = response.apparent_encoding  # 'utf-8'
        print("getHTMLText")
        return response.text
    except:
        print("Error-getHTMLText")
        return ""


def fillUnivList(html, ulist, price1):
    try:
        names = re.findall(r'\<span class=\"title\" title=\".*?\"\>', html)
        prices = re.findall(r'\<strong\>[\d\.]*<\/strong\>', html)
        print("页面解析完成")
        for i in range(len(names)):
            name = names[i].split('"')[3]  # <span class="title" title="ins大容量双肩包男韩版大学生书包女初中">
            price = re.split(">|<", prices[i])[2]  # <strong> 59.90 </strong>
            ulist.append([name, price])
            price1.append(price)
        print("列表生成完成")
    except:
        print("Error-fillUnivList")
        return ""


def printUnivList(ulist, path):
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write("商品\t价格\n")
            for i in range(len(ulist)):
                u = ulist[i]
                f.write(u[0] + "\t")
                f.write(u[1] + "\n")
            f.close()
            print("文件存储完成")
    except:
        print("Error-printUnivList")
        return ""


def printUnivList_mongodb(ulist):
    try:
        # 建立连接
        client = pymongo.MongoClient('192.168.52.111', 27017)
        # 连接数据库
        db = client['mydb_4']
        # 连接表
        collection = db['taobao_data']
        for i in range(len(ulist)):
            u = ulist[i]
            # 插入数据
            collection.insert_one({'名称': u[0], '价格': u[1]})
        print("文件存储完成_mongodb")
    except:
        print("Error-printUnivList_mongodb")
        return ""


def getData(price1, x, y):
    kd = 1000  # 价格跨度
    zd = 10000  # 价格最大值
    sum = 0
    for j in range(0, 10):
        count = 0
        min = kd * j
        max = kd * (j + 1)
        x.append(f'{min}~{max}')
        for i in price1:
            f = float(i)
            if f > min and f <= max:
                count += 1
        y.append(count)
    for i in price1:
        f = float(i)
        if f > zd:
            sum += 1
    x.append(f'{zd}以上')
    y.append(sum)


def Drawing(x, y):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决plt中文显示的问题
    plt.rcParams['axes.unicode_minus'] = False  # 解决plt负号显示的问题
    plt.subplot(1, 2, 1)  # 不同图在同一画布中的位置
    plt.title("价格分布图")
    plt.xlabel("价格")
    plt.ylabel("数量")
    plt.bar(x, y)  # 柱状图
    plt.subplot(1, 2, 2)  # 不同图在同一画布中的位置
    plt.title("价格比例图")
    explode = (0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01)
    plt.pie(y, explode, x, autopct='%.2f%%')  # 饼状图
    plt.show()


def main():
    x = []
    y = []
    ulist = []
    price1 = []
    name = input("请输入名称：")
    page = int(input("请输入页数："))
    path = "D:/" + name + ".txt"
    for i in range(page):
        url = "https://re.taobao.com/search_ou?keyword=" + name + "&page=" + str(page)
        html = getHTMLText(url)
        fillUnivList(html, ulist, price1)
    printUnivList(ulist, path)
    printUnivList_mongodb(ulist)
    getData(price1, x, y)
    Drawing(x, y)


if __name__ == '__main__':
    main()

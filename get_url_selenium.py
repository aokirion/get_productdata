from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import time
import get_unique_list
from selenium import webdriver
import sys

# 引数を引き取る
args = sys.argv

# カテゴリリストを辞書型で保持
category_list = {
    1:"米・パン",
    2:"肉、ハム類",
    3:"魚介類",
    4:"麺類",
    5:"雑貨・日用品",
    6:"野菜類",
    7:"果物類",
    8:"酒・アルコール",
    9:"お茶・飲料",
    10:"調味料・油",
    11:"お菓子・スイーツ",
    12:"旅行・チケット",
    13:"セット類・その他",
    15:"卵",
    16:"加工食品",
    17:"電化製品",
    18:"工芸品",
    19:"感謝状・記念品"
}

if len(args) == 2:
    if args[1].isdigit():
        if int(args[1]) in category_list.keys():
            categoryid = args[1]
        else:
            print("該当カテゴリは存在しません。\n引数を見直してください。")
            sys.exit()
    else:
        print("引数は数値を入力してください。")
        # 処理を終了する
        sys.exit()
else:
    # 2023/6/1現在
    print("下記のカテゴリIDを参考に、引数を1つ設定してください。")
    print("1：米・パン")
    print("2：肉、ハム類")
    print("3：魚介類")
    print("4：麺類")
    print("5：雑貨・日用品")
    print("6：野菜類")
    print("7：果物類")
    print("8：酒・アルコール")
    print("9：お茶・飲料")
    print("10：調味料・油")
    print("11：お菓子・スイーツ")
    print("12：旅行・チケット")
    print("13：セット類・その他")
    print("15：卵")
    print("16：加工食品")
    print("17：電化製品")
    print("18：工芸品")
    print("19：感謝状・記念品")

    # 処理を終了する
    sys.exit()
    
# お礼品名、自治体配列を初期化
productname_list = []
jichitai_list = []
product_donation_money_list = []

# WebDriverの起動（Chromeの例）
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('C:\driver\chromedriver_win32\chromedriver',options=options)

# 取得対象のURLを指定
url_for_pages = 'https://furunavi.jp/Product/Search?categoryid=' + categoryid + '&pagesize=100'

# ウェブページへのアクセス
driver.get(url_for_pages)
time.sleep(3)

html = driver.page_source.encode('utf-8')
ScrapingGetHtmlResponseHtml_for_count = BeautifulSoup(html, 'html.parser')

# FORの件数を決めるための事前準備
# 対象カテゴリの総件数を取得する
get_count_all = ScrapingGetHtmlResponseHtml_for_count.find('ul',attrs={'class':'pagination'})
count_all = get_count_all.find(attrs={'class':'product_count'})

# ページ数を設定（切り上げ）
for_count = int(int(count_all.text)/100) + 1
time.sleep(5)

# ページ分繰り返す
for i in range(for_count):
    # 取得対象のURLを指定
    url = 'https://furunavi.jp/Product/Search?categoryid=' + categoryid + '&pagesize=100&pageno=' + str(i+1)

    # ウェブページへのアクセス
    driver.get(url)
    print("データ取得中：" + str(i+1) + "/" + str(for_count))

    time.sleep(3)

    html = driver.page_source.encode('utf-8')
    ScrapingGetHtmlResponseHtml = BeautifulSoup(html, 'html.parser')

    # BeautifulSoup4のfind_all()メソッドで指定タグを取得する(お礼品名)
    get_productname = ScrapingGetHtmlResponseHtml.find_all('a',attrs={'data-name':'productid'},limit=100)
    # BeautifulSoup4のfind_all()メソッドで指定タグを取得する(自治体名)
    get_jichitai = ScrapingGetHtmlResponseHtml.find_all('p',attrs={'class':'product-municipal'},limit=100)
    # BeautifulSoup4のfind_all()メソッドで指定タグを取得する(寄付金額)
    get_product_donation_money = ScrapingGetHtmlResponseHtml.find_all('p',attrs={'class':'product-price'},limit=100)

    # BeautiflSoupで取得したデータは一回別のところに格納してから出力する
    for data in get_productname:
        productname = data.text
        # 文字列から先頭と末尾の空白を削除するためには、strip()メソッドを使用
        productname = productname.strip()
        # データが「##ProductName##」の場合は、対象外とする
        if productname != "##ProductName##":
            # 配列に格納する
            productname_list.append(productname)

    for data in get_jichitai:
        jichitai_name = data.text
        # 文字列から先頭と末尾の空白を削除するためには、strip()メソッドを使用
        jichitai_name = jichitai_name.strip()
        # 配列に格納する
        jichitai_list.append(jichitai_name)

    for data in get_product_donation_money:
        product_donation_money = data.text
        # 文字列から先頭と末尾の空白を削除するためには、strip()メソッドを使用
        product_donation_money = product_donation_money.strip()
        # 配列に格納する
        product_donation_money_list.append(product_donation_money)

# お礼品名、自治体名、寄付金額を一つの配列にまとめる（重複削除のため）
all_list = []

for list_num in range(len(productname_list)):
    all_list.append([jichitai_list[list_num],productname_list[list_num],product_donation_money_list[list_num]])

all_list_marge = get_unique_list.get_unique_list(all_list)

# ファイル出力する
with open('product_data_' + categoryid + '.csv', mode='w', encoding="utf-8_sig") as f:
    for list_count in range(len(all_list_marge)):
        f.write(all_list_marge[list_count][0] + "," + all_list_marge[list_count][1] + "," + all_list_marge[list_count][2] + "\n")

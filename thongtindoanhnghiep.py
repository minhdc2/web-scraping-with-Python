###########################THÔNG TIN DOANH NGHIỆP HÀ NỘI#################
import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from pandas.io.parsers import TextParser

with requests.session() as s:
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    no_pages = 5
    data_1 = []
    for j in np.arange(no_pages):
        url_text_1 = "https://thongtindoanhnghiep.co/tim-kiem?location=&kwd=&p=" + str(j+1)
        doc_1 = BeautifulSoup(s.get(url_text_1).text, "html.parser")
        a = doc_1.find_all("a")
        val1 = []
        for i in range(len(a)):
            val1.append(a[i].text)
        x1 = val1[11:71]
        x1_sub = []
        for i in range(len(x1)):
            x1_sub.append(x1[4*i:4*(i+1)])
        data_1.append(TextParser(x1_sub, names=["Company","Tax ID","Province","Business"]).get_chunk())
    table1 = pd.concat(data_1)
    table1["No"] = list(range(len(table1["Company"])))

    data_2 = []
    for j in np.arange(no_pages):
        url_text_2 = "https://thongtindoanhnghiep.co/tim-kiem?location=&kwd=&p=" + str(j+1)
        doc_2 = BeautifulSoup(requests.session().get(url_text_2).text, "html.parser")
        p = doc_2.find_all("p")
        val2 = []
        for i in range(len(p)):
            val2.append(p[i].text)
        x2 = val2[2:62]
        x2_sub = []
        for i in range(len(x2)):
            x2_sub.append(x2[4*i:4*(i+1)])
        data_2.append(TextParser(x2_sub, names=["Location","Founded Date","Address","Updated Date"]).get_chunk())
    table2 = pd.concat(data_2)
    table2["No"] = list(range(len(table2["Location"])))

    table = pd.merge(left = table1, right = table2, on = "No")

    del table["No"]

table.head()

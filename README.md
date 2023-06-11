# A_social_network_analysis_for_web_pages_2
* Dokuz Eylül Üniversitesi web sayfalarına yönelik bir sosyal ağ analizi ve bu sonuçların görselleştirmesi yapıldı. 
* https://www.deu.edu.tr/ ana sayfası ve altındaki tüm sayfalar ve buradaki tüm veriler kapsamdadır.

* Web sayfası bazlı üç centrality analizi yapılacaktır; Degree Centrality, Betweenness 	Centrality, Closeness Centrality. 
- Bu üç centrality analizi sonucu tüm web sayfaları en yüksekten en düşüğe tabloda sıralandı ve centrality_results dosyasına kaydedildi.
- Bu üç centrality analizi sonuçları, veri görselleştirmesi yapıldı ekran görüntüleri Grafikler dosyasına kaydedildi.

* !! soru_2.py dosyasındaki yorum kısmı ana sayfayı ve tüm alt sayfaları bulup txt dosyalarına yazdıran kısımdır.
Bunun yapmamım sebebi işlem uzun sürdüğü için hesaplama işlemlerini txt dosyalarında linlkeri çekerek yaptım.

## Kullanlın Kütüphaneler
- import re
- import pandas as pd
- import requests
- from bs4 import BeautifulSoup
- import os
- import csv
- import networkx as nx
- from urllib.parse import urljoin
- import matplotlib.pyplot as plt
- from urllib.parse import urlparse

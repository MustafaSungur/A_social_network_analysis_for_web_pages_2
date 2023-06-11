import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import csv
import networkx as nx
from urllib.parse import urljoin
import matplotlib.pyplot as plt
from urllib.parse import urlparse

def find_subpages(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        }
        response = requests.get(url, timeout=5, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            filtre =  str(href).split(".") 
            if href and href.startswith("http") and "deu" in filtre and "pdf" not in filtre and "jpeg" not in filtre:
                links.append(href)
        return links
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return []

def sanitize_filename(filename):
    # Link dosyalarını isimlendirirken geçersiz karakterleri çıkarır
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return filename

def write_links_to_csv(url, subpages):
    parsed_url = urlparse(url)
    filename =str(str(parsed_url.netloc) + str(parsed_url.path)) + ".csv"
    filename = sanitize_filename(filename)
   
    with open('links/' + filename, 'w', newline='',encoding='utf8',errors='replace') as csvfile:
        writer = csv.writer(csvfile)
        for subpage in subpages:
            writer.writerow([subpage])

def calculate_degree_centrality():
    graph = nx.Graph()
    for filename in os.listdir('links'):
        if filename.endswith('.csv'):
            page_url = filename.split('.')[0]
            if page_url =="www":
                continue
            graph.add_node(page_url)
                
            with open('links/' + filename, 'r',encoding='utf8') as subpage_csv:
                subpage_reader = csv.reader(subpage_csv)
                for subpage_row in subpage_reader:
                    subpage_url = subpage_row[0]
                    graph.add_edge(page_url, subpage_url)

    degree_centrality = nx.degree_centrality(graph)
    sorted_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
    return sorted_centrality

# Ana web sitesi 
main_url = 'https://www.deu.edu.tr/'

# Alt sayfaları bulur
# subpages = find_subpages(main_url)

# 'links' klasörünü oluşturur
if not os.path.exists('links'):
    os.makedirs('links')

# # Alt linkleri CSV dosyalarına yazar
# write_links_to_csv(main_url, subpages)
# for subpage in subpages:
#     subpage_subpages = find_subpages(subpage)
#     write_links_to_csv(subpage, subpage_subpages)

# Degree centrality hesaplar
degree_centrality = calculate_degree_centrality()

# İlk 50 değerleri alır
top_50_centrality = degree_centrality[:80]
pages, centrality_values = zip(*top_50_centrality)

# Sütun grafiği oluşturur
plt.bar(pages, centrality_values)
plt.xlabel('Sayfa')
plt.ylabel('Degree Centrality')
plt.xticks(rotation=90)
plt.title('Degree Centrality - İlk 80 Değer')
plt.tight_layout()

# Grafiği gösterir
plt.show()


def calculate_betweenness_centrality():
    graph = nx.Graph()
    for filename in os.listdir('links'):
        if filename.endswith('.csv'):
            page_url = filename.split('.')[0]
            if page_url =="www":
                continue
            graph.add_node(page_url)
            with open('links/' + filename, 'r',encoding='utf8') as subpage_csv:
                subpage_reader = csv.reader(subpage_csv)
                for subpage_row in subpage_reader:
                    subpage_url = subpage_row[0]
                    graph.add_edge(page_url, subpage_url)

    betweenness_centrality = nx.betweenness_centrality(graph)
    sorted_centrality = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)
    return sorted_centrality

# Betweenness centrality hesaplar
betweenness_centrality = calculate_betweenness_centrality()

# İlk 50 değeri alır
top_50_centrality = betweenness_centrality[:80]
pages, centrality_values = zip(*top_50_centrality)

# Sütun grafiği oluşturur
plt.bar(pages, centrality_values)
plt.xlabel('Sayfa')
plt.ylabel('Betweenness Centrality')
plt.xticks(rotation=90)
plt.title('Betweenness Centrality - İlk 80 Değer')
plt.tight_layout()

# Grafiği gösterir
plt.show()


def calculate_closeness_centrality():
    graph = nx.Graph()
    for filename in os.listdir('links'):
        if filename.endswith('.csv'):
            page_url = filename.split('.')[0]
            if page_url =="www":
                continue
            graph.add_node(page_url)
            with open('links/' + filename, 'r',encoding='utf8') as subpage_csv:
                subpage_reader = csv.reader(subpage_csv)
                for subpage_row in subpage_reader:
                    subpage_url = subpage_row[0]
                    graph.add_edge(page_url, subpage_url)

    closeness_centrality = nx.closeness_centrality(graph)
    sorted_centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
    return sorted_centrality

# Closeness centrality hesapla
closeness_centrality = calculate_closeness_centrality()

# İlk 50 değeri al
nodes = [node for node, _ in closeness_centrality[:80]]
centrality_values = [centrality for _, centrality in closeness_centrality[:80]]

# Sonuçları sütun grafiği olarak göster
plt.bar(nodes, centrality_values)
plt.xlabel('Düğüm')
plt.ylabel('Closeness Centrality')
plt.title('Closeness Centrality Sonuçları (İlk 80)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()



df_degree = pd.DataFrame.from_records(degree_centrality, columns=['Sayfa', 'Degree Centrality'])

df_betweenness = pd.DataFrame.from_records(betweenness_centrality, columns=['Sayfa', 'Betweenness Centrality'])

df_closeness = pd.DataFrame.from_records(closeness_centrality, columns=['Sayfa', 'Closeness Centrality'])

# Excel dosyasına kaydet
with pd.ExcelWriter('centrality_results.xlsx') as writer:
    df_combined = pd.concat([df_degree, df_betweenness, df_closeness], axis=1)
    df_combined.to_excel(writer, sheet_name='Centrality Results', index=False)
    
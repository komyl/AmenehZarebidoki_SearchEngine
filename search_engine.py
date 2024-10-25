import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Scraping functions (same as before)
def scrape_wikipedia(search_term):
    search_url = f'https://en.wikipedia.org/wiki/{search_term.replace(" ", "_")}'
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1', id='firstHeading').text.strip()
        first_paragraph = soup.find('p').text.strip()
        return f"🔍 Wikipedia Page: {title}\nIntroduction: {first_paragraph}\nRead the full article here: {search_url}\n"
    else:
        return f"Failed to retrieve the page for '{search_term}'. Status code: {response.status_code}\n"

def scrape_arxiv(search_term, num_results=5):
    search_url = f'https://arxiv.org/search/?query={search_term.replace(" ", "+")}&searchtype=all&source=header'
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        papers = soup.find_all('li', class_='arxiv-result')
        results = "📄 arXiv Results:\n"
        if papers:
            for paper in papers[:num_results]:
                title = paper.find('p', class_='title').text.strip()
                link = "https://arxiv.org" + paper.find('a')['href']
                results += f"{title}\n{link}\n"
            return results
        else:
            return "No papers found on arXiv.\n"
    else:
        return f"Could not retrieve arXiv results. Status code: {response.status_code}\n"

def scrape_google_scholar(search_term, num_results=5):
    search_url = f'https://scholar.google.com/scholar?hl=en&q={search_term.replace(" ", "+")}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('h3', class_='gs_rt')
        results = "📚 Google Scholar Results:\n"
        if articles:
            for article in articles[:num_results]:
                title = article.find('a').text.strip()
                link = article.find('a')['href'] if article.find('a')['href'].startswith('http') else None
                results += f"{title}\n{link}\n"
            return results
        else:
            return "No articles found on Google Scholar.\n"
    else:
        return f"Could not retrieve Google Scholar results. Status code: {response.status_code}\n"

def scrape_pubmed(search_term, num_results=5):
    search_url = f'https://pubmed.ncbi.nlm.nih.gov/?term={search_term.replace(" ", "+")}'
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('a', class_='docsum-title')
        results = "🔬 PubMed Results:\n"
        if articles:
            for article in articles[:num_results]:
                title = article.text.strip()
                link = "https://pubmed.ncbi.nlm.nih.gov" + article['href']
                results += f"{title}\n{link}\n"
            return results
        else:
            return "No articles found on PubMed.\n"
    else:
        return f"Could not retrieve PubMed results. Status code: {response.status_code}\n"

def perform_search():
    search_term = entry.get()
    if search_term:
        results_text.delete(1.0, tk.END)  # Clear previous results
        results = ""
        results += scrape_wikipedia(search_term)
        results += scrape_arxiv(search_term)
        results += scrape_google_scholar(search_term)
        results += scrape_pubmed(search_term)
        results_text.insert(tk.END, results)  # Insert new results
    else:
        messagebox.showwarning("Input Error", "Please enter a search term.")

# GUI setup
root = tk.Tk()
root.title("Amy's Search Engine")
root.geometry("600x400")

label = tk.Label(root, text="Enter a topic or keyword to search:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=perform_search)
search_button.pack(pady=10)

results_text = scrolledtext.ScrolledText(root, width=70, height=15)
results_text.pack(pady=5)

welcome_message = "Hello! Welcome to Amy's Search Engine! We provide search capabilities across Wikipedia, Google Scholar, arXiv, and PubMed. Let’s have fun exploring your articles! If you want to improve this, feel free to check GitHub."
results_text.insert(tk.END, welcome_message)  # Insert welcome message at start

root.mainloop()

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def scrape_documentation(url, output_dir, depth=1, max_depth=2):
    if depth > max_depth:
        return

    print(f'Scraping {url} at depth {depth}')

    response = requests.get(url)
    if response.status_code != 200:
        print(f'Failed to retrieve the page: {response.status_code}')
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # Save the current page content to a file
    section_name = url.split('/')[-1]  # Get the last part of the URL for the file name
    file_name = os.path.join(output_dir, f'{section_name}.txt')
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(soup.text)

    # Assume that documentation is organized with links to individual pages
    links = [a['href'] for a in soup.find_all('a', href=True) if 'docs' in a['href']]
    #print(links)
    
    for link in links:
        # Construct the absolute URL for each link
        # Note: This assumes that all links are relative. 
        # You might need to handle absolute links differently.
        #doc_url = f'{url}/{link}' if not link.startswith('http') else link
        doc_url = urljoin(url, link)
        scrape_documentation(doc_url, output_dir, depth=depth + 1, max_depth=max_depth)

# Usage
#base_url = 'https://elasticpath.dev/docs/pxm/products'
base_url = 'https://elasticpath.dev/docs/pxm/products/ep-pxm-products-api/pxm-products-api-overview'
output_dir = 'elastic_path_docs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
scrape_documentation(base_url, output_dir)

import requests
from bs4 import BeautifulSoup
import csv

url = 'https://doors.stanford.edu/~sr/universities.html'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    target_element = soup.find('hr') # remove all content before the first horizontal rule 
    # (before hr explains the content of the page, not the content itself)

    parsed_content = target_element.find_next_siblings() # get all elements after the first horizontal rule
    universities_elements = parsed_content
    universities_contents = soup.find_all('a') # gets a tags with university names but with trash included (trash includes dom elements, unrelated content, escape sequences, and single chars)

    # removes dom elements
    universities_names_with_esc_seq_and_unrelated_content = [university.text.split('</a>')[0] for university in universities_contents]
    
    # removes the unrelated content
    for index, university in enumerate(universities_names_with_esc_seq_and_unrelated_content):
        if university.startswith('\n\t'):
            universities_names_with_esc_seq_and_unrelated_content = universities_names_with_esc_seq_and_unrelated_content[index:]
            break
    
    universities_names_with_esc_seq = universities_names_with_esc_seq_and_unrelated_content
    
    # remove the escape sequences
    for index, university in enumerate(universities_names_with_esc_seq):
        if university.startswith('\n\t'):
            universities_names_with_esc_seq[index] = university[2:]
        elif university.startswith('\n   '):
            universities_names_with_esc_seq[index] = university[9:]
    
    universities_names_with_single_chars = universities_names_with_esc_seq

    universities_names = [university.strip() for university in universities_names_with_single_chars if len(university) > 4] # remove the single chars and niche separators (ex: UM) (it is in alphabetical order, hence why single chars exist)

    print(*universities_names, sep='\n')

    csv_file_path = 'university_data.csv'
    
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        csv_writer.writerow([university for university in universities_names])
    
    print(f"Scraping completed. Data has been saved to '{csv_file_path}'.")
else:
    print("Failed to retrieve the webpage.")

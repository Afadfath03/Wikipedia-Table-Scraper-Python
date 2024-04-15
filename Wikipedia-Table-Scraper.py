import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_user_input():
    wiki_url = input("\nEnter the Wikipedia URL to scrape (e.g., https://en.wikipedia.org/wiki/List_of_XX_episodes): ")
    return wiki_url

def get_desired_format():
    print("\nAvailable file format:")
    print("1. JSON")
    print("2. TXT (Numbered List)")
    print("3. TXT (Unnumbered List)")
    format_choice = input("Choose file format: ")

    valid_formats = {"1": "JSON", "2": "TXTN", "3": "TXTU"}
    chosen_format = valid_formats.get(format_choice)

    if not chosen_format:
        raise ValueError("Invalid format. Please choose available format.")
    else:
        return chosen_format

def scrape_wikipedia_table(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="wikitable")

        episode_titles = []
        rows = table.find_all("tr", class_="module-episode-list-row")
        for row in rows:
            title_element = row.find("td", class_="summary")
            title_text = title_element.get_text().strip()

            transliteration_index = title_text.lower().find("transliteration:")
            if transliteration_index != -1:
                episode_title = title_text[:transliteration_index].strip()
            else:
                episode_title = title_text

            episode_titles.append(episode_title)

        return episode_titles
    except Exception as e:
        print("Error scraping data:", e)
        return []

def create_result_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def create_numbered_list_file(file_path, episode_titles):
    with open(file_path, "w") as file:
        for i, title in enumerate(episode_titles, 1):
            file.write(f"{i}. {title}\n")
    print(f"\nTXT file saved to {file_path}")

def create_unnumbered_list_file(file_path, episode_titles):
    with open(file_path, "w") as file:
        file.write("\n".join(episode_titles))
    print(f"\nTXT file saved to {file_path}")

def create_json_file(file_path, episode_titles):
    import json
    with open(file_path, "w") as file:
        json.dump(episode_titles, file, indent=2)
    print(f"\nJSON file saved to {file_path}")

def main():
    try:
        wiki_url = get_user_input()
        result_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Result")
        create_result_folder(result_folder_path)

        episode_titles = scrape_wikipedia_table(wiki_url)

        desired_format = get_desired_format()
        file_name = f"episode_titles_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        if desired_format == "JSON":
            create_json_file(os.path.join(result_folder_path, f"{file_name}.json"), episode_titles)
        elif desired_format == "TXTN":
            create_numbered_list_file(os.path.join(result_folder_path, f"{file_name}.txt"), episode_titles)
        elif desired_format == "TXTU":
            create_unnumbered_list_file(os.path.join(result_folder_path, f"{file_name}.txt"), episode_titles)
        else:
            raise ValueError("Invalid format. Please choose available format.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
from uuid import uuid4
import logging

def search_book(title):
    # Encode the title for URL usage
    query = title.replace(" ", "+")
    url = f"https://audiobookbay.lu/?s={query}"

    # Make a request to the AudioBook Bay search page
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0" ,
                                          "Accept-Language": "en-US,en;q=0.5",
                                          "Accept-Encoding": "gzip, deflate, br",
                                          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Connection": "keep-alive"}
                            )
    soup = BeautifulSoup(response.content, 'html.parser')
    books = []
    for item in soup.find_all("div", class_="post"):  # Hypothetical class name for book entries
        book_title = item.find("a").text
        book_link = item.find("a")["href"]
        books.append({"title": book_title, "link": book_link})
    
    
    
    return books

def download_book(link):
    pass

def fetch_book(url):
    # Complete URL to fetch book details
    link = "https://audiobookbay.lu" + url
    try:
        # Make HTTP GET request to fetch page content
        
        response = requests.get(link, headers={"User-Agent": "Mozilla/5.0" ,
                                          "Accept-Language": "en-US,en;q=0.5",
                                          "Accept-Encoding": "gzip, deflate, br",
                                          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Connection": "keep-alive"}
                            )

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract book details
        title = soup.find("h1")
        #magnet = 
        author = soup.find("span", class_="author")
        read_by = soup.find("span", class_="narrator")
        #image is href with m.media-amazon.com in it
        image = None
        #url of the page

        
        # Construct and return a dictionary with book details
        details = {
            
            "title": title.text,
            "author": author.text,
            "read_by": read_by.text,
            "image": image,
            'url': link
            
        }
        for key, value in details.items():
            print("\n")
            print(f"{key}: {value}")
            
        return details

    except requests.RequestException as e:
        
            logging.error(f"Request failed: {e}") 
            
    except ValueError as e:
        
            logging.error(f"Invalid response: {e}")

        
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    # Return None if there were any failures
    return None

def download_image(url):
    if not url:
        return None
    # Make an HTTP GET request to fetch the image content
    response = requests.get(url)
    file_name = f"{uuid4()}.{url.split('.')[-1]}"
    if response.status_code == 200:
        # Save the image content to a file
        with open(file_name, "wb") as file:
            file.write(response.content)
        return file_name
    return None


def login():
    # Make a POST request to the login page
    url = "https://audiobookbay.lu/wp-login.php"
    
    data = {
        "log": "bdrkh",
        "pwd": "6iepoecaem",
        "rememberme": "forever",
        "wp-submit": "Log In",
        "redirect_to": "wp-admin/",
        "testcookie": "1"
    }
    headers = {
        "User-Agent": "Mozilla/5.0" ,
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Connection": "keep-alive"
    }
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Logged in successfully!")
    else:
        print("Failed to login.")
        print(response.status_code)
        print(response.content)
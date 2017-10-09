import time
import os
import urllib
import urllib.request

words_to_search = ['rice', 'potato', 'beans', 'steak', 'pork']

keywords = [' ', 'dish', 'plate', 'recipe']


def format_spaces_to_urls(str):
    return str.replace(' ', '%20')


def download_page_raw_html(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        response_data = str(response.read())
        return response_data
    except Exception as e:
        print(str(e))
        return None


def download_image(image_url):
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError

    data = None

    try:
        request = Request(image_url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
        response = urlopen(request, None, 15)

        data = response.read()
        response.close()
    except (HTTPError, URLError):
        data = None

    return data

def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = None
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content

def parse_google_images_results(googleImageResultsPage):
    page = googleImageResultsPage
    urls = []
    while True:
        url, end_content = _images_get_next_item(page)
        if url == None:
            break
        else:
            urls.append(url)
            page = page[end_content:]
    return urls


def get_google_image_search(search_str):
    from urllib import parse
    
    url = 'https://www.google.com/search?q=' + parse.quote_plus(search_str) + \
        '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    page_raw_html = download_page_raw_html(url)
    return parse_google_images_results(page_raw_html)


def write_to_file(path, content):
    output_file = open(path, 'wb')
    output_file.write(content)
    output_file.close()



begin_time = time.time()  # start the timer

i = 0
while i < len(words_to_search):
    urls = []

    word = words_to_search[i]

    print ("Item no.: " + str(i + 1) + " --> Item name = " + str(word))
    print ("Evaluating...")

    j = 0
    while j < len(keywords):
        searchStr = word + " " + keywords[j]
        print ("Searching for: " + searchStr)
        urls = urls + get_google_image_search(searchStr)
        j = j + 1

    print ("Total Image Links = " + str(len(urls)))
    print ("\n")

    # This allows you to write all the links into a test file. This text file will be created in the same directory as your code. You can comment out the below 3 lines to stop writing the output to the text file.
    info = open('output.txt', 'a')  # Open the text file called database.txt
    # Write the title of the page
    info.write(str(i) + ': ' + word + ": " + str(urls) + "\n\n\n")
    info.close()  # Close the file

    current_time = time.time()  # stop the timer
    # Calculating the total time required to crawl, find and download all the links of 60,000 images
    total_time = current_time - begin_time
    print("Total time taken: " + str(total_time) + " Seconds")

    print ("Starting Download...")

    k = 0
    errorCount = 0

    try:
        os.makedirs(word)
    except OSError as e:
        if e.errno != 17:
            raise
        # time.sleep might help here
        pass

    while(k < len(urls)):
        try:
            image_url = urls[k]
            image_data = download_image(image_url)

            if image_data != None:
                image_path = word + "/" + str(k + 1)

                if ".png" in image_url:
                    image_path = image_path + ".png"
                else:
                    image_path = image_path + ".jpg"

                write_to_file(image_path, image_data)

            print("completed ====> " + str(k + 1))

        except IOError:  # If there is any IOError

            errorCount += 1
            print("IOError on image " + str(k + 1))

        finally:
            k = k + 1

    i = i + 1

print("\n")
print("Everything downloaded!")
print("\n" + str(errorCount) + " ----> total Errors")
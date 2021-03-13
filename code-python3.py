# Credits to 'nazarpechka' for helping out with this code
# 'DeVviL' was update for more random and fix file extension

import string, random, os, sys, _thread, httplib2, time
from PIL import Image

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python3 " + sys.argv[0] + " (Number of threads)")
THREAD_AMOUNT = int(sys.argv[1])

INVALID = [0, 503, 5296]

try:
    os.mkdir('scraped-photos')
except:
    pass

def scrape_pictures(thread):
    while True:
        #url = 'http://img.prntscr.com/img?url=http://i.imgur.com/'
        url = 'http://i.imgur.com/'
        length = random.randint(5, 7)
        letter = random.randint(1, length)
        url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(letter))
        url += ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length - letter))
        url += '.jpg'
        # print (url)

        file_path = 'scraped-photos/'
        filename = file_path+url.rsplit('/', 1)[-1]
        # print (filename)

        h = httplib2.Http('.cache' + thread)
        response, content = h.request(url)
        out = open(filename, 'wb')
        out.write(content)
        out.close()

        file_size = os.path.getsize(filename)
        if file_size in INVALID:
            print("[-] Invalid: " + url)
            os.remove(filename)
        else:
            print("[+] Valid: " + url)

            try:
                img = Image.open(filename)
                format = img.format
                img.close()

                if format == "PNG":
                    if img != '.png':
                        os.rename(filename, os.path.splitext(filename)[0] + ".png")
                if format == "GIF":
                    if img != '.gif':
                        os.rename(filename, os.path.splitext(filename)[0] + ".gif")
            except IOError:
                os.remove(filename)

for thread in range(1, THREAD_AMOUNT + 1):
    thread = str(thread)
    try:
        _thread.start_new_thread(scrape_pictures, (thread,))
    except:
        print('Error starting thread ' + thread)
print('Succesfully started ' + thread + ' threads.')

while True:
    time.sleep(1)

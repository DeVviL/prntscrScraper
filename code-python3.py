#Credits to 'nazarpechka' for helping out with this code

import string, random, os, sys, _thread, httplib2, time
# from PIL import Image

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python3 " + sys.argv[0] + " (Number of threads)")
THREAD_AMOUNT = int(sys.argv[1])

INVALID = [0, 503, 5296]

def scrape_pictures(thread):
    while True:
        #url = 'http://img.prntscr.com/img?url=http://i.imgur.com/'
        url = 'http://i.imgur.com/'
        length = random.choice((5, 6))
        file_path = 'scraped-photos/'
        if length == 5:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        else:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
            url += ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))
            url += '.jpg'
            # print (url)


            filename = file_path+url.rsplit('/', 1)[-1]
            # print (filename)

            h = httplib2.Http('.cache' + thread)
            response, content = h.request(url)
            try:
                out = open(filename, 'wb')
            except:
                os.mkdir('photos')
                out = open(filename, 'wb')
            out.write(content)
            out.close()

            file_size = os.path.getsize(filename)
            if file_size in INVALID:
                print("[-] Invalid: " + url)
                os.remove(filename)
            else:
                print("[+] Valid: " + url)

for thread in range(1, THREAD_AMOUNT + 1):
    thread = str(thread)
    try:
        _thread.start_new_thread(scrape_pictures, (thread,))
    except:
        print('Error starting thread ' + thread)
print('Succesfully started ' + thread + ' threads.')

while True:
    time.sleep(1)

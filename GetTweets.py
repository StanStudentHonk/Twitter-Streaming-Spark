import twitter
import socket
import json
TCP_IP = "localhost"
TCP_PORT = 9876
KEY_WORD = 'football'

def twt_app(TCP_IP,TCP_PORT,keyword=KEY_WORD):

    consumer_key= ''
    consumer_secret= ''
    access_token= ''
    access_token_secret= ''
    
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret,
                      sleep_on_rate_limit=True)

    LANGUAGES = ['en']
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(10)
    print("Waiting for TCP connection...")
    
    conn, addr = s.accept()
    print("Connected... Starting getting tweets.")
    
    for line in api.GetStreamFilter(track=[keyword],languages=LANGUAGES):
        conn.send( line['text'].encode('utf-8') )
        print(line['text'])
        print()
        
if __name__=="__main__":
    twt_app(TCP_IP,TCP_PORT,keyword=KEY_WORD)
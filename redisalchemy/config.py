from redis import Redis

redis = Redis(host='localhost', port=6379, db=0)

def config(host='localhost', port=6379, db=0):
    global redis
    redis = Redis(host=host, port=port, db=db)
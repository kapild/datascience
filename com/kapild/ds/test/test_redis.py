from ds.backend.redis.Redis import RedisStoreImpl


def test_redis():
    redis_dict = {
        "read": {
            "host": "127.0.0.1",
            "port": 6379,
            "db": 0,
        },
        "write": {
            "host": "localhost",
            "port": 6379,
            "db": 0,
        }
    }
    fsq_redis = RedisStoreImpl(redis_dict)
    set_name = "kapil"
    fsq_redis.set_add(set_name, "kapil")
    print(fsq_redis.set_members("name"))


if __name__ == "__main__":
    test_redis()
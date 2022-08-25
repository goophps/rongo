STORES = {
    "default": "redis",
    "stores": {
        "redis": {
            "backend": "rongo.cache.drivers.RedisDriver",
            "host": "127.0.0.1",
            "port": "6379",
            "password": "",
            "timeout": 10,
            "db": 0,
            "prefix": "",
            "expire": 0,
        },
        "memcached": {
            "backend": "rongo.cache.drivers.MemcachedDriver",
            "host": "127.0.0.1",
            "port": "11211",
            "timeout": 10,
            "prefix": "",
            "expire": 0,
        },
    }

}

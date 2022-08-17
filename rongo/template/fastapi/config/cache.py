STORES = {
    "default": "redis",
    "stores": {
        "redis": {
            "backend": "rongo.cache.drivers.RedisDriver",
            "host": "127.0.0.1",
            "port": "6379",
            "password": "",
            "db": 0,
            "prefix": "",
            "expire": 0,
        },
    }

}

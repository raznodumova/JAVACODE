from functools import wraps


def my_decor(old_func):
    cache_dict = {}

    @wraps(old_func)
    def new_func(*args):
        max_cache = 100
        if args in cache_dict:
            return cache_dict[args]
        else:
            result = old_func(*args)
            cache_dict[args] = result
            if len(cache_dict) > max_cache:
                cache_dict.popitem(last=False)
            return result

    return new_func

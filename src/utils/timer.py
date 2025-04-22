import time
from src.utils.utils import fancy_print


def time_complexity(name_process):
    
    def decorator_factory(func): 

        def wraper(*args, **kwargs): 
            t1 = time.time() 
            result = func(*args, **kwargs) 
            t2 = time.time() 

            duration = t2-t1
            fancy_print(f'DONE PROCESS {name_process} IN {duration:.4f}s')
            return result 
        
        return wraper 
    
    return decorator_factory

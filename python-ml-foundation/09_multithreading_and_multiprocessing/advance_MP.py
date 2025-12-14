from concurrent.futures import ProcessPoolExecutor
import time

def print_numbers():
    for num in range(5):
        time.sleep(1)
        return f"Numbers:{num}"

numbers=[1,2,231,32,43,43,23,34,23,43,12,342,12,23,21,3,4,5]
if __name__=="__main__":
    with ProcessPoolExecutor(max_workers=3) as executor:
        results= executor.map(print_numbers,numbers)

    for result in results:
        print(result)
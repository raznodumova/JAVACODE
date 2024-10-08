import random
import math
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import json
import time


def generate_data(n):
    return [random.randint(1, 1000) for i in range(n)]


def process_number(number):
    if number == 0:
        return 1
    else:
        return math.factorial(number)

#--------------вариант А-------------------------------
def variant_A(data):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(process_number, data)
    return list(results)

#--------------вариант Б-------------------------------
def variant_B(data):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(process_number, data)
    return results

#--------------вариант В-------------------------------
def variant_C(input_queue, output_queue):
    while True:
        number = input_queue.get()
        if number is None:  # Сигнал завершения
            break
        result = process_number(number)
        output_queue.put(result)


def process_with_individual_processes(data):
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()
    processes = []

    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=variant_C, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    for number in data:
        input_queue.put(number)

    # Сигнал окончания для каждого процесса
    for _ in processes:
        input_queue.put(None)

    results = []
    for _ in data:
        results.append(output_queue.get())

    for p in processes:
        p.join()

    return results

#--------------сравнение производительности-------------------------------


def main(n):
    # Генерируем данные
    data = generate_data(n)

    # Однопоточный вариант
    start = time.time()
    single_thread_results = [process_number(num) for num in data]
    single_thread_time = time.time() - start

    # Вариант А: Потоки
    start = time.time()
    thread_results = variant_A(data)
    threads_time = time.time() - start

    # Вариант Б: Пул процессов
    start = time.time()
    pool_results = variant_B(data)
    pool_time = time.time() - start

    # Вариант В: Отдельные процессы
    start = time.time()
    individual_process_results = process_with_individual_processes(data)
    individual_process_time = time.time() - start

    # Сохранение результаты в JSON файл
    results = {
        "Single Thread": single_thread_results,
        "Thread Pool": thread_results,
        "Process Pool": pool_results,
        "Individual Processes": individual_process_results
    }

    with open('results.json', 'w') as f:
        json.dump(results, f)

    # Сравнительная таблица времени
    performance_comparison = {
        "Variant": ["Single Thread", "Thread Pool", "Process Pool", "Individual Processes"],
        "Time (seconds)": [single_thread_time, threads_time, pool_time, individual_process_time]
    }

    print(performance_comparison)


if __name__ == "__main__":
    main(100)
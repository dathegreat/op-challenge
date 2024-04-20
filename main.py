import random, time

#data structure to store IP addresses
ip_request_count = {}

def requestHandled(ipAddress: str):
    #increment the ip's request count, or initialize to 1 if ip is new
    ip_request_count[ipAddress] = ip_request_count.get(ipAddress, 0) + 1

def top100(ip_data: dict) -> list:
    sorted_dictionary = sorted(ip_data, key=lambda x:x[1], reverse=True )
    return sorted_dictionary[0:100]

def test_sort_time(test_data_size: int, iterations_to_run: int) -> float:
    run_times = []
    #generate many fake ip addresses and counts
    print("generating fake ip data")
    test_ip_data = {}
    for i in range(0, test_data_size):
        random_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        test_ip_data[random_ip] = random.randint(1,10000)
    print("starting sort test")
    for i in range(0, iterations_to_run):
        #time getting top 100 visitors
        print(f"iteration: {i}")
        start_time = time.perf_counter()
        top = top100(test_ip_data)
        end_time = time.perf_counter()
        run_times.append(end_time - start_time)
        print(test_ip_data[top[0]], test_ip_data[top[99]])
        print("completed in: ", (end_time - start_time) * 1000, "ms")
    #return average run time
    return sum(run_times) / iterations_to_run

def test_insert_time(iterations_to_run: int) -> tuple[float, float]:
    fresh_insert_times = []
    update_times = []
    print("starting insert test")
    for i in range(0, iterations_to_run):
        #time inserting new ip
        start_time = time.perf_counter()
        random_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        requestHandled(random_ip)
        end_time = time.perf_counter()
        fresh_insert_times.append(end_time - start_time)
        #time updating ip count
        start_time = time.perf_counter()
        requestHandled(random_ip)
        end_time = time.perf_counter()
        update_times.append(end_time - start_time)
    #return average run time
    return (sum(fresh_insert_times) / iterations_to_run, sum(update_times) / iterations_to_run)

print("AVERAGE SORT TIME:", test_sort_time(200000, 10) * 1000, "ms")
insert_times = test_insert_time(1000)
print("AVERAGE INSERT TIME:", insert_times[0] * 1000, "ms")
print("AVERAGE UPDATE TIME:", insert_times[1] * 1000, "ms")



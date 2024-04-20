import random, time
#data structure to store IP addresses and their counts
#e.g. {key: "16.16.9.17"}
ip_request_count: dict[str, int]  = {}
#a running deque of highest count ip addresses, in descending order from left to right
#e.g. [(100, "16.16.9.17"), (85, "34.106.4.31"), ... (2, "54.207.159.35")]
top_ip_addresses: list[tuple[int, str]] = []

def requestHandled(ipAddress: str):
    #increment the ip's request count, or initialize to 1 if the ip is new
    new_count = ip_request_count.get(ipAddress, 0) + 1
    ip_request_count[ipAddress] = new_count
    #add count right away if deque is empty, then don't bother checking rest of empty deque
    if len(top_ip_addresses) == 0:
        top_ip_addresses.append( (new_count, ipAddress) )
        return
    #perform initial loop to see if the address already exists in the top addresses.
    #This could be optimized by keeping a separate set of all the addresses currently in the deque
    #so that the lookup would run in O(1) time (since python sets use hash tables under the hood),
    #but at the cost of more moving parts and likelihood for separate data structures to go out of sync.
    #Since the deque is only ever 100 items long, it is a tiny optimization anyway
    for i in range(0, len(top_ip_addresses)):
        if top_ip_addresses[i][1] == ipAddress:
            #the item is simply deleted because it will be added again in the correct place
            #with an updated count later in the function
            del top_ip_addresses[i]
            break
    #check to see if ip's count has surpassed any elements in the deque
    for i in range(0, len(top_ip_addresses)):
        #prevent annoying indexes popping up as we reference these values by giving them a name
        count, address = top_ip_addresses[i]
        if new_count >= count:
            #remove smallest count from deque if deque is full to make room for new_count
            #which is guaranteed to be greater than the smallest deque item.
            #I chose >= here instead of == because only checking for equality scares me.
            #If by some wizardry the length jumped from 99 straight to 101, then the deque
            #could, in theory, grow large enough to consume the world and everyone I love.
            if len(top_ip_addresses) >= 100:
                top_ip_addresses.pop()
            top_ip_addresses.insert(i, (new_count, ipAddress))
            break

def top100() -> list:
    return list(map(lambda x: x[1], top_ip_addresses))

def clear():
    ip_request_count.clear()
    top_ip_addresses.clear()


#----------JANKY TESTING CODE FOR MY PEACE OF MIND---------------
#-----------------PROCEED AT YOUR OWN RISK-----------------------

def get_random_ip() -> str:
    #thank you stack overflow for this one-line monstrosity, which generates
    #a random ip address of the form a.b.c.d
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def test_sort_time(test_data_size: int, iterations_to_run: int) -> float:
    run_times = []
    #generate many fake ip addresses and counts
    print("generating fake ip data (this will take a while)")
    #a small percentage of the time, pull the last ip and run it through again
    last_generated_ip = ""
    for i in range(0, test_data_size):
        #thank you stack overflow for this one-line monstrosity, which generates
        #a random ip address of the form a.b.c.d
        random_ip = get_random_ip()
        random_number = random.randint(0,100)
        requestHandled(random_ip if random_number > 1 else last_generated_ip)
        last_generated_ip = random_ip
    print("starting sort test")
    for i in range(0, iterations_to_run):
        #time getting top 100 visitors
        print(f"iteration: {i}")
        start_time = time.perf_counter()
        top = top100()
        end_time = time.perf_counter()
        run_times.append(end_time - start_time)
        print("0th place ", ip_request_count[top[0]], "99th place: ", ip_request_count[top[99]])
        print("completed in: ", (end_time - start_time) * 1000, "ms")
    #reset state (not safe, I know, tests should be stateless, but I'm not writing real unit tests here)
    clear()
    #return average run time
    return sum(run_times) / iterations_to_run

def test_insert_time(iterations_to_run: int) -> tuple[float, float]:
    fresh_insert_times = []
    update_times = []
    print("starting insert test")
    for i in range(0, iterations_to_run):
        #time inserting new ip
        start_time = time.perf_counter()
        random_ip = get_random_ip()
        requestHandled(random_ip)
        end_time = time.perf_counter()
        fresh_insert_times.append(end_time - start_time)
        #time updating ip count
        start_time = time.perf_counter()
        requestHandled(random_ip)
        end_time = time.perf_counter()
        update_times.append(end_time - start_time)
    clear()
    #return average run time
    return (sum(fresh_insert_times) / iterations_to_run, sum(update_times) / iterations_to_run)

def test_top_ip_addresses_maintains_correct_length_after_update():
    random_ips = []
    for i in range(0,5):
        random_ips.append(get_random_ip())
    for ip in random_ips:
        requestHandled(ip)
    print("length of top_ip_addresses == 5 on init: ", len(top_ip_addresses) == 5, len(top_ip_addresses))
    requestHandled(random_ips[0])
    print("length of top_ip_addresses == 5 after update: ", len(top_ip_addresses) == 5, len(top_ip_addresses))
    clear()

def test_top_ip_addresses_maintain_sorted_order():
    random_ips = []
    for i in range(0,500):
        random_ips.append(get_random_ip())
    for ip in random_ips:
        requestHandled(ip)
    #increment random ip's 5000 times
    #by my super fuzzy memory of the pigeonhole principle, I think this means we are guaranteed
    #at the top 100 will all be incremented to varying degrees, or something like that
    for i in range(0, 5000):
        requestHandled(random_ips[random.randint(0, len(random_ips)) - 1])
    for i in range(0, 5000):
        requestHandled(random_ips[0])
    #test to see if the deque is ordered
    for i in range(1, len(top_ip_addresses)):
        if top_ip_addresses[i - 1][0] < top_ip_addresses[i][0]:
            print(f"{i-1}: {top_ip_addresses[i - 1][0]}, {i}, {top_ip_addresses[i][0]}")
            print(top_ip_addresses)
            return False
    return True
    clear()

print("AVERAGE SORT TIME:", test_sort_time(20_000_000, 10) * 1_000, "ms")
insert_times = test_insert_time(1_000)
print("AVERAGE INSERT TIME:", insert_times[0] * 1_000, "ms")
print("AVERAGE UPDATE TIME:", insert_times[1] * 1_000, "ms")
test_top_ip_addresses_maintains_correct_length_after_update()
print("top ip addresses maintain sorted order: ", test_top_ip_addresses_maintain_sorted_order())



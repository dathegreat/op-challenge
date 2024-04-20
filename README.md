# Overview

### Naive Approach
Initially, I implemented the naive approach of creating a hashmap with ip addresses as the keys and their request count as the values. Then, I sorted by value and sliced the top 100 when `top100()` was called. Not surprisingly, this ran quite fast on insertion, but horrendously slow on sort. I created a basic test function, and on my laptop each sort took almost *eight seconds* at `n=20,000,000`. Needless to say, I immediately went to brainstorming a more optimized solution. This lead to...

### Optimized Solution
I still kept the hash table for keeping score of all the millions of ip addresses, but I added a deque for keeping track of the top 100. This deque has some basic rules to keep it reliable: 

* It must never exceed 100 items in length
* At any given point in time it must be fully sorted 
* It must perform all needed operations in linear or sub-linear time

Because of these regulations, the `top100()` function was greatly simplified to only pulling and returning the values from the deque in their existing order. This reduced the runtime in tests to *0.023 milliseconds* for 20,000,000 test addresses. 

# Function Complexity Breakdown
##### *all given time averages are tested at `n=20,000,000`*
### requestHandled()
##### O(n), Ω(1), Average insert time: 4.13 μs, Average update time: 0.07 μs
Performs several operations on a dictionary and list with O(1) time complexity, and several with O(n) time complexity. None of these operations are nested, and so the function runs in O(n) time overall. Additionally, I implemented some minor optimizations so that the best case time complexity is Ω(1). Because the function only operates at a maximum of `n=100`, it is incredibly fast. 

### top100()
##### O(n), Ω(n), Average runtime: 23.15 μs
Performs two basic linear operations, iterating over the deque once to extract its addresses and again to convert it to a list (this second operation was not required in the documentation, but felt like a nice thing to do).

### clear()
##### O(n), Ω(1)
Performs two operations, clearing the hashmap and deque. Depending on who you ask, these could be considered constant time operations, but since garbage collection technically does occur as a result of the function call, I choose to label it O(n).

# Solutions I thought about, but decided against
In preliminary brainstorming, I thought about using some sort of balanced tree like an AVL tree, but I decided against it because: 
* a) It felt needlessly complicated
* b) I didn't want to download any external code if I could help it, and python does not have a native tree implementation
* c) I would have had to extend python's tuple class to define the overall comparator value for an (address, count) tuple. 

I also stumbled across a python library called Sorted Collections, which boasted a sorted dictionary data type and really fast operations. However, I decided against using this for reason b) above, and because I would have had to figure out some way to sort the dictionary by value, not key, which didn't seem possible without heavy modification. 

# Testing
I would test this with the same mindset apparent in my janky tests, but with a lot more time and effort involved. Additionally, I would add significantly more tests to cover edge cases and different data sizes. Oh, and I would very much employ a testing framework instead of printing to the console like a mad man. 

# Further Improvement
While writing the code, I thought often about how it would probably explode if anyone tried to run it asynchronously. There are many calls to and iterations over a shared data structure in the `requestHandled()` function, and that would be a lot of work to try and lock down with a semaphore. If this were to actually live in production somewhere, I would consider ways to modify the algorithm so that parallelism takes more of a center stage in the design.
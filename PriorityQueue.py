import heapq
class PriorityQueue:
    def __init__(self):
        self._queue = []
    def push(self, item):
        heapq.heappush(self._queue,item)
    def pop(self):
        return heapq.heappop(self._queue)
    def isEmpty(self):
        return len(self._queue)==0
    def __str__(self):
        return " ".join([str(i) for i in self._queue])
if __name__ == '__main__':
    p = PriorityQueue()
    p.push([12,"a"])
    p.push([1,"b"])
    p.push([14,"c"])
    p.push([7,"d"])
    p.push([8,"e"])
    p.push([2,"f"])
    p.push([15,"g"])
    while not p.isEmpty():
        print(p)
        print(p.pop())
        print("--")


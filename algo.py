def aStarSearch(problem, heuristic=0):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    loc_pqueue = PriorityQueue()
    visited_node = {}
    parent_child_map = {}
    direction_list = [] 
    path_cost = 0
    heuristic_value = 0
       
    start_node = problem.getStartState()
    parent_child_map[start_node] = []
    loc_pqueue.push(start_node,heuristic_value)
        
    def traverse_path(parent_node):
        temp = 0
        while True:
            '''print parent_node'''
            map_row = parent_child_map[parent_node]
            if (len(map_row) == 4):
                parent_node = map_row[0]
                direction = map_row[1]
                gvalue = map_row[2]
                fvalue = map_row[3]
                direction_list.append(direction)
                '''print "Gvalue = %d" % gvalue
                print fvalue'''
                '''print "Hueristic = %d" % (fvalue-gvalue)'''
                '''print "Admissible H = %d" % temp'''
                temp = temp + 1
            else:
                break       
        return direction_list
        
    while (loc_pqueue.isEmpty() == False):
        
        parent_node = loc_pqueue.pop()
        
        if (parent_node != problem.getStartState()):
            path_cost = parent_child_map[parent_node][2]
                
        if (problem.isGoalState(parent_node)):
            pathlist = traverse_path(parent_node)
            pathlist.reverse()
            return pathlist
        
        elif (visited_node.has_key(parent_node) == False):
            visited_node[parent_node] = []            
            sucessor_list = problem.getSuccessors(parent_node)
            no_of_child = len(sucessor_list)
            if (no_of_child > 0):          
                temp = 0
                while (temp < no_of_child):
                    child_nodes = sucessor_list[temp]
                    child_state = child_nodes[0];
                    child_action = child_nodes[1];
                    child_cost = child_nodes[2];
                    
                    heuristic_value = heuristic(child_state, problem)
                    gvalue = path_cost + child_cost
                    fvalue = gvalue + heuristic_value
                    
                    if (visited_node.has_key(child_state) == False):
                        loc_pqueue.push(child_state,fvalue)
                    if (parent_child_map.has_key(child_state) == False):
                        parent_child_map[child_state] = [parent_node,child_action,gvalue,fvalue]
                    else:
                        if (child_state != start_node):
                            stored_fvalue = parent_child_map[child_state][3]
                            if (stored_fvalue > fvalue):
                                parent_child_map[child_state] = [parent_node,child_action,gvalue,fvalue]
                    temp = temp + 1

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0
    
    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
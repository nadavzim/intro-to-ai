##################################################################################################
# nadav zimmerman and ynon hayun exe 1 of intro to AI.                                           #
##################################################################################################

import state

# implements a priority queue that works with ID
# every element in the queue has 2 items: 1.the state
#                                        2.its depth in the search tree
insert_count = 1
remove_count = 0
init_state = None  # The initial state.
threshold = 0  #
# current_depth = 0 # The depth of the last removed state
MAX = 100
nextThreshold = MAX + 1


def create(s):
    global init_state
    global threshold
    init_state = s
    threshold = val(s)
    return [s]


def is_empty(f):
    """
        Checks if the frontier (priority queue) is empty.
        - Returns True if the frontier is empty, otherwise returns False.
    """
    return len(f) == 0


def insert(f, s):
    # inserts state s to the frontier
    global threshold
    global nextThreshold
    global insert_count
    if val(s) <= threshold:
        insert_count += 1
        f.append(s)
        i = len(f) - 1
        while i > 0 and val(f[i]) < val(f[(i - 1) // 2]):
            t = f[i]
            f[i] = f[(i - 1) // 2]
            f[(i - 1) // 2] = t
            i = (i - 1) // 2
    else:
        nextThreshold = min(nextThreshold, val(s))


##################################################################################################
# nadav zimmerman and ynon hayun exe 1 of intro to AI.                                           #
##################################################################################################
def removeAndUpdate(f):
    """
        Removes the state with the highest priority (the lowest value) from the frontier, and updates the threshold and
         the remove's counter
        - Increases the global remove count.
        - Increases the threshold  to include more states in the future.
        - Removes the root element (state with the highest priority) and maintains the heap.
        - Returns the removed state.
    """
    global remove_count, threshold, nextThreshold
    s = f[0]
    remove_count += 1
    f[0] = f[-1]
    del f[-1]
    heapify(f, 0)
    if is_empty(f):
        threshold = nextThreshold
        nextThreshold += val(s)
    return s


def val(s):
    return state.hdistance(s) + state.path_len(s)


def heapify(f, i):
    minSon = i
    if 2 * i + 1 < len(f) and val(f[2 * i + 1]) < val(f[minSon]):
        minSon = 2 * i + 1
    if 2 * i + 2 < len(f) and val(f[2 * i + 2]) < val(f[minSon]):
        minSon = 2 * i + 2
    if minSon != i:
        t = f[minSon]
        f[minSon] = f[i]
        f[i] = t
        heapify(f, minSon)




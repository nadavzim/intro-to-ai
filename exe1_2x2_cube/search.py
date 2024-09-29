#search
import state
import frontier

def search(n = None):
    s= state.create(n)
    print(s)
    f= frontier.create(s)
    while not frontier.is_empty(f):
        s= frontier.removeAndUpdate(f)
        if state.is_target(s):
            return s
        ns= state.get_next(s)
        for i in ns:
            frontier.insert(f, i)
    return 0


print (search())
print ("inserts: ", frontier.insert_count)
print ("removes: ", frontier.remove_count)

"""
moves = '15344502000105324040'+'150413'
s = ["R", "R", "R", "R", "G", "G", "B", "B", "Y", "Y", "G", "G",
     "B", "B", "Y", "Y", "W", "W", "W", "W", "O", "O", "O", "O"]
print(s)
for m in moves:
    s = state.make_move(s, state.MOVES[int(m)])
    print(s)
"""

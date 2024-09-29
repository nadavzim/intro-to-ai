LEFT = 0
ROOT = 1
RIGHT = 2

'''
Reads file fname to the list ds.
Each line in the file contains comma seperated numbers (the attributes)
and the class (the last value in the line.)
'''
def readDataset(fname):
    f = open(fname, "r")
    ds = []
    s = f.readline()
    while s != "":
        ds += [[]]
        s=s.split(",")
        for i in s[:-1]:
            ds[-1] += [float(i)]
        ds[-1] += [s[-1]]
        s = f.readline()
    return ds

'''
returns a list of all the classes in the dataset.
'''
def classes(ds):
    cls = []
    for i in ds:
        if not(i[-1] in cls):
            cls += [i[-1]]
    return cls

'''
Returns the gini criterion of ds[start...mid] and ds[mid+1...end-1]
'''
def gini(ds, classes, mid):
    left_classes_count = [0] * len(classes)
    right_classes_count = [0] * len(classes)

    for i in range(mid + 1):
        left_classes_count[classes.index(ds[i][-1])] += 1

    for i in range(mid + 1, len(ds)):
        right_classes_count[classes.index(ds[i][-1])] += 1

    left_gini = 1.0 - sum((count / (mid + 1)) ** 2 for count in left_classes_count if count != 0)
    right_gini = 1.0 - sum((count / (len(ds) - mid - 1)) ** 2 for count in right_classes_count if count != 0)

    gini_index = (mid + 1) / len(ds) * left_gini + (len(ds) - mid - 1) / len(ds) * right_gini

    return gini_index



def chooseSplit(ds, classes):
    best_gini = 1.0
    best_attribute = 0
    best_value = ds[0][0]

    for attribute in range(len(ds[0]) - 1):
        sorted_ds = sorted(ds, key=lambda x: x[attribute])
        for i in range(len(sorted_ds) - 1):
            mid = (sorted_ds[i][attribute] + sorted_ds[i + 1][attribute]) / 2
            current_gini = gini(sorted_ds, classes, i)
            if current_gini < best_gini:
                best_gini = current_gini
                best_attribute = attribute
                best_value = mid

    return [best_attribute, best_value]


def majority(ds, classes):
    count = [0] * len(classes)
    for i in ds:
        count[classes.index(i[-1])] += 1
    return classes[count.index(max(count))]


'''
Returns True iff all instances id ds have the same class
'''


def allTheSameClass(ds):
    cls = ds[0][-1] 
    for i in ds:
        if i[-1] != cls:
            return False
    return True
        
'''
Builds the decision tree. A leaf has at most leafSize instances
'''
def buildTree(ds, classes, leafSize = 1):
    if allTheSameClass(ds) or len(ds) <= leafSize:
        return [majority(ds, classes)]

    best_split = chooseSplit(ds, classes)
    left_split = [x for x in ds if x[best_split[0]] <= best_split[1]]
    right_split = [x for x in ds if x[best_split[0]] > best_split[1]]

    left_subtree = buildTree(left_split, classes, leafSize)
    right_subtree = buildTree(right_split, classes, leafSize)

    return [left_subtree, best_split, right_subtree]


def buildClassifier(fname, leafSize = 1):
    ds = readDataset(fname)
    cls = classes(ds)
    return buildTree(ds, cls, leafSize)

def classify(dt, instance):
    if len(dt) == 1:
        return dt[0]
    if instance[dt[ROOT][0]] <= dt[ROOT][1]:
        return classify(dt[LEFT], instance)
    return classify(dt[RIGHT], instance)
    

dt = buildClassifier("iris-training.txt", 70)
print(dt)
ds = readDataset("iris-testing.txt")
c = 0
for i in ds:
    if classify(dt, i[:-1]) == i[-1]:
        c = c + 1
print(c)

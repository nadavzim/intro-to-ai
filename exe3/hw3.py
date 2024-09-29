##################################################################################################
# nadav zimmerman and ynon hayun exe 3 of intro to AI.                                           #
##################################################################################################


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
# Gini function to calculate the Gini index for a split dataset
# ds: dataset, classes: unique labels, mid: index for the split point
# left_classes_count and right_classes_count count the instances per class in left and right splits
def gini(ds, classes, mid):
    # Initialize count arrays for left and right splits
    left_classes_count = [0] * len(classes)
    right_classes_count = [0] * len(classes)

    # Count instances per class in the left split
    for i in range(mid + 1):
        left_classes_count[classes.index(ds[i][-1])] += 1

    # Count instances per class in the right split
    for i in range(mid + 1, len(ds)):
        right_classes_count[classes.index(ds[i][-1])] += 1

    # Calculate Gini index for the left split
    left_gini = 1.0 - sum((count / (mid + 1)) ** 2 for count in left_classes_count if count != 0)
    # Calculate Gini index for the right split
    right_gini = 1.0 - sum((count / (len(ds) - mid - 1)) ** 2 for count in right_classes_count if count != 0)

    # Weighted average of Gini indices for the two splits
    gini_index = (mid + 1) / len(ds) * left_gini + (len(ds) - mid - 1) / len(ds) * right_gini

    return gini_index

# chooseSplit function to find the best attribute and value to split on
# best_gini: stores the lowest Gini index found, best_attribute: stores the index of the best attribute
# best_value: stores the value at which the best split occurs
# For each attribute, sort the dataset and find the best split point based on Gini index
def chooseSplit(ds, classes):
    # Initialize best Gini index and corresponding attribute and value
    best_gini = 1.0
    best_attribute = 0
    best_value = ds[0][0]

    # Iterate over all attributes except the last column (labels)
    for attribute in range(len(ds[0]) - 1):
        # Sort dataset by the current attribute
        sorted_ds = sorted(ds, key=lambda x: x[attribute])
        # Test all potential split points for the current attribute
        for i in range(len(sorted_ds) - 1):
            # Calculate the midpoint for the current attribute's values
            mid = (sorted_ds[i][attribute] + sorted_ds[i + 1][attribute]) / 2
            # Calculate Gini index for this split
            current_gini = gini(sorted_ds, classes, i)
            # Update best Gini index and corresponding attribute and value if current Gini is better
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
# buildTree function to build the decision tree recursively
# ds: dataset, classes: unique labels, leafSize: minimum number of samples to create a leaf
# If all instances belong to the same class or the dataset size is less than or equal to leafSize, return the majority class
# Otherwise, find the best split and split the dataset into left and right subsets
# Recursively build the left and right subtrees
def buildTree(ds, classes, leafSize = 1):
    # Check if all instances have the same class or if dataset size is below the leaf size threshold
    if allTheSameClass(ds) or len(ds) <= leafSize:
        return [majority(ds, classes)]

    # Find the best attribute and value to split the data
    best_split = chooseSplit(ds, classes)
    # Split the dataset based on the best attribute and value
    left_split = [x for x in ds if x[best_split[0]] <= best_split[1]]
    right_split = [x for x in ds if x[best_split[0]] > best_split[1]]

    # Recursively build the left and right subtrees
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

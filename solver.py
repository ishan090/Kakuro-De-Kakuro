# A program that aims to solve kakuro puzzles
# As every empty cell in the kakuro grid has an index
# to locate it with, it must then belong to two
# Sequences




default_domain = [*range(1, 10)]


def make_min(length, domain):
    """assumes domain is sorted"""
    return sum(domain[:length-1])


def another(total, length, exclude=None):
    assert length != 0, "Hey! Length can't be zero ya"
    if exclude is None:
        exclude = []
    domain = [i for i in default_domain if i not in exclude]
    if length > len(domain):
        return False
    pos = []
    if length == 1:
        if total in domain:
            pos.append([total])
            return pos
        else:
            return False
    if total < make_min(length, domain):
        return False
    minimum = 10
    for i in domain:
        if i >= minimum:
            return pos
        other = another(total-i, length-1, exclude=exclude+[i])
        if not other:
            continue
        pos += [[i]+j for j in other]
        for j in other:
            if min(j) < minimum:
                minimum = min(j)
    return pos


print(another(45, 10))


class Kakuro:
    def __init__(self, maze=None, file=None) -> None:
        assert maze or file, "Must provide Maze or File"
    
    def parse(file):
        with open(file) as f:
            data = file.read()


class Sequence:
    def __init__(self, total, l, cell_of_cell=False, direction=True) -> None:
        """total's the vaue that all the elements in the list l
        should add up to"""
        self.total = total
        self.length = len(l)
        if not cell_of_cell:
            l = [None if (i == "_" or not i) else i for i in l]
        self.elements = l
        self.elems_are_cells = cell_of_cell
        self.direction = direction
        assert self.check_duplicacy(), "Elements of sequence"
        c = self.consistent()
        assert c, f"Input values {total}, {l} are in consistent"
    
    def check_duplicacy(self):
        elems = self.getElements()
        if self.elems_are_cells:
            elems = [i.getValue() for i in elems]
        present = []
        for i in elems:
            if i in present:
                return False
            if present is not None:
                present.append(i)
        return True
    
    def getTotal(self):
        return self.total
    
    def getLength(self):
        return self.length
    
    def getElements(self):
        return self.elements
    
    def consistent(self):
        known = [i for i in self.getElements() if not i.isEmpty()]
        known_sum = sum(known)
        posibilities = another(self.getTotal()-known_sum, self.getLength()-len(known), exclude=known)
        if not posibilities:
            return False
        domains = []
        for pos in posibilities:
            domains.append(known+pos)
        self.domains = domains
        return True
        

    
    def __str__(self) -> str:
        out = str(self.getTotal())+": "
        for i in self.getElements():
            out += str(i) + ", "
        return out[:-2]


class Cell:
    def __init__(self, n, s1, s2, domain=None) -> None:
        self.empty = n == "_" or not n
        if not self.empty:
            assert isinstance(n, int)
            assert n <= 9
            self.value = n
        else:
            self.value = None

        if not domain:
            domain = [*range(1, 10)]
        self.domain = domain
        # The sequences that this cell belongs to
        self.s1 = s1
        self.s2 = s2
    
    def isEmpty(self):
        return self.empty
    
    def getValue(self):
        return self.value
    
    def nodeConsistent(self):
        return len(self.domain) != 0
    
    def __str__(self) -> str:
        return self.value if not self.empty else "_"



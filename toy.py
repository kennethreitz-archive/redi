import redi

d = redi.value('haystack:metalist')

d.data = []
d.data.append(dict(blah='blah'))
d.data.append([1,2,3,4])

print d._raw
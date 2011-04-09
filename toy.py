import redi

lst = redi.list(('haystack', 'metalist'))

# lst.append({'x': 'y'})

# for l in lst:
    # print l

lst[0].update({'a':'b'})

print list(lst._raw)


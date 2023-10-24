tek_lines=[(1,0),(1,1)]
baz=[0]
new=[i for i in tek_lines if all(baz) in i].sort(key=lambda: x[i] for i in range(len(x)))
print(new)
print(1 in (1,0))




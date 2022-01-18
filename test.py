# from urllib.parse import urlencode
# data = {'telephone': 18729594835, "username": "jim"}
# print(urlencode(data))
# from pydantic import BaseModel
#
# class Person(BaseModel):
#     name: str
#     age: int = 10
#
# p = Person(name="jim")
# print(p.json(),type(p.json()))
# print(p.dict(),type(p.dict()))

d = {"name":"jim"}
c = {"age":11}
d.update(c)
print(d)

import os
print(os.getcwd(),type(os.getcwd()))
print(os.path.split(__file__))
os.popen(r'ls -la')
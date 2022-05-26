#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tosclib as tosc

root = tosc.load("../demos/files/test.tosc")
parent = tosc.ElementTOSC(root[0])

parent.createProperty("s", "CustomProperty", "1007")

print("Added Property:\n")
parent.showProperty("CustomProperty")

tosc.write(root, "../demos/files/out.tosc")


# In[2]:


box = tosc.ElementTOSC(parent.createNode("BOX"))

box.createProperty("c", "color", "", {
                     "r" : str(1),
                     "g" : str(1),
                     "b" : str(0),
                     "a" : "1"
                  })

print(box.__dict__)


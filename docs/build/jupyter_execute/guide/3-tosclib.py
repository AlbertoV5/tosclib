#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tosclib as tosc

root = tosc.load("../demos/files/test.tosc")
parent = tosc.e(root[0])
target = tosc.e(parent.findChild("target"))
target.showProperty("color")


# In[2]:


colors = {"r":"0", "g":"0", "b":"1", "a":"1"}
target.setPropertyValue("color", params = colors)
target.showProperty("color")


# In[3]:


tosc.write(root, "../demos/files/out.tosc")


# In[4]:


import tosclib as tosc
import argparse

root = tosc.load("../demos/files/test.tosc")
parent = tosc.ElementTOSC(root[0])

# Creating Property in parent Node
parent.createProperty(
                        type ="s",
                        key = "name",
                        text = "geoff"
                     )

print("Added Property: ")
parent.showProperty("name")
tosc.write(root, "../demos/files/out.tosc")


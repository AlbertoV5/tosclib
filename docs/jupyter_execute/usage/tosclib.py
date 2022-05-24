#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tosclib as tosc

root = tosc.load("demos/files/test.tosc")
parent = tosc.e(root[0])
target = tosc.e(parent.findChild("target"))
target.showProperty("color")


# In[2]:


colors = {"r":"0", "g":"0", "b":"1", "a":"1"}
target.setPropertyValue("color", params = colors)
target.showProperty("color")


# In[3]:


tosc.write(root, "demos/files/out.tosc")

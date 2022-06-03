local numValue = self.parent.parent.children.numvalue           
            
function onValueChanged(key)
    if (key == "x" and self.values.x == 1) then
        numValue:notify(self.parent.name)
    end
end
import maya.cmds as cmds
import json

        
def reset_animation(items):
    nurbs = cmds.ls(items, type="nurbsCurve")
    for nurb in nurbs:
        control = cmds.listRelatives(nurb, p=True) [0]
        attributes = cmds.listAttr(control, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            print(cmds.getAttr(f"{control}.{attr}"))
            if attr.startswith("translate") or attr.startswith("rotate"):
                cmds.setAttr(f"{control}.{attr}", 0)
            elif attr.startswith("scale"):
                cmds.setAttr(f"{control}.{attr}", 1)
                
        attributes = cmds.listAttr(control, keyable=True, userDefined=True)
        if attributes is None:
            continue
        for attr in attributes:
            dv = cmds.addAttr(f"{control}.{attr}", q=True, dv=True)
            cmds.setAttr(f"{control}.{attr}", dv)
            
            
def save_animation(items):
    data_to_save =[]    
    nurbs = cmds.ls(items, type="nurbsCurve")
    for nurb in nurbs:
        control = cmds.listRelatives(nurb, p=True) [0]
        attributes = cmds.listAttr(control, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            data_to_save.append(cmds.getAttr(f"{control}.{attr}"))
            
    save_data(data_to_save)
    
def save_data(entry):
    file_path = r'C:\Users\luigi\Desktop\Save.json'
    
    with open(file_path, "w") as file:
        json.dump(entry, file)
        
def load_animation(entry):
    file_path = r'C:\Users\luigi\Desktop\Save.json'
    
    with open(file_path, "r") as file:
        data = json.load(file)
    
    nurbs = cmds.ls(items, type="nurbsCurve")
    i = 0
    for nurb in nurbs:
        control = cmds.listRelatives(nurb, p=True) [0]
        attributes = cmds.listAttr(control, keyable=True)
        if attributes is None:
            continue
        
        for attr in attributes:           
            if attr.startswith("translate") or attr.startswith("rotate"):
                cmds.setAttr(f"{control}.{attr}", data[i])
            i+=1           
            
items = cmds.ls("*_ac_*", "*_fk_*")

if cmds.window(ui, q=True, ex=True):
    cmds.deleteUI(ui)

ui = cmds.window(ui)

cmds.columnLayout( adjustableColumn=True )
cmds.button(label='SAVE Animation', command= 'save_animation(items)')
cmds.button(label='LOAD Animation', command='load_animation(items)')
cmds.button(label='RESET Animation', command='reset_animation(items)')
cmds.button(label='Close', command='cmds.deleteUI(ui)')
cmds.setParent('..')
cmds.showWindow(ui)

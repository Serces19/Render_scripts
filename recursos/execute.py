import nuke

print('Iniciando execute.py')

########################################
# Accede a la raíz del proyecto
root_node = nuke.root()

# Obtén el primer y último fotograma
first_frame = int(root_node['first_frame'].value())
last_frame = int(root_node['last_frame'].value())
frame_range = last_frame - first_frame

print('last frame:', frame_range)

# Obtener el nombre del script
shot_name = nuke.tcl('regsub -all {_v[0-9]+} [file rootname [file tail [value root.name]]] ""')
print('shot name:', shot_name)

######################################
#Renderizar
node_name = "Write_version"
if nuke.exists(node_name):
    write_node = nuke.toNode(node_name)
    nuke.render(write_node, continueOnError = True)
else:
    print(f"El nodo {node_name} no existe")



#################
quit()
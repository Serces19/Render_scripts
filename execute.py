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


######################################

node_name = "Write_loco"
if nuke.exists(node_name):
    write_node = nuke.toNode(node_name)
    nuke.execute(write_node)
else:
    print(f"El nodo {node_name} no existe")


#################
quit()
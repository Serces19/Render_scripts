import re

cadena = "fgs .......... <<<<<..>M>>>>>>>>>>> El nodo 10 tiene un valor de 5.5"

patron = r"(El nodo.*)"

resultado = re.search(patron, cadena)

if resultado:
    nodo_completo = resultado.group(1).strip()
    print(nodo_completo)
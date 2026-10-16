#!/bin/bash

# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

echo "=========================================="
echo " Ejecutando Pruebas Unitarias - TecnoStock"
echo "=========================================="

# Asegurar que el directorio actual esté en el PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# Ejecutar el descubridor de pruebas de Python apuntando a la carpeta de tests
python3 -m unittest discover -s tests -p "test_*.py"

# Guardar el código de salida de las pruebas
RESULTADO=$?

echo "=========================================="
if [ $RESULTADO -eq 0 ]; then
    echo " ¡TODAS LAS PRUEBAS PASARON CON ÉXITO! 🎉"
else
    echo " ❌ ALGUNAS PRUEBAS FALLARON. REVISA EL LOG."
fi
echo "=========================================="

exit $RESULTADO
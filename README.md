# TecnoStock — Arquitectura de lógica de negocio (Unidad 3)

Repositorio de la actividad **Diseño arquitectural del sistema con IA** del curso *Componentes de Lógica de Negocio*. Continúa al **Caso 05: TecnoStock**  de la Unidad 2 (BRD y User Stories de TecnoStock, retail de electrónica)[cite: 1, 2, 30].

**Integrantes 👥  (Equipo 5):** 
* Rodrigo Noguera Pérez (`2136238`)
* Andrik Hasiel Pérez Limón (`2118898`)
* Erick Antonio Páez Estrada (`2120761`)[cite: 1]  
**Nombre del Profesor:** M.A Miguel Ángel Gómez Marroquín[cite: 1]

---

## 🎯 Alcance del Proyecto
El sistema aborda las vulnerabilidades operativas críticas de TecnoStock (fugas de mercancía, discrepancias entre inventario físico y de sistema, ventas accidentales de productos apartados y rastreo de números de serie). 

Los casos de uso arquitecturalmente significativos modelados son:
* **CU-01:** Venta directa y cobro (con validación de stock disponible y *rollback* transaccional ante pagos declinados).
* **CU-02:** Entrega con ticket QR y número de serie para asegurar la trazabilidad de la "Unidad Exacta".
* **CU-03:** Apartado con reserva temporal de 15 minutos, cálculo automático de anticipo del 20% y validación del límite de 5 artículos por cliente.
* **CU-04:** Vencimiento automático de apartado a los 30 días y conversión del anticipo a saldo a favor en el monedero electrónico.
* **CU-05:** Transferencia entre sucursales con máquina de estados, autorización obligatoria de Supervisor y manejo de discrepancias en tránsito.
---

## ⚙️ Decisiones Principales de Arquitectura (ADR)
* **ADR-01 (Domain Model):** Adoptado para todo el núcleo transaccional, encapsulando reglas complejas e interdependientes en entidades y *value objects* ricos.
* **ADR-02 (Unit of Work):** Implementado para garantizar atomicidad en operaciones compuestas (como apartados, cobros y transferencias), evitando estados intermedios corruptos en inventarios.
* **ADR-03 (CQRS Básico):** Aplicado exclusivamente en las consultas de alta concurrencia de disponibilidad global de stock para evitar bloqueos en las tablas transaccionales.
* **ADR-04 (Validación de Límite de Artículos):** Validación del límite de 5 artículos en el dominio coordinada con el conteo aportado por el servicio de aplicación dentro de la misma unidad de trabajo.
---
## 🏛️ Aggregates Principales del Dominio
El modelo se organiza en torno a 6 raíces de agregado con fronteras transaccionales estrictas:
1. **Venta** (líneas de venta, pagos con procesador abstracto y comprobante QR)
2. **Apartado** (reserva temporal, cálculo de anticipo y reglas de vigencia)
3. **Inventario** (control de stock por sucursal, existencias y unidades seriadas)
4. **Transferencia** (ciclo de estados y validación de autorización del Supervisor)
5. **Monedero** (gestión de saldos a favor por anticipos de apartados vencidos)
6. **Devolucion** (validación de plazos, comprobantes y condiciones de artículos)
---


## 📂 Estructura del Repositorio
docs/            Informe completo de arquitectura (Etapas 7 y 9), ADRs, matriz de trazabilidad y bitácora de IA
diagrams/        Archivos fuente (.drawio) y exportaciones visuales (PNG/PDF) de clases y secuencia
src/tecnostock/  Estructura por capas (Dominio, Aplicación e Infraestructura)
tests/           Validación de escenarios y reglas de negocio clave

*Nota de arquitectura: La dependencia apunta siempre hacia el centro del dominio (Infraestructura → Aplicación → Dominio).*

---
## 🔍 Guía de Evaluación y Revisión

Para facilitar la revisión de la arquitectura del **Equipo 5**, sugerimos seguir estos pasos:

1. **Documentación y Decisiones:** 
   Inicie revisando el Informe de Arquitectura principal y los registros de decisiones (ADRs) ubicados dentro del directorio `docs/`. Aquí se justifica la exclusión de devoluciones y el manejo de apartados/transferencias.

2. **Exploración de Modelos Visuales:** 
   Los diagramas de clases y de secuencia se encuentran en `diagrams/`. Si desea editar o visualizar los archivos fuente (Mermaid/PlantUML), puede importarlos en su editor de código o mediante la herramienta *draw.io* (opción *Insertar > Avanzado*).

3. **Validación de Reglas de Negocio (Testing):** 
   Nuestra lógica de dominio está blindada con pruebas automatizadas (requiere Python 3.9+, sin librerías de terceros). Para ejecutarlas y comprobar las invariantes del negocio, corra el siguiente script en la terminal desde la raíz del proyecto:
   ```bash
   ./run_tests.sh
---

## Supuestos pendientes
Se documentaron hallazgos clave pendientes de validación en la sección 9.4 del informe (como el momento exacto en que disminuye el inventario frente a la entrega física con número de serie, y el alcance operativo de las devoluciones)[cite: 1].
* `diagrams/`: Archivos fuente (`.drawio`) y exportaciones visuales de los diagramas de clases y de secuencia.
* `src/`: Estructura organizada por capas (Dominio, Aplicación e Infraestructura).
* `tests/`: Validación de escenarios y reglas de negocio clave.


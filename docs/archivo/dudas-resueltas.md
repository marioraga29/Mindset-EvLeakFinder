# Dudas resueltas (archivo)

Tabla movida desde `docs/01-notas-internas.md` §2 el 17-nov-2026. Las decisiones con su porqué siguen en §1 de las notas.

| ID | Resolución |
|---|---|
| P-01 | Mínimo duro del baseline: 2.000 manos |
| P-02 | Muestra recomendada: 10.000 manos; por debajo se avisa «muestra pequeña» |
| P-04 | Fuga neta: `max(0, (EVbb/100 baseline − EVbb/100 observado) × manos / 100)`; sin EV, «no estimable» |
| P-24 | Ventana T+30 por sesión (cualquier torneo), con pestañas por torneo en el visor, mínimo de manos igual a la mitad de la ventana, ventana de 0 manos sin alerta y rejilla sin resultado total (M07) |
| P-26 | Fatiga frente al stack (M10): se deja como trabajo futuro y se documenta como limitación; la gráfica no cambia |
| P-25 | Mínimo por métrica calculado con el baseline del jugador (½ de lo habitual, suelo de 3), tres estados de la ventana, FDR solo sobre lo evaluable y sensibilidad en la memoria hecha por el autor (M06) |
| P-23 | Profundidad de stack: cuatro tramos (menos de 10 BB, 10–20, 20–40 y 40 BB o más, provisionales), mínimo de 50 oportunidades con respaldo en el total del baseline y contraste exacto Poisson-binomial (M05) |
| P-06 | La pausa que separa dos sesiones es de 30 minutos |
| P-16 | Resuelta con las diapositivas 5 y 8 (K07): sin baseline no hay feed ni resumen; con baseline y sin lotes auditados, el feed explica que no hay casos y un panel «Baseline actual» sustituye al resumen |
| P-13 | El baseline inicial excluye las ventanas T+30 por trigger (K06); si no hay detecciones, no hay nada que avisar |

P-03 se queda fuera del MVP y no bloquea la entrega. Las dudas P-07 a P-17 son de interfaz y pertenecen a la especificación del Dashboard, no a 7.1.

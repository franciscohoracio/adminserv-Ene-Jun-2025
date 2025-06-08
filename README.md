# Prácticas básicas de Kubernetes con kind

Este repositorio contiene las guías y los manifiestos necesarios para realizar seis prácticas introductorias de Kubernetes utilizando [kind](https://kind.sigs.k8s.io/). Cada práctica está pensada para ejecutarse en un entorno local con Docker instalado.

## Requisitos previos

- Docker y [kind](https://kind.sigs.k8s.io/) instalados.
- `kubectl` configurado para usar el clúster de kind.

## Estructura del repositorio

| Archivo | Descripción |
|---------|-------------|
| `manifests/base/nginx-pod.yaml` | Manifiesto para crear un pod sencillo con Nginx. |
| `manifests/base/nginx-deployment.yaml` | Deployment con réplicas de Nginx. |
| `manifests/base/nginx-service.yaml` | Exposición del deployment mediante un `Service`. |
| `manifests/config/mensaje.txt` | Archivo de ejemplo usado para crear un ConfigMap. |
| `manifests/config/pod-con-configmap.yaml` | Pod que monta el ConfigMap anterior. |
| `manifests/storage/volumenes.yaml` | Ejemplo de `PersistentVolume`, `PersistentVolumeClaim` y pod. |
| `manifests/config/pod-secreto.yaml` | Pod que obtiene una variable de un Secret. |
| `manifests/base/nginx-probe.yaml` | Pod con probes de liveness y readiness. |
| `manifests/networking/ingress.yaml` | Ingress que expone el servicio de Nginx. |
| `manifests/storage/statefulset.yaml` | StatefulSet con almacenamiento persistente. |
| `manifests/jobs/job.yaml` | Job que ejecuta un comando y termina. |
| `manifests/jobs/cronjob.yaml` | CronJob programado periódicamente. |
| `manifests/networking/network-policy.yaml` | NetworkPolicy que limita el tráfico. |
| `manifests/autoscaling/hpa.yaml` | HPA para escalar el deployment. |
| `manifests/daemonset/daemonset.yaml` | DaemonSet que corre en todos los nodos. |
| `manifests/rbac/rbac.yaml` | Ejemplo de ServiceAccount y RBAC. |
## Organización de carpetas

Los manifiestos de Kubernetes se encuentran en la carpeta `manifests` organizados en varios subdirectorios:
- **base**: pods, deployments y services básicos.
- **config**: ConfigMaps y Secrets.
- **storage**: volúmenes persistentes y StatefulSets.
- **networking**: Ingress y NetworkPolicy.
- **jobs**: Jobs y CronJobs.
- **autoscaling**: escalado automático con HPA.
- **daemonset**: ejemplo de DaemonSet.
- **rbac**: recursos de autenticación y permisos.


## Práctica 1: Crear un clúster con kind y desplegar un Pod

### Objetivo
Configurar un clúster local con kind y desplegar un pod sencillo.

### Pasos
1. Crear el clúster:
   ```bash
   kind create cluster --name practicas-k8s
   ```
2. Verificar los nodos del clúster:
   ```bash
   kubectl get nodes
   ```
3. Crear el pod ejecutando:
   ```bash
   kubectl apply -f manifests/base/nginx-pod.yaml
   ```
4. Comprobar que el pod está en ejecución y ver los logs:
   ```bash
   kubectl get pods
   kubectl logs nginx
   ```
5. **Desafío**: cambia la imagen a `httpd` en el manifiesto y vuelve a crear el pod.

---

## Práctica 2: Deployment y Service

### Objetivo
Desplegar Nginx utilizando un Deployment y exponerlo mediante un Service de tipo NodePort.

### Pasos
1. Aplicar el deployment:
   ```bash
   kubectl apply -f manifests/base/nginx-deployment.yaml
   ```
2. Ver los pods creados:
   ```bash
   kubectl get pods -l app=nginx
   ```
3. Exponer el servicio:
   ```bash
   kubectl apply -f manifests/base/nginx-service.yaml
   ```
4. Probar accediendo en el navegador o con `curl`:
    ```bash
    curl http://localhost:30080
    ```
5. **Desafío**: escala el deployment a 5 réplicas y observa el balanceo de carga.

---

## Práctica 3: ConfigMaps y montado en pods

### Objetivo
Crear un ConfigMap a partir de un archivo y montarlo en un contenedor.

### Pasos
1. Generar el ConfigMap:
   ```bash
   kubectl create configmap mensaje-config --from-file=manifests/config/mensaje.txt
   ```
2. Crear el pod:
   ```bash
   kubectl apply -f manifests/config/pod-con-configmap.yaml
   ```
3. Verificar el contenido del ConfigMap dentro del contenedor:
   ```bash
   kubectl exec -it pod-con-configmap -- cat /config/mensaje.txt
   ```
4. **Desafío**: modifica `manifests/config/mensaje.txt`, vuelve a crear el ConfigMap y reinicia el pod.

---

## Práctica 4: Volúmenes persistentes

### Objetivo
Usar un volumen local para almacenar datos que sobrevivan a reinicios del pod.

### Pasos
1. Crear los recursos necesarios con el manifiesto `manifests/storage/volumenes.yaml`:
   ```bash
   kubectl apply -f manifests/storage/volumenes.yaml
   ```
2. Verificar que el archivo se ha creado en el volumen:
   ```bash
   kubectl exec -it pod-con-pv -- cat /data/hola.txt
   ```
3. Eliminar y volver a crear el pod para comprobar que el archivo persiste.
4. **Desafío**: monta el mismo volumen en otro pod para compartir datos.

---

## Práctica 5: Variables de entorno y secretos

### Objetivo
Crear un Secret y usarlo como variable de entorno en un contenedor.

### Pasos
1. Crear el Secret:
   ```bash
   kubectl create secret generic mi-secreto --from-literal=CLAVE_API=12345
   ```
2. Desplegar el pod:
   ```bash
   kubectl apply -f manifests/config/pod-secreto.yaml
   ```
3. Comprobar el valor de la variable de entorno:
   ```bash
   kubectl exec -it pod-secreto -- env | grep CLAVE_API
   ```
4. **Desafío**: combina un ConfigMap y un Secret para pasar varias variables.

---

## Práctica 6: Health Checks (Probes)

### Objetivo
Definir readiness y liveness probes para un contenedor de Nginx.

### Pasos
1. Crear el pod con probes:
   ```bash
   kubectl apply -f manifests/base/nginx-probe.yaml
   ```
2. Consultar la descripción del pod y observar los eventos:
   ```bash
   kubectl describe pod nginx-con-probes
   ```
3. **Desafío**: modifica la `livenessProbe` para que falle y comprueba que el pod se reinicia.

---

## Práctica 7: Ingress básico

### Objetivo
Exponer el servicio Nginx mediante un recurso Ingress.

### Pasos
1. Asegúrate de haber creado el `nginx-service` de la práctica 2.
2. Aplica el manifiesto:
   ```bash
   kubectl apply -f manifests/networking/ingress.yaml
   ```
3. Añade en tu `/etc/hosts` la línea `127.0.0.1 local.example.com`.
4. Accede a `http://local.example.com` para comprobar la respuesta.
5. **Desafío**: agrega otra regla al Ingress para un host o ruta distinta.

---

## Práctica 8: StatefulSet con almacenamiento

### Objetivo
Desplegar un StatefulSet que mantenga datos persistentes.

### Pasos
1. Crear los recursos:
   ```bash
   kubectl apply -f manifests/storage/statefulset.yaml
   ```
2. Observa los PVC generados para cada réplica del StatefulSet.
3. Escribe un archivo en uno de los pods y verifica que persiste tras reiniciar dicho pod.
4. **Desafío**: escala el StatefulSet y revisa la creación de nuevos volúmenes.

---

## Práctica 9: Jobs

### Objetivo
Ejecutar un trabajo que finaliza una vez completada la tarea.

### Pasos
1. Crear el Job:
   ```bash
   kubectl apply -f manifests/jobs/job.yaml
   ```
2. Espera a que termine y revisa los logs con `kubectl logs job/fecha-job`.
3. **Desafío**: modifica el comando para que falle y observa el `backoffLimit`.

---

## Práctica 10: CronJobs

### Objetivo
Programar tareas periódicas dentro del clúster.

### Pasos
1. Desplegar el CronJob:
   ```bash
   kubectl apply -f manifests/jobs/cronjob.yaml
   ```
2. Esperar unos minutos y listar los Jobs creados.
3. **Desafío**: cambia la periodicidad a cada 5 minutos.

---

## Práctica 11: Network Policies

### Objetivo
Restringir el tráfico hacia los pods de Nginx.

### Pasos
1. Aplicar la política de red:
   ```bash
   kubectl apply -f manifests/networking/network-policy.yaml
   ```
2. Crea un pod `busybox` con la etiqueta `access=granted` e intenta acceder al servicio.
3. **Desafío**: prueba desde un pod sin la etiqueta y verifica que la conexión es rechazada.

---

## Práctica 12: Autoscaling con HPA

### Objetivo
Escalar el deployment de Nginx automáticamente según el uso de CPU.

### Pasos
1. Aplica el manifiesto del autoscaler:
   ```bash
   kubectl apply -f manifests/autoscaling/hpa.yaml
   ```
2. Genera carga para observar el aumento de réplicas.
3. **Desafío**: ajusta el valor de `averageUtilization` y analiza el comportamiento.

---

## Práctica 13: DaemonSets

### Objetivo
Ejecutar un contenedor en cada nodo del clúster.

### Pasos
1. Crear el DaemonSet:
   ```bash
   kubectl apply -f manifests/daemonset/daemonset.yaml
   ```
2. Comprueba que se creó un pod por nodo con `kubectl get pods -o wide`.
3. **Desafío**: agrega tolerations para que se ejecute también en nodos con taints.

---

## Práctica 14: ServiceAccounts y RBAC

### Objetivo
Crear una cuenta de servicio con permisos limitados para listar pods.

### Pasos
1. Desplegar los recursos:
   ```bash
   kubectl apply -f manifests/rbac/rbac.yaml
   ```
2. Usa esa cuenta para intentar listar los pods del namespace.
3. **Desafío**: extiende la `Role` para permitir la creación de pods y comprueba el cambio.

---

## Limpieza

Para eliminar el clúster de kind y todos los recursos creados:
```bash
kind delete cluster --name practicas-k8s
```

## Pruebas

Para ejecutar las pruebas automatizadas:
```bash
pytest
```

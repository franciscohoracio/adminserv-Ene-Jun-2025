# Prácticas básicas de Kubernetes con kind

Este repositorio contiene las guías y los manifiestos necesarios para realizar seis prácticas introductorias de Kubernetes utilizando [kind](https://kind.sigs.k8s.io/). Cada práctica está pensada para ejecutarse en un entorno local con Docker instalado.

## Requisitos previos

- Docker y [kind](https://kind.sigs.k8s.io/) instalados.
- `kubectl` configurado para usar el clúster de kind.

## Estructura del repositorio

| Archivo | Descripción |
|---------|-------------|
| `nginx-pod.yaml` | Manifiesto para crear un pod sencillo con Nginx. |
| `nginx-deployment.yaml` | Deployment con réplicas de Nginx. |
| `nginx-service.yaml` | Exposición del deployment mediante un `Service`. |
| `mensaje.txt` | Archivo de ejemplo usado para crear un ConfigMap. |
| `pod-con-configmap.yaml` | Pod que monta el ConfigMap anterior. |
| `volumenes.yaml` | Ejemplo de `PersistentVolume`, `PersistentVolumeClaim` y pod. |
| `pod-secreto.yaml` | Pod que obtiene una variable de un Secret. |
| `nginx-probe.yaml` | Pod con probes de liveness y readiness. |

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
   kubectl apply -f nginx-pod.yaml
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
   kubectl apply -f nginx-deployment.yaml
   ```
2. Ver los pods creados:
   ```bash
   kubectl get pods -l app=nginx
   ```
3. Exponer el servicio:
   ```bash
   kubectl apply -f nginx-service.yaml
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
   kubectl create configmap mensaje-config --from-file=mensaje.txt
   ```
2. Crear el pod:
   ```bash
   kubectl apply -f pod-con-configmap.yaml
   ```
3. Verificar el contenido del ConfigMap dentro del contenedor:
   ```bash
   kubectl exec -it pod-con-configmap -- cat /config/mensaje.txt
   ```
4. **Desafío**: modifica `mensaje.txt`, vuelve a crear el ConfigMap y reinicia el pod.

---

## Práctica 4: Volúmenes persistentes

### Objetivo
Usar un volumen local para almacenar datos que sobrevivan a reinicios del pod.

### Pasos
1. Crear los recursos necesarios con el manifiesto `volumenes.yaml`:
   ```bash
   kubectl apply -f volumenes.yaml
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
   kubectl apply -f pod-secreto.yaml
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
   kubectl apply -f nginx-probe.yaml
   ```
2. Consultar la descripción del pod y observar los eventos:
   ```bash
   kubectl describe pod nginx-con-probes
   ```
3. **Desafío**: modifica la `livenessProbe` para que falle y comprueba que el pod se reinicia.

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

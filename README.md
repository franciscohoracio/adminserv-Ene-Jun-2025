# Prácticas básicas de Kubernetes con kind

Estas prácticas están diseñadas para que los alumnos aprendan los conceptos fundamentales de Kubernetes utilizando kind (Kubernetes IN Docker).

---

## Práctica 1: Crear un clúster con kind y desplegar un Pod

### Objetivo

- Instalar y usar kind para levantar un clúster de Kubernetes local.
- Desplegar un pod básico usando un archivo YAML.

### Instrucciones

1. Crear el clúster:

   ```bash
   kind create cluster --name practicas-k8s
   ```

2. Verificar los nodos:

   ```bash
   kubectl get nodes
   ```

3. Crear el archivo `nginx-pod.yaml`:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: nginx
   spec:
     containers:
       - name: nginx
         image: nginx:latest
         ports:
           - containerPort: 80
   ```

4. Aplicar y verificar:
   ```bash
   kubectl apply -f nginx-pod.yaml
   kubectl get pods
   kubectl logs nginx
   ```

### Desafío opcional

- Cambiar la imagen del contenedor por `httpd` y probar nuevamente.

---

## Práctica 2: Deployment y Service

### Objetivo

- Crear un Deployment para manejar réplicas.
- Exponer el servicio usando NodePort.

### Instrucciones

1. Crear el archivo `nginx-deployment.yaml`:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-deploy
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: nginx
     template:
       metadata:
         labels:
           app: nginx
       spec:
         containers:
           - name: nginx
             image: nginx
             ports:
               - containerPort: 80
   ```

2. Aplicar el Deployment:

   ```bash
   kubectl apply -f nginx-deployment.yaml
   kubectl get pods -l app=nginx
   ```

3. Crear el archivo `nginx-service.yaml`:

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: nginx-service
   spec:
     type: NodePort
     selector:
       app: nginx
     ports:
       - port: 80
         targetPort: 80
         nodePort: 30080
   ```

4. Aplicar el Service y probar:
   ```bash
   kubectl apply -f nginx-service.yaml
   kubectl port-forward services/nginx-service 8080:80
   curl http://localhost:8080
   ```

### Desafío opcional

- Aumentar el número de réplicas a 5 y verificar el balanceo de carga usando `watch curl`.

---

## Práctica 3: ConfigMaps y montado en pods

### Objetivo

- Crear un ConfigMap desde un archivo.
- Montarlo en un contenedor y visualizar su contenido.

### Instrucciones

1. Crear un archivo de configuración:

   ```bash
   echo "Bienvenido a Kubernetes" > mensaje.txt
   ```

2. Crear el ConfigMap:

   ```bash
   kubectl create configmap mensaje-config --from-file=mensaje.txt
   ```

3. Crear el archivo `pod-con-configmap.yaml`:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: pod-con-configmap
   spec:
     containers:
       - name: busybox
         image: busybox
         command: ["sleep", "3600"]
         volumeMounts:
           - name: mensaje-vol
             mountPath: "/config"
     volumes:
       - name: mensaje-vol
         configMap:
           name: mensaje-config
   ```

4. Aplicar y verificar:
   ```bash
   kubectl apply -f pod-con-configmap.yaml
   kubectl exec -it pod-con-configmap -- cat /config/mensaje.txt
   ```

### Desafío opcional

- Modificar el contenido del archivo, volver a crear el ConfigMap y reiniciar el pod.

---

## Práctica 4: Volúmenes Persistentes

### Objetivo
- Usar un volumen persistente local para guardar datos.
- Comprobar que los datos persisten aunque el pod se reinicie.

### Instrucciones
1. Crear un `PersistentVolume` y `PersistentVolumeClaim`:
   ```yaml
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: local-pv
   spec:
     capacity:
       storage: 1Gi
     accessModes:
       - ReadWriteOnce
     hostPath:
       path: "/tmp/kind-pv"
   ---
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: local-pvc
   spec:
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 1Gi
   ```

2. Crear un pod que use este volumen:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: pod-con-pv
   spec:
     containers:
     - name: busybox
       image: busybox
       command: [ "sh", "-c", "echo 'Hola desde PV' > /data/hola.txt && sleep 3600" ]
       volumeMounts:
       - mountPath: "/data"
         name: volumen-pv
     volumes:
     - name: volumen-pv
       persistentVolumeClaim:
         claimName: local-pvc
   ```

3. Aplicar todo y verificar:
   ```bash
   kubectl apply -f volumenes.yaml
   kubectl exec -it pod-con-pv -- cat /data/hola.txt
   ```

4. Eliminar el pod y volverlo a crear para comprobar persistencia.

### Desafío opcional
- Montar el volumen en otro pod para compartir los datos.

---

## Práctica 5: Variables de entorno y secretos

### Objetivo
- Crear un Secret y usarlo como variable de entorno en un pod.

### Instrucciones
1. Crear un Secret:
   ```bash
   kubectl create secret generic mi-secreto --from-literal=CLAVE_API=12345
   ```

2. Crear el pod:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: pod-secreto
   spec:
     containers:
     - name: alpine
       image: alpine
       command: ["sh", "-c", "env | grep CLAVE_API && sleep 3600"]
       env:
       - name: CLAVE_API
         valueFrom:
           secretKeyRef:
             name: mi-secreto
             key: CLAVE_API
   ```

3. Aplicar y verificar:
   ```bash
   kubectl apply -f pod-secreto.yaml
   kubectl exec -it pod-secreto -- env | grep CLAVE_API
   ```

### Desafío opcional
- Usar un ConfigMap y un Secret juntos para inyectar variables en el pod.

---

## Práctica 6: Health Checks (Probes)

### Objetivo
- Definir readiness y liveness probes para un contenedor.

### Instrucciones
1. Crear el archivo `nginx-probe.yaml`:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: nginx-con-probes
   spec:
     containers:
     - name: nginx
       image: nginx
       ports:
       - containerPort: 80
       readinessProbe:
         httpGet:
           path: /
           port: 80
         initialDelaySeconds: 5
         periodSeconds: 10
       livenessProbe:
         httpGet:
           path: /
           port: 80
         initialDelaySeconds: 15
         periodSeconds: 20
   ```

2. Aplicar y verificar:
   ```bash
   kubectl apply -f nginx-probe.yaml
   kubectl describe pod nginx-con-probes
   ```

### Desafío opcional
- Cambiar la `livenessProbe` para que apunte a una ruta inexistente y observar el reinicio del pod.

---

## Limpieza

Para eliminar el clúster:

```bash
kind delete cluster --name practicas-k8s

```

# Pedido App — Helm + ArgoCD + Jenkins (Python backend)


Sigue las instrucciones del documento previo. Este repositorio contiene el chart de Helm, definición de ArgoCD y pipeline de Jenkins.


2. Levantar Minikube
minikube start --driver=docker --memory=4096 --cpus=2
kubectl create namespace my-tech

🔹 3. Instalar ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml


Accede al dashboard de ArgoCD:

kubectl port-forward svc/argocd-server -n argocd 8080:443


👉 luego abre: https://localhost:8080

Usuario: admin
Password:

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

🔹 4. Preparar credenciales de la DB
kubectl create secret generic pedido-db-credentials \
  --from-literal=POSTGRES_USER=pedido_user \
  --from-literal=POSTGRES_PASSWORD=pedido_pass \
  -n my-tech

🔹 5. Probar manualmente con Helm

Clona el repo o descomprime el ZIP:

unzip pedido-app.zip
cd pedido-app/charts/pedido-app


Instala:

helm install pedido . -n my-tech


Comprueba:

kubectl get pods -n my-tech
kubectl get svc -n my-tech
kubectl get ingress -n my-tech

🔹 6. Integrar con ArgoCD

Dentro de pedido-app/environments/prod/application.yaml ya tienes la definición de la Application.
Aplica:

kubectl apply -f environments/prod/application.yaml -n argocd


ArgoCD sincronizará el chart automáticamente.

🔹 7. Exponer Ingress en Minikube

Habilita el addon:

minikube addons enable ingress


Obtén la IP:

minikube ip


Edita tu /etc/hosts:

<MINIKUBE_IP> pedido.example.com


Accede a:

http://pedido.example.com/api/

🔹 8. Probar CI/CD con Jenkins

Configura Jenkins con un pipeline multibranch o pipeline desde Jenkinsfile.

La pipeline (Jenkinsfile en el repo) construye la imagen Docker, la sube a tu registry y actualiza el values.yaml.

ArgoCD detecta el cambio en Git y sincroniza el cluster automáticamente.
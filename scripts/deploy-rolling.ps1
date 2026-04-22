param(
    [string]$Image,
    [string]$Namespace = "aceest",
    [string]$Deployment = "aceest-fitness",
    [string]$Container = "aceest-fitness"
)

if (-not $Image) {
    Write-Error "Use -Image dockerhub-user/aceest-fitness:tag"
    exit 1
}

kubectl set image deployment/$Deployment $Container=$Image -n $Namespace
kubectl rollout status deployment/$Deployment -n $Namespace

Write-Host "Rolling deployment complete: $Image"
param(
    [string]$Namespace = "aceest",
    [string]$Deployment = "aceest-fitness",
    [string]$Container = "aceest-fitness",
    [string]$Image
)

if (-not $Image) {
    Write-Error "Provide -Image <dockerhub-user/aceest-fitness:tag>"
    exit 1
}

kubectl set image deployment/$Deployment $Container=$Image -n $Namespace
kubectl rollout status deployment/$Deployment -n $Namespace

Write-Host "Deployment completed with image: $Image"

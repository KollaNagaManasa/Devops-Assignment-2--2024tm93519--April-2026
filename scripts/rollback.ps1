param(
    [string]$Namespace = "aceest",
    [string]$Deployment = "aceest-fitness"
)

kubectl rollout undo deployment/$Deployment -n $Namespace
kubectl rollout status deployment/$Deployment -n $Namespace

Write-Host "Rollback done for $Deployment in $Namespace"
param(
    [string]$Namespace = "aceest",
    [string]$Deployment = "aceest-fitness"
)

kubectl rollout undo deployment/$Deployment -n $Namespace
kubectl rollout status deployment/$Deployment -n $Namespace

Write-Host "Rollback executed for deployment: $Deployment"

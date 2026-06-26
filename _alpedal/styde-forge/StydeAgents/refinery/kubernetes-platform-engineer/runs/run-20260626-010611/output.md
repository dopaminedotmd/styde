design CRD for AppDeploy custom resource
group: styde.io/v1
kind: AppDeploy
spec:
  image: string
  replicas: int
  cluster: string
  mesh: istio|linkerd
  gitops: argocd|flux
status:
  phase: reconciling|ready|failed
  observedGeneration: int
  conditions: list
kubebuilder scaffold operator
operator/
  api/
    v1/
      appdeploy_types.go
      appdeploy_webhook.go
  controllers/
    appdeploy_controller.go
  main.go
reconciliation loop
watch AppDeploy resource
read spec.cluster to target fleet cluster
if spec.mesh==istio: inject sidecar annotation, create VirtualService
if spec.mesh==linkerd: set linkerd.io/inject: enabled, create ServiceProfile
generate ArgoCD Application pointing to cluster target
create or update Deployment + Service in target cluster via kubeconfig
report back status.phase and conditions
CRD design
appdeploy_types.go
type AppDeploySpec struct {
  Image    string `json:"image"`
  Replicas int32  `json:"replicas"`
  Cluster  string `json:"cluster"`
  Mesh     string `json:"mesh,omitempty"`
  GitOps   string `json:"gitops,omitempty"`
}
type AppDeployStatus struct {
  Phase               string      `json:"phase"`
  ObservedGeneration  int64       `json:"observedGeneration"`
  Conditions          []metav1.Condition `json:"conditions,omitempty"`
}
controller reconcile
func (r *AppDeployReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
  appDeploy := &stydev1.AppDeploy{}
  if err := r.Get(ctx, req.NamespacedName, appDeploy); err != nil {
    return ctrl.Result{}, client.IgnoreNotFound(err)
  }
  targetKubeconfig := r.fetchClusterKubeconfig(appDeploy.Spec.Cluster)
  targetClient := r.buildClient(targetKubeconfig)
  deploy := buildDeployment(appDeploy)
  if appDeploy.Spec.Mesh == "istio" {
    deploy.Annotations["sidecar.istio.io/inject"] = "true"
  }
  if appDeploy.Spec.Mesh == "linkerd" {
    deploy.Annotations["linkerd.io/inject"] = "enabled"
  }
  if _, err := controllerutil.CreateOrUpdate(ctx, targetClient, deploy, func() error {
    deploy.Spec.Replicas = &appDeploy.Spec.Replicas
    deploy.Spec.Template.Spec.Containers[0].Image = appDeploy.Spec.Image
    return nil
  }); err != nil {
    return ctrl.Result{}, err
  }
  if appDeploy.Spec.GitOps == "argocd" {
    argocdApp := buildArgoCDApplication(appDeploy)
    r.applyArgoCDApp(ctx, argocdApp)
  }
  appDeploy.Status.Phase = "ready"
  appDeploy.Status.ObservedGeneration = appDeploy.Generation
  r.Status().Update(ctx, appDeploy)
  return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
}
output AppDeploy manifest example
apiVersion: styde.io/v1
kind: AppDeploy
metadata:
  name: web-frontend
spec:
  image: nginx:1.25
  replicas: 3
  cluster: prod-eu-west-1
  mesh: istio
  gitops: argocd
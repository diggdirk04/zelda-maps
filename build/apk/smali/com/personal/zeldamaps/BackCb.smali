.class public Lcom/personal/zeldamaps/BackCb;
.super Ljava/lang/Object;
.implements Landroid/webkit/ValueCallback;

.field public a:Landroid/app/Activity;

.method public constructor <init>(Landroid/app/Activity;)V
    .registers 2
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput-object p1, p0, Lcom/personal/zeldamaps/BackCb;->a:Landroid/app/Activity;
    return-void
.end method

.method public onReceiveValue(Ljava/lang/Object;)V
    .registers 4
    :try_start
    const-string v0, "true"
    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v0
    if-eqz v0, :fallback
    return-void
    :fallback
    iget-object v0, p0, Lcom/personal/zeldamaps/BackCb;->a:Landroid/app/Activity;
    instance-of v1, v0, Lcom/personal/zeldamaps/MainActivity;
    if-eqz v1, :panel
    check-cast v0, Lcom/personal/zeldamaps/MainActivity;
    invoke-virtual {v0}, Lcom/personal/zeldamaps/MainActivity;->backFallback()V
    return-void
    :panel
    instance-of v1, v0, Lcom/personal/zeldamaps/PanelActivity;
    if-eqz v1, :end
    check-cast v0, Lcom/personal/zeldamaps/PanelActivity;
    invoke-virtual {v0}, Lcom/personal/zeldamaps/PanelActivity;->backFallback()V
    :end
    nop
    :try_end
    .catch Ljava/lang/Throwable; {:try_start .. :try_end} :catch
    :catch
    return-void
.end method

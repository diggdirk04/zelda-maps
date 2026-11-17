.class public Lcom/personal/zeldamaps/Runner;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;

.field public op:I

.method public constructor <init>(I)V
    .registers 2
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput p1, p0, Lcom/personal/zeldamaps/Runner;->op:I
    return-void
.end method

.method public run()V
    .registers 3
    :try_start
    iget v0, p0, Lcom/personal/zeldamaps/Runner;->op:I
    const/4 v1, 0x2
    if-ne v0, v1, :notback
    sget-object v1, Lcom/personal/zeldamaps/Dual;->mainAct:Landroid/app/Activity;
    if-eqz v1, :end
    invoke-virtual {v1}, Landroid/app/Activity;->onBackPressed()V
    goto :end
    :notback
    if-nez v0, :open
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->userClose()V
    goto :end
    :open
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->userOpen()V
    :end
    nop
    :try_end
    .catch Ljava/lang/Throwable; {:try_start .. :try_end} :catch
    :catch
    return-void
.end method

.class public Lcom/personal/zeldamaps/Bridge;
.super Ljava/lang/Object;

.field public side:I

.method public constructor <init>(I)V
    .registers 2
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput p1, p0, Lcom/personal/zeldamaps/Bridge;->side:I
    return-void
.end method

.method public send(Ljava/lang/String;)V
    .registers 3
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    :try_s
    iget v0, p0, Lcom/personal/zeldamaps/Bridge;->side:I
    invoke-static {v0, p1}, Lcom/personal/zeldamaps/Dual;->deliver(ILjava/lang/String;)V
    :try_s_end
    .catch Ljava/lang/Throwable; {:try_s .. :try_s_end} :catch_s
    :catch_s
    return-void
.end method

# Why the web view last died ("crash"/"kill"), or "" — read once, then cleared.
.method public lastCrash()Ljava/lang/String;
    .registers 5
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    const-string v3, ""
    :try_l
    sget-object v0, Lcom/personal/zeldamaps/Dual;->mainAct:Landroid/app/Activity;
    if-eqz v0, :l_done
    const-string v1, "zm"
    const/4 v2, 0x0
    invoke-virtual {v0, v1, v2}, Landroid/app/Activity;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;
    move-result-object v0
    const-string v1, "rg"
    const-string v2, ""
    invoke-interface {v0, v1, v2}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    move-result-object v3
    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;
    move-result-object v0
    invoke-interface {v0, v1}, Landroid/content/SharedPreferences$Editor;->remove(Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;
    move-result-object v0
    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->apply()V
    :l_done
    nop
    :try_l_end
    .catch Ljava/lang/Throwable; {:try_l .. :try_l_end} :catch_l
    :catch_l
    return-object v3
.end method

.method public role()Ljava/lang/String;
    .registers 3
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget v0, p0, Lcom/personal/zeldamaps/Bridge;->side:I
    if-eqz v0, :m
    const-string v1, "panel"
    return-object v1
    :m
    sget-object v1, Lcom/personal/zeldamaps/Dual;->panel:Landroid/webkit/WebView;
    if-eqz v1, :solo
    const-string v1, "main"
    return-object v1
    :solo
    const-string v1, "solo"
    return-object v1
.end method

.method public hasSecond()Z
    .registers 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->hasSecond()Z
    move-result v0
    return v0
.end method

.method public openPanel()V
    .registers 3
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    new-instance v0, Lcom/personal/zeldamaps/Runner;
    const/4 v1, 0x1
    invoke-direct {v0, v1}, Lcom/personal/zeldamaps/Runner;-><init>(I)V
    invoke-static {v0}, Lcom/personal/zeldamaps/Dual;->postMain(Ljava/lang/Runnable;)V
    return-void
.end method

.method public closePanel()V
    .registers 3
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    new-instance v0, Lcom/personal/zeldamaps/Runner;
    const/4 v1, 0x0
    invoke-direct {v0, v1}, Lcom/personal/zeldamaps/Runner;-><init>(I)V
    invoke-static {v0}, Lcom/personal/zeldamaps/Dual;->postMain(Ljava/lang/Runnable;)V
    return-void
.end method

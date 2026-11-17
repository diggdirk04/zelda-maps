.class public Lcom/personal/zeldamaps/Dual;
.super Ljava/lang/Object;

.field public static mainAct:Landroid/app/Activity;
.field public static main:Landroid/webkit/WebView;
.field public static panelAct:Landroid/app/Activity;
.field public static panel:Landroid/webkit/WebView;
.field public static want:Z

.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method

.method public static safeStart(Landroid/app/Activity;Landroid/webkit/WebView;)V
    .registers 3
    :try_start
    invoke-static {p0, p1}, Lcom/personal/zeldamaps/Dual;->start(Landroid/app/Activity;Landroid/webkit/WebView;)V
    :try_end
    .catch Ljava/lang/Throwable; {:try_start .. :try_end} :catch
    :catch
    return-void
.end method

.method public static start(Landroid/app/Activity;Landroid/webkit/WebView;)V
    .registers 5
    sput-object p0, Lcom/personal/zeldamaps/Dual;->mainAct:Landroid/app/Activity;
    sput-object p1, Lcom/personal/zeldamaps/Dual;->main:Landroid/webkit/WebView;
    new-instance v0, Lcom/personal/zeldamaps/Bridge;
    const/4 v1, 0x0
    invoke-direct {v0, v1}, Lcom/personal/zeldamaps/Bridge;-><init>(I)V
    const-string v1, "ZDual"
    invoke-virtual {p1, v0, v1}, Landroid/webkit/WebView;->addJavascriptInterface(Ljava/lang/Object;Ljava/lang/String;)V
    const/4 v1, 0x1
    sput-boolean v1, Lcom/personal/zeldamaps/Dual;->want:Z
    return-void
.end method

.method public static findSecond()I
    .registers 6
    sget-object v0, Lcom/personal/zeldamaps/Dual;->mainAct:Landroid/app/Activity;
    if-nez v0, :ok
    const/4 v1, -0x1
    return v1
    :ok
    const-string v1, "display"
    invoke-virtual {v0, v1}, Landroid/app/Activity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;
    move-result-object v1
    check-cast v1, Landroid/hardware/display/DisplayManager;
    invoke-virtual {v1}, Landroid/hardware/display/DisplayManager;->getDisplays()[Landroid/view/Display;
    move-result-object v1
    array-length v2, v1
    const/4 v3, 0x0
    :loop
    if-ge v3, v2, :none
    aget-object v4, v1, v3
    invoke-virtual {v4}, Landroid/view/Display;->getDisplayId()I
    move-result v5
    if-eqz v5, :next
    return v5
    :next
    add-int/lit8 v3, v3, 0x1
    goto :loop
    :none
    const/4 v1, -0x1
    return v1
.end method

.method public static hasSecond()Z
    .registers 2
    :try_start
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->findSecond()I
    move-result v0
    :try_end
    .catch Ljava/lang/Throwable; {:try_start .. :try_end} :catch
    if-ltz v0, :no
    const/4 v1, 0x1
    return v1
    :no
    const/4 v1, 0x0
    return v1
    :catch
    const/4 v1, 0x0
    return v1
.end method

.method public static openPanel()V
    .registers 5
    sget-object v0, Lcom/personal/zeldamaps/Dual;->panelAct:Landroid/app/Activity;
    if-eqz v0, :go
    return-void
    :go
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I
    const/16 v1, 0x1a
    if-ge v0, v1, :ok
    return-void
    :ok
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->findSecond()I
    move-result v0
    if-gez v0, :have
    return-void
    :have
    new-instance v1, Landroid/content/Intent;
    sget-object v2, Lcom/personal/zeldamaps/Dual;->mainAct:Landroid/app/Activity;
    const-class v3, Lcom/personal/zeldamaps/PanelActivity;
    invoke-direct {v1, v2, v3}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V
    const/high16 v3, 0x18000000
    invoke-virtual {v1, v3}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
    invoke-static {}, Landroid/app/ActivityOptions;->makeBasic()Landroid/app/ActivityOptions;
    move-result-object v3
    invoke-virtual {v3, v0}, Landroid/app/ActivityOptions;->setLaunchDisplayId(I)Landroid/app/ActivityOptions;
    invoke-virtual {v3}, Landroid/app/ActivityOptions;->toBundle()Landroid/os/Bundle;
    move-result-object v3
    invoke-virtual {v2, v1, v3}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;Landroid/os/Bundle;)V
    return-void
.end method

.method public static closePanel()V
    .registers 1
    sget-object v0, Lcom/personal/zeldamaps/Dual;->panelAct:Landroid/app/Activity;
    if-eqz v0, :done
    invoke-virtual {v0}, Landroid/app/Activity;->finish()V
    :done
    return-void
.end method

.method public static attachPanel(Landroid/app/Activity;Landroid/webkit/WebView;)V
    .registers 4
    sput-object p0, Lcom/personal/zeldamaps/Dual;->panelAct:Landroid/app/Activity;
    sput-object p1, Lcom/personal/zeldamaps/Dual;->panel:Landroid/webkit/WebView;
    new-instance v0, Lcom/personal/zeldamaps/Bridge;
    const/4 v1, 0x1
    invoke-direct {v0, v1}, Lcom/personal/zeldamaps/Bridge;-><init>(I)V
    const-string v1, "ZDual"
    invoke-virtual {p1, v0, v1}, Landroid/webkit/WebView;->addJavascriptInterface(Ljava/lang/Object;Ljava/lang/String;)V
    const-string v0, "window.zdRole&&zdRole('main')"
    invoke-static {v0}, Lcom/personal/zeldamaps/Dual;->toMain(Ljava/lang/String;)V
    return-void
.end method

.method public static detachPanel()V
    .registers 1
    const/4 v0, 0x0
    sput-object v0, Lcom/personal/zeldamaps/Dual;->panelAct:Landroid/app/Activity;
    sput-object v0, Lcom/personal/zeldamaps/Dual;->panel:Landroid/webkit/WebView;
    const-string v0, "window.zdRole&&zdRole('solo')"
    invoke-static {v0}, Lcom/personal/zeldamaps/Dual;->toMain(Ljava/lang/String;)V
    return-void
.end method

.method public static toMain(Ljava/lang/String;)V
    .registers 3
    sget-object v0, Lcom/personal/zeldamaps/Dual;->main:Landroid/webkit/WebView;
    if-eqz v0, :done
    new-instance v1, Lcom/personal/zeldamaps/Deliver;
    invoke-direct {v1, v0, p0}, Lcom/personal/zeldamaps/Deliver;-><init>(Landroid/webkit/WebView;Ljava/lang/String;)V
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->post(Ljava/lang/Runnable;)Z
    :done
    return-void
.end method

.method public static deliver(ILjava/lang/String;)V
    .registers 5
    if-nez p0, :tomain
    sget-object v0, Lcom/personal/zeldamaps/Dual;->panel:Landroid/webkit/WebView;
    goto :have
    :tomain
    sget-object v0, Lcom/personal/zeldamaps/Dual;->main:Landroid/webkit/WebView;
    :have
    if-eqz v0, :done
    new-instance v1, Ljava/lang/StringBuilder;
    const-string v2, "window.zdRecv&&zdRecv("
    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V
    invoke-static {p1}, Lorg/json/JSONObject;->quote(Ljava/lang/String;)Ljava/lang/String;
    move-result-object v2
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v2, ")"
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v2
    new-instance v1, Lcom/personal/zeldamaps/Deliver;
    invoke-direct {v1, v0, v2}, Lcom/personal/zeldamaps/Deliver;-><init>(Landroid/webkit/WebView;Ljava/lang/String;)V
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->post(Ljava/lang/Runnable;)Z
    :done
    return-void
.end method

.method public static postMain(Ljava/lang/Runnable;)V
    .registers 2
    sget-object v0, Lcom/personal/zeldamaps/Dual;->main:Landroid/webkit/WebView;
    if-eqz v0, :done
    invoke-virtual {v0, p0}, Landroid/webkit/WebView;->post(Ljava/lang/Runnable;)Z
    :done
    return-void
.end method

.method public static userOpen()V
    .registers 1
    const/4 v0, 0x1
    sput-boolean v0, Lcom/personal/zeldamaps/Dual;->want:Z
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->openPanel()V
    return-void
.end method

.method public static userClose()V
    .registers 1
    const/4 v0, 0x0
    sput-boolean v0, Lcom/personal/zeldamaps/Dual;->want:Z
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->closePanel()V
    return-void
.end method

.method public static noWant()V
    .registers 1
    const/4 v0, 0x0
    sput-boolean v0, Lcom/personal/zeldamaps/Dual;->want:Z
    return-void
.end method

.method public static onMainStart()V
    .registers 1
    sget-boolean v0, Lcom/personal/zeldamaps/Dual;->want:Z
    if-eqz v0, :done
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->openPanel()V
    :done
    return-void
.end method

.method public static onMainStop()V
    .registers 0
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->closePanel()V
    return-void
.end method

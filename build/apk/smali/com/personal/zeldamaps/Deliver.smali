.class public Lcom/personal/zeldamaps/Deliver;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;

.field public w:Landroid/webkit/WebView;
.field public s:Ljava/lang/String;

.method public constructor <init>(Landroid/webkit/WebView;Ljava/lang/String;)V
    .registers 3
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput-object p1, p0, Lcom/personal/zeldamaps/Deliver;->w:Landroid/webkit/WebView;
    iput-object p2, p0, Lcom/personal/zeldamaps/Deliver;->s:Ljava/lang/String;
    return-void
.end method

.method public run()V
    .registers 4
    :try_start
    iget-object v0, p0, Lcom/personal/zeldamaps/Deliver;->w:Landroid/webkit/WebView;
    iget-object v1, p0, Lcom/personal/zeldamaps/Deliver;->s:Ljava/lang/String;
    const/4 v2, 0x0
    invoke-virtual {v0, v1, v2}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V
    :try_end
    .catch Ljava/lang/Throwable; {:try_start .. :try_end} :catch
    :catch
    return-void
.end method

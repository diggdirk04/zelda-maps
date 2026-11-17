.class public Lcom/personal/zeldamaps/ExtClient;
.super Landroid/webkit/WebViewClient;

.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Landroid/webkit/WebViewClient;-><init>()V
    return-void
.end method

.method public shouldOverrideUrlLoading(Landroid/webkit/WebView;Landroid/webkit/WebResourceRequest;)Z
    .registers 7
    :try_start
    invoke-interface {p2}, Landroid/webkit/WebResourceRequest;->getUrl()Landroid/net/Uri;
    move-result-object v0
    invoke-virtual {v0}, Landroid/net/Uri;->getScheme()Ljava/lang/String;
    move-result-object v1
    if-eqz v1, :no
    const-string v2, "http"
    invoke-virtual {v1, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z
    move-result v2
    if-eqz v2, :no
    new-instance v2, Landroid/content/Intent;
    const-string v3, "android.intent.action.VIEW"
    invoke-direct {v2, v3, v0}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V
    const/high16 v3, 0x10000000
    invoke-virtual {v2, v3}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
    invoke-virtual {p1}, Landroid/webkit/WebView;->getContext()Landroid/content/Context;
    move-result-object v3
    invoke-virtual {v3, v2}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V
    const/4 v0, 0x1
    return v0
    :no
    nop
    :try_end
    .catch Ljava/lang/Throwable; {:try_start .. :try_end} :catch
    :catch
    const/4 v0, 0x0
    return v0
.end method

# Renderer died (crash or killed for memory): detach + destroy the dead WebView, note why, then rebuild the activity.
.method public onRenderProcessGone(Landroid/webkit/WebView;Landroid/webkit/RenderProcessGoneDetail;)Z
    .registers 7
    const-string v4, "kill"
    :try_a
    invoke-virtual {p2}, Landroid/webkit/RenderProcessGoneDetail;->didCrash()Z
    move-result v0
    if-eqz v0, :a_done
    const-string v4, "crash"
    :a_done
    nop
    :try_a_end
    .catch Ljava/lang/Throwable; {:try_a .. :try_a_end} :catch_a
    :catch_a
    const/4 v3, 0x0
    :try_b
    invoke-virtual {p1}, Landroid/webkit/WebView;->getContext()Landroid/content/Context;
    move-result-object v3
    invoke-virtual {p1}, Landroid/webkit/WebView;->getParent()Landroid/view/ViewParent;
    move-result-object v0
    instance-of v1, v0, Landroid/view/ViewGroup;
    if-eqz v1, :b_noparent
    check-cast v0, Landroid/view/ViewGroup;
    invoke-virtual {v0, p1}, Landroid/view/ViewGroup;->removeView(Landroid/view/View;)V
    :b_noparent
    invoke-virtual {p1}, Landroid/webkit/WebView;->destroy()V
    :try_b_end
    .catch Ljava/lang/Throwable; {:try_b .. :try_b_end} :catch_b
    :catch_b
    :try_c
    instance-of v1, v3, Landroid/app/Activity;
    if-eqz v1, :c_done
    check-cast v3, Landroid/app/Activity;
    const-string v0, "zm"
    const/4 v1, 0x0
    invoke-virtual {v3, v0, v1}, Landroid/app/Activity;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;
    move-result-object v0
    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;
    move-result-object v0
    const-string v1, "rg"
    invoke-interface {v0, v1, v4}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;
    move-result-object v0
    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->commit()Z
    invoke-virtual {v3}, Landroid/app/Activity;->recreate()V
    :c_done
    nop
    :try_c_end
    .catch Ljava/lang/Throwable; {:try_c .. :try_c_end} :catch_c
    :catch_c
    const/4 v0, 0x1
    return v0
.end method

.class public Lcom/personal/zeldamaps/PanelActivity;
.super Landroid/app/Activity;

.field private web:Landroid/webkit/WebView;

.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .registers 6
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
    new-instance v0, Landroid/webkit/WebView;
    invoke-direct {v0, p0}, Landroid/webkit/WebView;-><init>(Landroid/content/Context;)V
    iput-object v0, p0, Lcom/personal/zeldamaps/PanelActivity;->web:Landroid/webkit/WebView;
    invoke-virtual {v0}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;
    move-result-object v1
    const/4 v2, 0x1
    const/4 v3, 0x0
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setDomStorageEnabled(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setAllowFileAccess(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setAllowFileAccessFromFileURLs(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setBuiltInZoomControls(Z)V
    invoke-virtual {v1, v3}, Landroid/webkit/WebSettings;->setDisplayZoomControls(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setLoadWithOverviewMode(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setUseWideViewPort(Z)V
    new-instance v1, Lcom/personal/zeldamaps/ExtClient;
    invoke-direct {v1}, Lcom/personal/zeldamaps/ExtClient;-><init>()V
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V
    invoke-virtual {p0, v0}, Lcom/personal/zeldamaps/PanelActivity;->setContentView(Landroid/view/View;)V
    :try_fh
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I
    const/16 v2, 0x1a
    if-lt v1, v2, :no_fh
    invoke-virtual {v0, v3}, Landroid/webkit/WebView;->setDefaultFocusHighlightEnabled(Z)V
    :no_fh
    nop
    :try_fh_end
    .catch Ljava/lang/Throwable; {:try_fh .. :try_fh_end} :catch_fh
    :catch_fh
    :try_dual
    invoke-static {p0, v0}, Lcom/personal/zeldamaps/Dual;->attachPanel(Landroid/app/Activity;Landroid/webkit/WebView;)V
    :try_dual_end
    .catch Ljava/lang/Throwable; {:try_dual .. :try_dual_end} :catch_dual
    :catch_dual
    const-string v1, "file:///android_asset/web/index.html"
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V
    return-void
.end method

.method public onBackPressed()V
    .registers 4
    :try_start_b
    iget-object v0, p0, Lcom/personal/zeldamaps/PanelActivity;->web:Landroid/webkit/WebView;
    new-instance v1, Lcom/personal/zeldamaps/BackCb;
    invoke-direct {v1, p0}, Lcom/personal/zeldamaps/BackCb;-><init>(Landroid/app/Activity;)V
    const-string v2, "!!(window.zdBack&&window.zdBack())"
    invoke-virtual {v0, v2, v1}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V
    return-void
    :try_end_b
    .catch Ljava/lang/Throwable; {:try_start_b .. :try_end_b} :catch_b
    :catch_b
    invoke-virtual {p0}, Lcom/personal/zeldamaps/PanelActivity;->backFallback()V
    return-void
.end method

.method public backFallback()V
    .registers 3
    # Back on the bottom screen with nothing of its own to close: act as back on the main screen
    # (its history is the real one) instead of closing the panel.
    :try_dm
    sget-object v0, Lcom/personal/zeldamaps/Dual;->mainAct:Landroid/app/Activity;
    if-eqz v0, :no_main
    new-instance v1, Lcom/personal/zeldamaps/Runner;
    const/4 v0, 0x2
    invoke-direct {v1, v0}, Lcom/personal/zeldamaps/Runner;-><init>(I)V
    invoke-static {v1}, Lcom/personal/zeldamaps/Dual;->postMain(Ljava/lang/Runnable;)V
    return-void
    :no_main
    nop
    :try_dm_end
    .catch Ljava/lang/Throwable; {:try_dm .. :try_dm_end} :catch_dm
    :catch_dm
    iget-object v0, p0, Lcom/personal/zeldamaps/PanelActivity;->web:Landroid/webkit/WebView;
    invoke-virtual {v0}, Landroid/webkit/WebView;->canGoBack()Z
    move-result v1
    if-eqz v1, :cond_super
    invoke-virtual {v0}, Landroid/webkit/WebView;->goBack()V
    return-void
    :cond_super
    :try_nw
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->noWant()V
    :try_nw_end
    .catch Ljava/lang/Throwable; {:try_nw .. :try_nw_end} :catch_nw
    :catch_nw
    invoke-super {p0}, Landroid/app/Activity;->onBackPressed()V
    return-void
.end method

.method protected onDestroy()V
    .registers 1
    :try_start
    invoke-static {}, Lcom/personal/zeldamaps/Dual;->detachPanel()V
    :try_end
    .catch Ljava/lang/Throwable; {:try_start .. :try_end} :catch
    :catch
    invoke-super {p0}, Landroid/app/Activity;->onDestroy()V
    return-void
.end method

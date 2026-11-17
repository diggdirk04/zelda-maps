// Zelda Maps desktop wrapper: opens the offline web app in its own window.
const { app, BrowserWindow, shell } = require('electron');
const path = require('path');
const fs = require('fs');

function webDir() {
  // Packaged builds keep the site in resources/web; during `npm start` it's ../web.
  const packaged = path.join(process.resourcesPath || '', 'web');
  return fs.existsSync(path.join(packaged, 'index.html')) ? packaged : path.join(__dirname, '..', 'web');
}

function createWindow() {
  const dir = webDir();
  const win = new BrowserWindow({
    width: 1400, height: 950, backgroundColor: '#14130f', title: 'Zelda Maps',
    icon: path.join(dir, 'appicons', 'icon-512.png'),
    autoHideMenuBar: true,
    webPreferences: { contextIsolation: true, nodeIntegration: false, sandbox: true }
  });
  win.loadFile(path.join(dir, 'index.html'));
  // Source links (wikis, guides) open in the normal browser, not inside the app.
  win.webContents.setWindowOpenHandler(({ url }) => { shell.openExternal(url); return { action: 'deny' }; });
  win.webContents.on('will-navigate', (e, url) => { if (!url.startsWith('file:')) { e.preventDefault(); shell.openExternal(url); } });
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });

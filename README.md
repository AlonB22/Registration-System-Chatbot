# Registration System Chatbot

Full-stack registration project with:
- React web client (`frontend/`)
- React Native (Expo) mobile client (`Mobile/`)
- Flask backend (`Backend/`) deployed on Azure
- Node.js toast microservice (`ToastServer/`) deployed on Azure

## GitHub Repo Description
`Full-stack registration system with React web/mobile clients, Flask + MongoDB auth backend, and an OpenAI-powered toast microservice deployed on Azure.`

## Live Services
- Backend: `https://regsys-backend-alonb.azurewebsites.net`
- Toast server: `https://regsys-toast-alonb.azurewebsites.net`
- Backend health: `https://regsys-backend-alonb.azurewebsites.net/health`
- Toast health: `https://regsys-toast-alonb.azurewebsites.net/health`

## Demo Videos
These are web and mobile app videos for demonstration.

GitHub may not preview larger `.mp4` files inline. Use these direct links:
- Web app demo (download/open): [web_app.mp4](https://github.com/AlonB22/Registration-System-Chatbot/blob/main/frontend/public/web_app.mp4?raw=1)
- Mobile app demo (download/open): [mobile_app.mp4](https://github.com/AlonB22/Registration-System-Chatbot/blob/main/frontend/public/mobile_app.mp4?raw=1)

## Quick Verification (No Local Backend Needed)

### 1) Toast service
```powershell
(Invoke-WebRequest -UseBasicParsing "https://regsys-toast-alonb.azurewebsites.net/health").Content
(Invoke-WebRequest -UseBasicParsing "https://regsys-toast-alonb.azurewebsites.net/api/registration-toast").Content
```

### 2) Register with required first/last name
```powershell
$base = "https://regsys-backend-alonb.azurewebsites.net"
$email = "review$(Get-Random)@test.com"
$body = @{ first_name="Alice"; last_name="Smith"; email=$email; password="12345678" } | ConvertTo-Json
(Invoke-WebRequest -UseBasicParsing "$base/register" -Method POST -ContentType "application/json" -Body $body).Content
```

### 3) Login and confirm toast comes through backend
```powershell
$loginBody = @{ email=$email; password="12345678" } | ConvertTo-Json
(Invoke-WebRequest -UseBasicParsing "$base/login" -Method POST -ContentType "application/json" -Body $loginBody).Content
```

Expected behavior:
- registration without names returns `400`
- registration with names returns `201`
- login returns `200`
- responses include a `toast` string

## Watch Chat Log File Changes (Azure Excel)

The chatbot writes conversation rows to:
- `/home/site/wwwroot/AB_Deliveries_Chatbot_Logs.xlsx`

Use these PowerShell commands to watch changes with your own eyes:

### 1) Set variables and Kudu auth
```powershell
$rg  = "rg-regsys"
$app = "regsys-backend-alonb"

$pub = az webapp deployment list-publishing-credentials -g $rg -n $app | ConvertFrom-Json
$pair = "$($pub.publishingUserName):$($pub.publishingPassword)"
$basic = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($pair))
$headers = @{ Authorization = "Basic $basic" }
```

### 2) Trigger a new chat row (with unique marker)
```powershell
$tag = "E2E-" + (Get-Date -Format "yyyyMMddHHmmss")
$body = @{
  message = "בדיקת לוג $tag. הטלפון שלי 0501234567. מספר מעקב AB12CD34EF"
  history = @()
  user = @{ first_name = "Alon"; last_name = "Ben"; email = "alon@test.com" }
} | ConvertTo-Json -Depth 6

(Invoke-WebRequest -UseBasicParsing "https://$app.azurewebsites.net/chat" -Method POST -ContentType "application/json" -Body $body).Content
$tag
```

### 3) Check file metadata (size + modified time)
```powershell
Invoke-RestMethod -Uri "https://$app.scm.azurewebsites.net/api/vfs/site/wwwroot/" -Headers $headers |
  Where-Object { $_.name -eq "AB_Deliveries_Chatbot_Logs.xlsx" } |
  Select-Object name, size, mtime
```

### 4) Download and open the file
```powershell
Invoke-WebRequest -Uri "https://$app.scm.azurewebsites.net/api/vfs/site/wwwroot/AB_Deliveries_Chatbot_Logs.xlsx" `
  -Headers $headers `
  -OutFile ".\AB_Deliveries_Chatbot_Logs_from_Azure.xlsx"

Start-Process ".\AB_Deliveries_Chatbot_Logs_from_Azure.xlsx"
```

### 5) Optional: watch continuously (every 10 seconds)
```powershell
while ($true) {
  Invoke-RestMethod -Uri "https://$app.scm.azurewebsites.net/api/vfs/site/wwwroot/" -Headers $headers |
    Where-Object { $_.name -eq "AB_Deliveries_Chatbot_Logs.xlsx" } |
    Select-Object name, size, mtime
  Start-Sleep -Seconds 10
}
```

If you get `404`, send one `/chat` message first, then check again.

## What To Review In Code
- Backend API routes: `Backend/app.py`
- Registration/login validation + Mongo insert: `Backend/services/user_service.py`
- Mongo connection config: `Backend/database.py`
- Toast generation service: `ToastServer/server.js`
- Web registration modal + validation: `frontend/src/App.jsx`
- Mobile registration payload + validation: `Mobile/app/(tabs)/index.tsx`

## Local Frontend/Mobile (Optional)

If you want to run only client apps against live Azure services:

```bash
cd frontend
npm install
npm run dev
```

```bash
cd Mobile
npm install
npm run start
```

The repo already includes Azure URLs in:
- `frontend/.env`
- `Mobile/.env`

## Notes
- Backend and ToastServer source code are included for transparency, but reviewers do not need to run them locally to validate functionality.
- Deployment details are documented in [DEPLOY_AZURE.md](./DEPLOY_AZURE.md).

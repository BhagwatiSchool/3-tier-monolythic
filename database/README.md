# 🗄️ Azure SQL Database Setup Guide

This folder contains all SQL scripts required to set up the Azure SQL Database for the Resource Management Dashboard.

---

## 📋 Files in This Folder

| File | Purpose |
|------|---------|
| `01_create_tables.sql` | Creates all database tables |
| `02_insert_default_data.sql` | Inserts default theme configuration |
| `03_create_admin_user.sql` | Creates default admin user |
| `04_sample_resources.sql` | Inserts sample resources (optional) |
| `backup_and_restore.sql` | Backup and restore commands |

---

## 🚀 Quick Setup (Step-by-Step)

### Step 1: Create Azure SQL Database

1. **Login to Azure Portal:** https://portal.azure.com
2. Search for **"SQL databases"**
3. Click **"+ Create"**
4. Fill in details:
   - **Resource Group:** Create new or select existing
   - **Database Name:** `resource-dashboard-db` (**CHANGE ACCORDINGLY**)
   - **Server:** Create new
     - **Server name:** `your-unique-server-name` (**CHANGE ACCORDINGLY**)
     - **Location:** Southeast Asia (or your preferred region)
     - **Authentication:** SQL authentication
     - **Admin login:** `dbadmin` (**CHANGE ACCORDINGLY**)
     - **Password:** Strong password (**CHANGE ACCORDINGLY** and SAVE IT!)
   - **Compute + Storage:** Basic or Standard tier
5. **Networking:**
   - ✅ Allow Azure services
   - ✅ Add current client IP
6. Click **"Review + Create"** > **"Create"**

⏱ **Wait:** 5-10 minutes for deployment

---

### Step 2: Get Connection String

1. Go to your database resource
2. Click **"Connection strings"** (left menu)
3. Copy the **ADO.NET** connection string
4. Note it down - you'll need it for `.env` configuration

**Format for PyMSSQL (Backend .env):**
```
mssql+pymssql://USERNAME:PASSWORD@SERVER_NAME.database.windows.net:1433/DATABASE_NAME
```

**Example (CHANGE ACCORDINGLY):**
```
mssql+pymssql://dbadmin:MySecure@Pass123@resource-server.database.windows.net:1433/resource-dashboard-db
```

---

### Step 3: Run SQL Scripts

#### Option A: Using Azure Portal Query Editor (Easiest)

1. Go to your database in Azure Portal
2. Click **"Query editor"** (left menu)
3. Login with:
   - **Authentication type:** SQL authentication
   - **Login:** `dbadmin` (or your admin username)
   - **Password:** Your database password
4. Run scripts in order:
   - Copy content of `01_create_tables.sql` → Paste → Click **"Run"**
   - Copy content of `02_insert_default_data.sql` → Paste → Click **"Run"**
   - Copy content of `03_create_admin_user.sql` → Paste → Click **"Run"**
   - (Optional) Copy content of `04_sample_resources.sql` → Paste → Click **"Run"**

✅ **Done!** Database is ready.

#### Option B: Using SQL Server Management Studio (SSMS)

1. Download SSMS: https://aka.ms/ssmsfullsetup
2. Connect to Azure SQL:
   - **Server name:** `your-server.database.windows.net`
   - **Authentication:** SQL Server Authentication
   - **Login:** Your admin username
   - **Password:** Your admin password
3. Open each `.sql` file and execute in order

#### Option C: Using Python Script (From Backend)

```bash
# Make sure backend .env is configured with DATABASE_URL
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run migration
python -c "from app.db.database import engine; from app.models.user import Base; Base.metadata.create_all(engine)"
```

---

### Step 4: Verify Tables

Run this query in Query Editor:

```sql
-- Check all tables
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE';
```

**Expected Output:**
- `users`
- `theme_config`
- `resources`

---

## 🔐 Default Admin User

After running `03_create_admin_user.sql`, you'll have:

- **Email:** `admin@example.com` (**CHANGE ACCORDINGLY** in the SQL file)
- **Password:** `Admin@123` (**CHANGE ACCORDINGLY** in the SQL file)
- **Role:** admin
- **Protected:** Yes (cannot be deleted)

⚠️ **IMPORTANT:** Change these credentials in production!

---

## 🔄 Backup and Restore

### Backup Database

**Azure Portal:**
1. Go to SQL database
2. Click **"Export"**
3. Choose storage account
4. Enter admin credentials
5. Click **"OK"**

**Automated Backups:**
Azure SQL automatically backs up databases. You can restore to any point in last 7-35 days.

### Restore Database

1. Go to SQL database
2. Click **"Restore"**
3. Select restore point
4. Enter new database name
5. Click **"OK"**

---

## 🔍 Troubleshooting

### Cannot connect to database

**Check:**
- ✅ Firewall rules include your IP
- ✅ Connection string is correct
- ✅ Username/password are correct
- ✅ Server name has `.database.windows.net`

**Add IP to Firewall:**
1. SQL Database > Networking
2. Add your current IP address
3. Save

### Query timeout

**Solution:**
- Increase connection timeout in connection string
- Check database tier (Basic might be slow)
- Upgrade to Standard tier

### Permission denied

**Check:**
- Using admin credentials?
- User has proper permissions?

---

## 📊 Database Schema

### Users Table
- Stores user accounts
- Includes authentication info
- Role-based access control

### Resources Table
- Infrastructure resources
- Performance metrics
- User ownership

### Theme Config Table
- User theme preferences
- Color schemes
- Dark/light mode settings

---

## 🔗 Connection String Examples

**Development (Local):**
```env
DATABASE_URL=sqlite:///./resource_dashboard.db
```

**Production (Azure SQL):**
```env
# CHANGE ACCORDINGLY with your actual credentials
DATABASE_URL=mssql+pymssql://dbadmin:YourPassword@your-server.database.windows.net:1433/resource-dashboard-db
```

---

## ✅ Final Checklist

- [ ] Azure SQL Database created
- [ ] Connection string copied
- [ ] All SQL scripts executed successfully
- [ ] Tables verified in Query Editor
- [ ] Default admin user created
- [ ] Backend `.env` updated with DATABASE_URL
- [ ] Firewall rules configured
- [ ] Test connection from backend

---

**Need Help?** Check the main README files or Azure SQL documentation!

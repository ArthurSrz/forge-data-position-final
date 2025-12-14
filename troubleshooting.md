# Troubleshooting Guide - La Forge à Data Position

## Issues Found and Solutions

### 1. NumPy Compatibility Issue with hydralit_components

**Problem**:
```
ModuleNotFoundError: No module named 'numpy.lib.arraysetops'
```

**Cause**: `hydralit_components` uses a deprecated import path that was removed in NumPy 2.x.

**Solution**: Downgrade NumPy to version 1.x:
```bash
pip install "numpy<2"
```

**Note**: This may cause conflicts with other packages requiring NumPy 2.x (like opencv-python). For this specific project, NumPy 1.x is required.

---

### 2. Missing Grist Database Tables

**Problem**:
```
Table not found "Form2"
```

**Cause**: The Grist document was missing the required tables (Form0, Form2).

**Solution**: Created the missing tables via Grist API:
- `Form2` - Master Data Position questions with columns: `profile_type`, `question`, `reponse`, `score`, `question_type`, `position`
- `Form0` - Custom user questions with columns: `profile_type`, `question`, `reponse`, `score`

---

### 3. Deprecated DataFrame.append() Method

**Problem**:
```
FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version.
```

**Cause**: pandas 2.0+ removed `DataFrame.append()` method.

**Solution**: Replace all occurrences with `pd.concat()`:
```python
# Before (deprecated)
df = df.append(new_row, ignore_index=True)

# After (correct)
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
```

**Files affected**: `Hello.py` (lines 251, 416, 491)

---

### 4. Hardcoded API Credentials

**Problem**: API keys and document IDs were hardcoded in source code, creating security risks.

**Solution**:
1. Created `.streamlit/secrets.toml` file:
```toml
[grist]
api_key = "your_api_key"
doc_id = "your_doc_id"
server = "https://docs.getgrist.com"
subdomain = "docs"
```

2. Updated code to use `st.secrets`:
```python
API_KEY = st.secrets["grist"]["api_key"]
DOC_ID = st.secrets["grist"]["doc_id"]
```

**Important**: Ensure `secrets.toml` is in `.gitignore` (already configured).

---

### 5. Duplicate Function Definitions

**Problem**: `add_answers_to_grist_table()` was defined twice in `gatherizer_tab()`.

**Solution**: Removed the duplicate definition, kept only one function at line 455.

---

### 6. Missing Error Handling for API Calls

**Problem**: API calls didn't check response status or handle errors, causing silent failures.

**Solution**:
1. Added `load_grist_table()` helper function with error handling
2. Updated `add_answers_to_grist_table()` to return `(success, message)` tuple
3. Added proper user feedback via `st.error()` for failed operations

---

### 7. Empty Records Causing Index Errors

**Problem**: Accessing `data['records'][0]` crashed when tables were empty.

**Solution**: Added guards before accessing record data:
```python
if not data.get('records'):
    st.warning("Aucune donnée disponible")
    return
```

---

## Running the Application

### Prerequisites
1. Python 3.11+ (tested with 3.13)
2. NumPy < 2.0
3. Configured `.streamlit/secrets.toml`

### Start Command
```bash
streamlit run Hello.py --server.headless true
```

### Required Environment
- Grist account with API access
- Tables Form0, Form2, Form3 in Grist document
- Network access to docs.getgrist.com

---

## Common Runtime Errors

### Port Already in Use
```bash
# Use a different port
streamlit run Hello.py --server.port 8502
```

### Missing Session State
If you see "Veuillez charger un data position", go to the "Qualification" tab first and load a Data Position before accessing other tabs.

---

---

### 8. Streamlit Cloud Secrets Configuration

**Problem**:
```
KeyError: 'st.secrets has no key "grist". Did you forget to add it to secrets.toml,
mount it to secret directory, or the app settings on Streamlit Cloud?
```

**Cause**: On Streamlit Community Cloud, secrets must be configured through the web interface, not via a local `secrets.toml` file.

**Solution**:
1. Go to your app on [Streamlit Community Cloud](https://share.streamlit.io/)
2. Click **"Manage app"** (bottom right corner)
3. Click **"Settings"** → **"Secrets"**
4. Paste the following configuration:

```toml
[grist]
api_key = "YOUR_GRIST_API_KEY"
doc_id = "YOUR_GRIST_DOC_ID"
server = "https://docs.getgrist.com"
subdomain = "docs"
```

5. Click **"Save"**
6. The app will automatically reboot

**Note**: Local development uses `.streamlit/secrets.toml`, but Streamlit Cloud requires secrets to be entered through the dashboard.

---

## Contact
For issues not covered here, check the GitHub repository or raise an issue.

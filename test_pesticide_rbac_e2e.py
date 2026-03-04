"""
SmartCropX — End-to-End Tests for Pesticide Recommendation + RBAC.
Runs against a live backend on http://localhost:8001.
"""
import sys, requests, json

BASE = "http://localhost:8001"
PASS = 0
FAIL = 0

def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name}  —  {detail}")


def register(full_name, email, password, role):
    r = requests.post(f"{BASE}/api/auth/register", json={
        "full_name": full_name, "email": email, "password": password, "role": role
    })
    if r.status_code == 201:
        return r.json()["access_token"]
    # already exists → login
    r2 = requests.post(f"{BASE}/api/auth/login", json={"email": email, "password": password})
    return r2.json()["access_token"]


print("\n══════════════════════════════════════════")
print("  SmartCropX E2E — Pesticide + RBAC Tests")
print("══════════════════════════════════════════\n")

# ── 0. Health check ──
r = requests.get(f"{BASE}/healthz")
test("Backend is healthy", r.status_code == 200)

# ── 1. Pesticide module health ──
print("\n— Pesticide Module —")
r = requests.get(f"{BASE}/api/pesticide/health")
test("Pesticide health endpoint", r.status_code == 200 and r.json()["status"] == "ok")

# ── 2. List diseases ──
r = requests.get(f"{BASE}/api/pesticide/diseases")
test("List diseases returns non-empty", r.status_code == 200 and len(r.json()["diseases"]) > 10, f"got {r.text[:100]}")

# ── 3. List crops ──
r = requests.get(f"{BASE}/api/pesticide/crops")
crops = r.json()["crops"]
test("List crops returns 5 crops", len(crops) == 5, f"got {crops}")

# ── 4. Recommend pesticide — known disease + crop ──
r = requests.post(f"{BASE}/api/pesticide/recommend", json={"disease": "Early Blight", "crop": "Tomato"})
d = r.json()
test("Known disease (Early Blight + Tomato) returns match",
     r.status_code == 200 and d["matched"] == True and "Mancozeb" in d["pesticide"],
     f"got {d}")

# ── 5. Recommend pesticide — known disease, no crop ──
r = requests.post(f"{BASE}/api/pesticide/recommend", json={"disease": "blast"})
d = r.json()
test("Disease without crop (blast) returns default",
     r.status_code == 200 and d["matched"] == True and "Tricyclazole" in d["pesticide"],
     f"got {d}")

# ── 6. Recommend pesticide — unknown disease ──
r = requests.post(f"{BASE}/api/pesticide/recommend", json={"disease": "xyz_nonexistent_disease"})
d = r.json()
test("Unknown disease returns graceful fallback (matched=false)",
     r.status_code == 200 and d["matched"] == False,
     f"got {d}")

# ── 7. Recommend pesticide — healthy ──
r = requests.post(f"{BASE}/api/pesticide/recommend", json={"disease": "healthy"})
d = r.json()
test("Healthy plant returns 'None required'",
     r.status_code == 200 and "None" in d["pesticide"],
     f"got {d}")

# ── 8. Recommend pesticide — Rice blast ──
r = requests.post(f"{BASE}/api/pesticide/recommend", json={"disease": "blast", "crop": "Rice"})
d = r.json()
test("Rice Blast returns crop-specific recommendation",
     r.status_code == 200 and d["crop"] == "Rice" and d["matched"] == True,
     f"got {d}")

# ═══════════════════════════════════════════
print("\n— RBAC Tests —")

# Register test users
farmer_token = register("Test Farmer", "test_farmer@e2e.test", "pass1234", "FARMER")
buyer_token = register("Test Buyer", "test_buyer@e2e.test", "pass1234", "BUYER")
admin_token = register("Test Admin", "test_admin@e2e.test", "pass1234", "ADMIN")

test("Register/login FARMER", farmer_token is not None)
test("Register/login BUYER", buyer_token is not None)
test("Register/login ADMIN", admin_token is not None)

# ── 9. FARMER can access prediction (via /market-predictions) ──
r = requests.get(f"{BASE}/market-predictions", headers={"Authorization": f"Bearer {farmer_token}"})
test("FARMER can access /market-predictions", r.status_code == 200, f"status={r.status_code}")

# ── 10. BUYER cannot access prediction ──
r = requests.get(f"{BASE}/market-predictions", headers={"Authorization": f"Bearer {buyer_token}"})
test("BUYER blocked from /market-predictions (403)", r.status_code == 403, f"status={r.status_code}")

# ── 11. Anonymous cannot access prediction ──
r = requests.get(f"{BASE}/market-predictions")
test("Anonymous blocked from /market-predictions (401/403)", r.status_code in (401, 403), f"status={r.status_code}")

# ── 12. ADMIN can access prediction ──
r = requests.get(f"{BASE}/market-predictions", headers={"Authorization": f"Bearer {admin_token}"})
test("ADMIN can access /market-predictions", r.status_code == 200, f"status={r.status_code}")

# ── 13. BUYER can access marketplace ──
r = requests.get(f"{BASE}/api/marketplace/access", headers={"Authorization": f"Bearer {buyer_token}"})
test("BUYER can access /api/marketplace/access", r.status_code == 200, f"status={r.status_code}")

# ── 14. FARMER cannot access marketplace ──
r = requests.get(f"{BASE}/api/marketplace/access", headers={"Authorization": f"Bearer {farmer_token}"})
test("FARMER blocked from /api/marketplace/access (403)", r.status_code == 403, f"status={r.status_code}")

# ── 15. ADMIN can access marketplace ──
r = requests.get(f"{BASE}/api/marketplace/access", headers={"Authorization": f"Bearer {admin_token}"})
test("ADMIN can access /api/marketplace/access", r.status_code == 200, f"status={r.status_code}")

# ── 16. Weather endpoint RBAC ──
r = requests.get(f"{BASE}/weather-forecast", headers={"Authorization": f"Bearer {farmer_token}"})
test("FARMER can access /weather-forecast", r.status_code == 200, f"status={r.status_code}")

r = requests.get(f"{BASE}/weather-forecast", headers={"Authorization": f"Bearer {buyer_token}"})
test("BUYER blocked from /weather-forecast (403)", r.status_code == 403, f"status={r.status_code}")

# ── 17. Community delete RBAC (ADMIN can delete any post) ──
# Create a post as FARMER
r = requests.post(f"{BASE}/api/community/posts",
    json={"title": "RBAC test post", "body": "This post tests RBAC delete", "tags": "test"},
    headers={"Authorization": f"Bearer {farmer_token}"})
if r.status_code == 201:
    post_id = r.json()["id"]
    # BUYER tries to delete → should fail (not owner, not admin)
    r2 = requests.delete(f"{BASE}/api/community/posts/{post_id}",
        headers={"Authorization": f"Bearer {buyer_token}"})
    test("BUYER cannot delete FARMER's post (403)", r2.status_code == 403, f"status={r2.status_code}")

    # ADMIN can delete → should succeed
    r3 = requests.delete(f"{BASE}/api/community/posts/{post_id}",
        headers={"Authorization": f"Bearer {admin_token}"})
    test("ADMIN can delete FARMER's post (200)", r3.status_code == 200, f"status={r3.status_code}")
else:
    test("Create test post for RBAC delete test", False, f"status={r.status_code}")

# ═══════════════════════════════════════════
print(f"\n══════════════════════════════════════════")
print(f"  Results: {PASS} passed, {FAIL} failed, {PASS+FAIL} total")
print(f"══════════════════════════════════════════\n")
sys.exit(0 if FAIL == 0 else 1)

# SmartCropX — Action Plan / Roadmap

> Generated: 2026-03-04  
> Scope: SRS compliance gaps + code-quality fixes

---

## 1. "ADD" Tasks — Missing Features

### TASK A-1: Pesticide Recommendation Module ✅ COMPLETED

**What:** The SRS requires a Pesticide Recommendation feature. Nothing exists today.

**Acceptance Criteria:**
- Backend endpoint `POST /api/recommend/pesticide` accepts a detected disease name (and optionally crop name) and returns top 3–5 pesticide recommendations with dosage, application method, safety precautions, and organic alternatives.
- Frontend page at `/pesticide-recommendation` with input field (disease/crop) and result cards.
- Navbar link added under "Recommend" or as a separate nav item.
- Works without external API — rule-based knowledge base.
- Integration: link from `PlantDiseaseDetection.jsx` — after disease is detected, show "Get Pesticide Recommendation" button that navigates to the pesticide page pre-filled with the detected disease.

**Implementation Plan:**

| Step | File(s) | Description |
|---|---|---|
| 1 | `backend/recommendation/pesticide_kb.py` (new) | Create pesticide knowledge base dictionary: ~15 diseases mapped to pesticide name, chemical class, dosage, application method, safety level, organic alternative |
| 2 | `backend/recommendation/schemas.py` (edit) | Add `PesticideInput` (disease: str, crop: Optional[str]) and `PesticideResponse` (recommendations list) Pydantic schemas |
| 3 | `backend/recommendation/routes.py` (edit) | Add `POST /api/recommend/pesticide` endpoint: lookup disease in KB, score/rank recommendations, return top 5 |
| 4 | `frontend/src/pages/PesticideRecommendation.jsx` (new) | Create page: disease input (text or dropdown), optional crop selector, submit button, result cards showing pesticide name, dosage, application, safety icon, organic badge |
| 5 | `frontend/src/App.js` (edit) | Add import + `<Route path="/pesticide-recommendation" ...>` |
| 6 | `frontend/src/pages/Header.jsx` (edit) | Add nav item or sub-menu under "Recommend" |
| 7 | `frontend/src/config/api.js` (edit) | Add `RECOMMEND_PESTICIDE` endpoint constant |
| 8 | `frontend/src/pages/PlantDiseaseDetection.jsx` (edit) | After disease detection result, add "Get Pesticide" button → navigates to `/pesticide-recommendation?disease={detected}` |
| 9 | Test | curl + UI verification |

**Estimated Complexity:** Medium (rule-based, no ML needed)

---

## 2. "UPDATE / FIX" Tasks — Partial / Broken Features

### TASK U-1: RBAC Enforcement ✅ COMPLETED

**What:** Roles (FARMER, BUYER, ADMIN) are defined in the DB and included in JWT tokens, but there is zero enforcement. Any logged-in user can do anything. The SRS requires RBAC.

**Acceptance Criteria:**
- Backend: `require_role("ADMIN")` dependency that raises 403 if user's role doesn't match.
- Community: only ADMIN can delete other users' posts/comments.
- Frontend: role-based UI — ADMIN sees moderation buttons; BUYER/FARMER see only their own edit/delete.
- Navbar shows role badge (e.g., "🛡 Admin").
- Optionally: ADMIN dashboard route `/admin` (stretch goal).

**Implementation Plan:**

| Step | File(s) | Description |
|---|---|---|
| 1 | `backend/community/auth.py` (edit) | Add `require_role(*allowed_roles)` FastAPI dependency that checks JWT `role` claim against allowed list; raises 403 Forbidden if mismatch |
| 2 | `backend/community/routes.py` (edit) | Update delete post/comment endpoints: allow owner OR ADMIN. Add explicit role check. |
| 3 | `frontend/src/context/AuthContext.js` (edit) | Expose `user.role` to components. Add `isAdmin`, `isFarmer`, `isBuyer` helpers. |
| 4 | `frontend/src/pages/Header.jsx` (edit) | Show role badge next to username. Conditionally show "Admin" menu item if role=ADMIN. |
| 5 | `frontend/src/pages/CommunityFeed.jsx` (edit) | Show delete buttons only for post owner or ADMIN. |
| 6 | `frontend/src/pages/PostDetail.jsx` (edit) | Same role-based delete/edit visibility. |
| 7 | Test | Register as FARMER → verify cannot delete others' posts. Register as ADMIN → verify can delete. |

**Estimated Complexity:** Medium

---

### TASK U-2: Blockchain "Future Scope" Labelling ⬛ MEDIUM PRIORITY

**What:** Blockchain features (StorageForm, Marketplace) exist but require Ganache, Truffle, MetaMask — which won't be running during a typical review. They fail silently or with console errors. The SRS does not require blockchain.

**Acceptance Criteria:**
- Blockchain pages still exist in code (don't delete) but are clearly marked as "Future Scope".
- A warning banner is shown on the blockchain pages: "This feature requires a local Ganache blockchain. See README for setup instructions."
- Dashboard cards linking to blockchain pages show a "Future Scope" badge.
- README.md mentions blockchain as future scope, not a core feature.

**Implementation Plan:**

| Step | File(s) | Description |
|---|---|---|
| 1 | `frontend/src/components/StorageForm.js` (edit) | Add a fallback UI banner when web3 is null: "Blockchain not connected — requires Ganache" |
| 2 | `frontend/src/components/Marketplace.js` (edit) | Same fallback banner |
| 3 | `frontend/src/pages/AgriDashboard.jsx` (edit) | Add "Future Scope" badge to Storage & Marketplace cards |
| 4 | `README.md` (edit) | Move blockchain section under "Future Scope" heading |

**Estimated Complexity:** Easy

---

## 3. "REMOVE / REFACTOR" Tasks

### TASK R-1: Clean Up Legacy / Unused Files ⬛ LOW PRIORITY

**What:** Several files in the repo are unused or test artifacts.

| File | Action | Reason |
|---|---|---|
| `backend/models/crop_demand_model.pkl` | Remove or archive | Not loaded by any endpoint |
| `backend/debug_api.py` | Remove | Dev-only debug file |
| `backend/render_deploy_test.py` | Remove | One-time deploy test |
| `backend/test_fallback_model.py` | Remove | One-time test script |
| `backend/test_models.py` | Remove | One-time test script |
| `backend/test_startup.py` | Remove | One-time test script |
| `backend/verify_start.py` | Remove | One-time startup check |
| `backend/main_minimal.py` | Remove | Minimal fallback not needed |
| `backend/backend.txt` | Remove | Stale text file |
| `backend/frotnedn.txt` | Remove | Typo filename, stale |
| `backend/lib.txt` | Remove | Stale |
| `backend/uploaded_image.jpg` | Remove | Test artifact |
| `backend/scripts/useless/` | Remove | Named "useless" |
| `backend/scripts/trial.py` | Remove | Trial/experiment script |
| `frontend/src/config/apiTest.js` | Keep (dev utility) | But exclude from build |

**Estimated Complexity:** Easy (file deletions)

---

### TASK R-2: Consolidate Multiple PlantDoc Models ⬛ LOW PRIORITY

**What:** There are 5 plantdoc `.keras` model files (~250 MB total). Only `plantdoc_optimized_v2.keras` is used as the primary model. The rest are fallbacks that were intermediate training outputs.

**Action:** Keep only `plantdoc_optimized_v2.keras` and `best_plantdoc_model.keras` (final fallback). Remove the other 3 to reduce repo/LFS size by ~150 MB.

**Estimated Complexity:** Easy

---

## Priority Summary

| Priority | Task ID | Title | Complexity |
|---|---|---|---|
| ✅ Done | A-1 | Add Pesticide Recommendation | Medium |
| ✅ Done | U-1 | RBAC Enforcement | Medium |
| 🟡 Medium | U-2 | Blockchain → Future Scope labelling | Easy |
| 🟢 Low | R-1 | Clean up unused files | Easy |
| 🟢 Low | R-2 | Consolidate plantdoc models | Easy |

---

## Implementation Order (Recommended)

```
Phase 1 (Critical — SRS compliance):  ✅ DONE
  1. A-1  Pesticide Recommendation     COMPLETED
  2. U-1  RBAC Enforcement              COMPLETED

Phase 2 (Polish — reviewer experience):
  3. U-2  Blockchain Future Scope label ~30 min
  4. R-1  Clean up unused files         ~15 min

Phase 3 (Optional):
  5. R-2  Consolidate models            ~10 min
```

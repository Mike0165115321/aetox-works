# 🗺️ Aetox Works — แผนพัฒนา (Roadmap)

> ระบบ AI Enterprise Workforce — LangGraph Supervisor-Worker
> Pipeline: Sales → Research → Content → Dev → Data

---

## ✅ Phase 0: Foundation

| Task | Status |
|:-----|:------:|
| โครงสร้างโปรเจค + venv | ✅ |
| LangGraph dependencies | ✅ |
| Supervisor-Worker Graph scaffold | ✅ |
| 4 Agent templates | ✅ |
| เอกสารไทยใน `docs/th/` | ✅ |
| GitHub: `Mike0165115321/aetox-works` | ✅ |

---

## ✅ Phase 1: LLM Integration (เสร็จ)

| Task | Status |
|:-----|:------:|
| `.env` + `config.py` | ✅ |
| LLM client (DeepSeek V4 Flash) | ✅ |
| LLM Router — classify intent เลือก agent | ✅ |
| Logging | ✅ |
| Tests (6 ผ่าน) | ✅ |

---

## ⏳ Phase 2-6: Agents

### 2. Sales Agent — Web Chat + Email (🚀 กำลังจะเริ่ม)

> เก็บโจทย์ลูกค้า, pain point, สรุป需求 → ส่ง Research

- [ ] **2.1** Web chat UI
- [ ] **2.2** Sales Agent prompt — personality + workflow
- [ ] **2.3** Gmail integration — ส่งอีเมลสรุปให้ลูกค้า
- [ ] **2.4** CRM พื้นฐาน (SQLite)
- [ ] **2.5** สรุป需求 → ส่งต่อไป Research Agent
- [ ] **2.6** Tests

### 3. Research Agent — ค้นหาข้อมูลตลาด

> หาข้อมูลตลาด, คู่แข่ง, keyword, insight (Firecrawl + Exa)

- [ ] **3.1** Research Agent prompt
- [ ] **3.2** Firecrawl integration (search + scrape)
- [ ] **3.3** Exa integration (semantic search)
- [ ] **3.4** สร้างรายงาน structured data → ส่ง Content Agent
- [ ] **3.5** Tests

### 4. Content Agent — เขียนคอนเทนต์

> เขียน copy, landing content, article, social post

- [ ] **4.1** Content Agent prompt
- [ ] **4.2** Blog/article generator
- [ ] **4.3** Landing page copy generator
- [ ] **4.4** Social media post generator
- [ ] **4.5** ส่งคอนเทนต์ → Dev Agent
- [ ] **4.6** Tests

### 5. Dev Agent — สร้างเว็บ

> สร้างเว็บ, feature, automation

- [ ] **5.1** Dev Agent prompt
- [ ] **5.2** HTML/CSS/JS generator จาก requirement
- [ ] **5.3** Local preview server
- [ ] **5.4** Deploy (GitHub Pages / server)
- [ ] **5.5** Human-in-the-loop approval
- [ ] **5.6** Tests

### 6. Data Agent — วัดผล

> วิเคราะห์ผลลัพธ์ lead/content/performance

- [ ] **6.1** Data Agent prompt
- [ ] **6.2** รองรับ CSV / JSON / logs
- [ ] **6.3** สร้างกราฟ + report (matplotlib)
- [ ] **6.4** Dashboard พื้นฐาน
- [ ] **6.5** สรุปผล → ส่งกลับลูกค้า
- [ ] **6.6** Tests

---

## Phase 7: Production — FastAPI Server & Deploy

- [ ] FastAPI endpoints
- [ ] Authentication
- [ ] LangSmith monitoring
- [ ] Human-in-the-loop
- [ ] Dockerize
- [ ] Deploy

---

## สถาปัตยกรรมปัจจุบัน

```
ลูกค้า
  │
  ▼
Sales → Research → Content → Dev → Data → ส่งมอบ
  │        │          │        │       │
  │   Firecrawl    DeepSeek   HTML   Matplotlib
  │   + Exa                  + Deploy
```

> **หมายเหตุ:** Phase 2-6 ทำตามลำดับ pipeline — Sales เสร็จก่อน แล้วต่อ Research -> Content -> Dev -> Data

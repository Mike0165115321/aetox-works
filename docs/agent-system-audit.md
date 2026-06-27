# Agent System Audit — 2026-06-28

## Summary

ตรวจระบบแบบสองชั้นตามแผน: unit/integration sandbox ก่อน แล้วตามด้วย live smoke ที่ใช้ DeepSeek จริง แต่ไม่ใช้ Firecrawl/Exa จริง
เพราะ key ภายนอกยังไม่ครบใน environment ปัจจุบัน

ผลรวม: agent graph ทำงานต่อกันครบ, Sales ไม่สร้าง notebook ซ้ำเมื่อส่ง context กลับมาถูกต้อง, Dev สร้างไฟล์ส่งมอบได้,
Data รวม final output พร้อมส่วนสิ่งที่ส่งมอบได้จริง และ test pollution ของ notebook ถูกอุดแล้ว

## Agent Verdict

| Area | Verdict | Evidence |
| --- | --- | --- |
| Personal Assistant / Supervisor | Pass | Pipeline route: Sales -> Research -> Content -> Dev -> Data -> Final; confirmation gate ยังบังคับอยู่ |
| Sales | Pass | Multi-turn ใช้ notebook เดิมผ่าน `[NB:...]`; confirmation lock notebook และสร้าง handoff brief |
| Research | Partial by design | Tool wiring ทำงาน แต่ live smoke ใช้ demo/mock search; output มี `source_mode=demo` เพื่อไม่หลอกว่าเป็น real research |
| Content | Pass | สร้าง draft ได้ และ mark `partial` ถ้า LLM/tool fail |
| Dev | Pass | สร้าง landing file ได้; metric `project_type` ถูกย้ายไป metadata ไม่เขียน string ลง metric numeric |
| Data | Pass | รวม lead/draft/project/report เป็น final output พร้อม deliverable list |
| Admin runtime graph | Pass | `/api/agents/status` มี node 7 ตัวและ edge ผ่าน Personal Assistant |

## Fixes Applied

- เพิ่ม `is_llm_failure()` และให้ agent mark failure/degraded output เป็น `partial` หรือ `error` แทนการถือว่า complete เงียบๆ
- Research output เพิ่ม `source_mode`, `web_source_mode`, `semantic_source_mode`, `warnings`, `llm_error`
- Dev build failure ถูกส่งออกเป็น `status=error`; metric logging ไม่กลืน error เงียบ และไม่บันทึก string ในช่อง numeric
- Dev API output เลิกเขียน hardcoded ไป `output/websites/...` และใช้ configured builder output directory เพื่อให้ test/live sandbox ครอบคลุม
- API logger setup เป็น idempotent แล้ว ป้องกัน `api.log` ซ้ำเมื่อ import/reload
- Test storage ถูก sandbox ผ่าน `tests/conftest.py` เพื่อไม่เขียน notebook/db/project ลง local app state จริง
- Sales confirmation output ชี้ notebook id/path จริง (`lead_<notebook_id>.md`) ไม่สับสนกับ CRM lead id
- Data final output แสดง pipeline จริงและ deliverables เช่น Lead ID, Draft ID, file path

## Cleanup

ลบ notebook artifact ใน `data/notebooks` จำนวน 34 ไฟล์ หลังยืนยันว่าเป็น test artifact ทั้งหมด:

- ไม่มีไฟล์ `confirmed`
- ไม่มี name/contact จริง
- เนื้อหาตรงกับ test input เช่น `help me`, `ช่วยทำเว็บหน่อยครับ`, `อยากเพิ่มยอดขาย`, `เพิ่มยอดขาย 50% ภายใน 3 เดือน`

หลัง cleanup และรัน test ซ้ำ `data/notebooks` ยังเหลือ 0 ไฟล์ แปลว่า test ไม่สร้าง notebook จริงกลับมาอีก

## Verification

- Unit/integration: `102 passed, 1 warning`
- Live smoke with DeepSeek: pass
- Live smoke result:
  - `sales_confirmed=true`
  - `notebook_count=1` ใน sandbox
  - `agents_used=["sales","research","content","dev","data"]`
  - `research_source_mode=demo`
  - `files_built_count=1`
  - final output มีส่วน `สิ่งที่ส่งมอบ`

## Remaining Risks

- Firecrawl/Exa key ยังไม่อยู่ใน environment จึงยังไม่ได้ยืนยัน real external research quality
- Local `AETOX_API_KEY` ยังไม่ตั้งค่า ถ้าเปิดใช้ production ควรเปิด auth
- Current final delivery มาจาก Data/Final aggregator โดยตรง; ถ้า product decision คือให้ Sales เป็นคนส่งงานปิดท้ายกับลูกค้า ต้องเพิ่ม final handoff กลับไป Sales ใน workflow รอบถัดไป
- Local DB อื่นยังมีข้อมูลเดิมอยู่ (`crm.db`, `content.db`, `metrics.db`, projects) รอบนี้ลบเฉพาะ notebook test artifact ตามกฎ cleanup ที่อนุมัติ

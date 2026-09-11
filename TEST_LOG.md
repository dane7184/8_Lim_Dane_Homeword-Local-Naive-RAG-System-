# Test Log

Run against the sample documents in `data/` (`company_handbook.md`,
`onboarding_guide.md`, `product_faq.md`).

Fill in the `Answer` and exact `Retrieved chunks` for each question after
running `poetry run python main.py` with `SHOW_RETRIEVED_CHUNKS = True`
(already the default) on your machine with Ollama running.

---

### Question 1 (on-topic)
**Q:** How many vacation days do employees get in their first three years?

**Answer:** 
    Retrieved chunks:
    - [003_Configuring_VPN_Access_for_Remote_Workers.txt] (distance=0.479) nue to experience issues, contact the IT helpdesk for further assistance.  **Sec...
    - [003_Configuring_VPN_Access_for_Remote_Workers.txt] (distance=0.481) **Configuring VPN Access for Remote Workers**  **Overview**  This article provid...
    - [003_Configuring_VPN_Access_for_Remote_Workers.txt] (distance=0.490) t to the company network and access company resources.  **Prerequisites**  * The...

---

### Question 2 (on-topic)
**Q:** What is the battery life of the RoboMower X1?

**Answer:** 
    Retrieved chunks:
    - [007_Troubleshooting_Issues_with_Company-Issued_Tablets.txt] (distance=0.514) ta is backed up before proceeding.  **Step 6: Check for Hardware Issues**  * Ins...
    - [007_Troubleshooting_Issues_with_Company-Issued_Tablets.txt] (distance=0.518) app to see if the issue is resolved.  **Step 5: Perform a Factory Reset**  * Go ...
    - [007_Troubleshooting_Issues_with_Company-Issued_Tablets.txt] (distance=0.521) efore escalating to advanced support.  **Step 1: Power Cycle the Tablet**  * Pre...

### Question 3 (on-topic)
**Q:** Who is my onboarding buddy and how long does the buddy program last?

**Answer:**
    Retrieved chunks:
    - [010_Configuring_Email_on_an_Android_Device.txt] (distance=0.478) ter syncing. * Tap "Next" to proceed.  **Step 6: Account Setup Complete**  * You...
    - [003_Configuring_VPN_Access_for_Remote_Workers.txt] (distance=0.483) nue to experience issues, contact the IT helpdesk for further assistance.  **Sec...
    - [002_Resetting_a_Forgotten_PIN.txt] (distance=0.503) d this limit, you will need to contact the IT Helpdesk to reset your PIN.  By fo...

### Question 4 (on-topic, tests boundary handling)
**Q:** Does the RoboMower X1's warranty cover accidental damage from driving into a pool?

**Answer:**
    Retrieved chunks:
    - [009_Resetting_a_Jammed_Printer.txt] (distance=0.469) oils from your skin can cause damage.  **Step 4: Check for Obstructions**  Inspe...
    - [007_Troubleshooting_Issues_with_Company-Issued_Tablets.txt] (distance=0.472) ta is backed up before proceeding.  **Step 6: Check for Hardware Issues**  * Ins...
    - [007_Troubleshooting_Issues_with_Company-Issued_Tablets.txt] (distance=0.494) **Troubleshooting Issues with Company-Issued Tablets**  This article provides st...

### Question 5 (OFF-topic — not in any document)
**Q:** What is the CEO's favorite programming language?

**Answer:** 
    Retrieved chunks:
    - [004_Troubleshooting_Issues_with_Microsoft_Office.txt] (distance=0.504) **Troubleshooting Issues with Microsoft Office**  This article provides steps to...
    - [001_Setting_Up_a_Mobile_Device_for_Company_Email.txt] (distance=0.506) ice's operating system). 3. Tap "Add Account" or "Create a new account". 4. Sele...
    - [004_Troubleshooting_Issues_with_Microsoft_Office.txt] (distance=0.508) lete, then restart your computer.  **Step 7: Reinstall Microsoft Office**  If no...

## Notes While Testing

- Record the actual distance values you see for Question 5 vs. the
  on-topic questions. If they're closer together than expected, you may
  need to adjust `MAX_RELEVANT_DISTANCE` in `app/config.py`.
- If an on-topic question gets a wrong or incomplete answer, check whether
  the *retrieval* step pulled the right chunk (retrieval problem) or the
  right chunk was retrieved but the model ignored it (generation problem)
  — these need different fixes.

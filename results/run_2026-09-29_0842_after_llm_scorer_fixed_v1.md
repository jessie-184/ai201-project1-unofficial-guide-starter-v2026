# Run log — after_llm_scorer_fixed_v1

- Produced by: `run_eval.py::main`
- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`
- Corpus: `campus_life` (index variant `default`)
- top-k: 4 · relevance cutoff: 0.55
- Runs per question: 3, caching off
- When: 2026-09-29 08:42

This table is one row per QUESTION. The run log your README asks for is
one row per CRITERION, so aggregate these into it — criterion 1 is how many
of your questions had the answer in the retrieved chunks, and so on.

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| How many exams are there for the CS 210 course? | pass | pass | pass |
| How do laundry payment methods differ between Aldridge Hall and Calder Annexe? | pass | pass | pass |
| When do unused dining dollars expire? | pass | pass | pass |
| Until when can I drop a course without receiving a W on my transcript? | pass | pass | pass |
| How long does it take to walk from Aldridge Hall to the science quad? | pass | pass | pass |

---

## The relevance gate on out-of-corpus questions

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.55. Refused 5 of 5.

Retrieval is deterministic and the gate is a comparison against a
fixed number, so these do not vary between runs — one pass over the
list is the whole measurement.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.787 | refused |
| How do I change the oil in a diesel engine? | 0.923 | refused |
| Who won the 1994 World Cup? | 0.847 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.849 | refused |
| How do I write a for loop in Rust? | 0.860 | refused |

---

## Real output

This is what the system actually produced. Paste the relevant parts
into your README underneath the table — the rubric asks for real
output as text, not a description of it.

### How many exams are there for the CS 210 course? — run 1

- Best distance: 0.3811 (passed the gate)
- Sources retrieved: course_cs_210.txt, course_cs_210_exams.txt

```
There are two midterms and a final for the CS 210 course. 

Source: `course_cs_210_exams.txt`
```

### How many exams are there for the CS 210 course? — run 2

- Best distance: 0.3811 (passed the gate)
- Sources retrieved: course_cs_210.txt, course_cs_210_exams.txt

```
Based on the documents, there are two midterms and a final for the CS 210 course (three exams in total). 

Source: `course_cs_210_exams.txt`
```

### How many exams are there for the CS 210 course? — run 3

- Best distance: 0.3811 (passed the gate)
- Sources retrieved: course_cs_210.txt, course_cs_210_exams.txt

```
Based on the provided documents, there are two midterms and a final for the CS 210 course. 

Source: course_cs_210_exams.txt
```

### How do laundry payment methods differ between Aldridge Hall and Calder Annexe? — run 1

- Best distance: 0.4264 (passed the gate)
- Sources retrieved: housing_aldridge_hall_laundry.txt, housing_calder_annexe.txt, housing_calder_annexe_laundry.txt

```
In Aldridge Hall, laundry is card only, whereas in Calder Annexe, laundry is app-based. 

Sources: 
- `housing_aldridge_hall_laundry.txt`
- `housing_calder_annexe_laundry.txt` (and `housing_calder_annexe.txt`)
```

### How do laundry payment methods differ between Aldridge Hall and Calder Annexe? — run 2

- Best distance: 0.4264 (passed the gate)
- Sources retrieved: housing_aldridge_hall_laundry.txt, housing_calder_annexe.txt, housing_calder_annexe_laundry.txt

```
In Aldridge Hall, laundry is card only, whereas in Calder Annexe, laundry is app-based. 

Sources: `housing_aldridge_hall_laundry.txt` and `housing_calder_annexe.txt` (or `housing_calder_annexe_laundry.txt`).
```

### How do laundry payment methods differ between Aldridge Hall and Calder Annexe? — run 3

- Best distance: 0.4264 (passed the gate)
- Sources retrieved: housing_aldridge_hall_laundry.txt, housing_calder_annexe.txt, housing_calder_annexe_laundry.txt

```
Laundry payment methods differ in that Aldridge Hall is card only, whereas Calder Annexe is app-based. 

Sources: 
- housing_aldridge_hall_laundry.txt
- housing_calder_annexe_laundry.txt (or housing_calder_annexe.txt)
```

### When do unused dining dollars expire? — run 1

- Best distance: 0.3675 (passed the gate)
- Sources retrieved: admin_dining_dollars.txt, admin_meal_plan_changes.txt, dining_north_kitchen.txt, dining_pellew_dining_hall.txt

```
Unused dining dollars disappear in May, as they do not roll over from the spring semester to the following autumn semester (admin_dining_dollars.txt).
```

### When do unused dining dollars expire? — run 2

- Best distance: 0.3675 (passed the gate)
- Sources retrieved: admin_dining_dollars.txt, admin_meal_plan_changes.txt, dining_north_kitchen.txt, dining_pellew_dining_hall.txt

```
Unused dining dollars disappear in May, as they do not roll over from the spring semester to the following autumn (*admin_dining_dollars.txt*).
```

### When do unused dining dollars expire? — run 3

- Best distance: 0.3675 (passed the gate)
- Sources retrieved: admin_dining_dollars.txt, admin_meal_plan_changes.txt, dining_north_kitchen.txt, dining_pellew_dining_hall.txt

```
Unused dining dollars disappear in May, as they do not roll over from the spring semester to the following autumn (*admin_dining_dollars.txt*).
```

### Until when can I drop a course without receiving a W on my transcript? — run 1

- Best distance: 0.2121 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_pass_fail_option.txt, admin_transcript_requests.txt, admin_withdrawal_deadline.txt

```
You can add a course through the end of the second week, and dropping after week two shows as a W on your transcript. This means you can drop a course without receiving a W through the end of the second week. 
(Source: admin_add_drop_deadline.txt)
```

### Until when can I drop a course without receiving a W on my transcript? — run 2

- Best distance: 0.2121 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_pass_fail_option.txt, admin_transcript_requests.txt, admin_withdrawal_deadline.txt

```
You can drop a course through the end of the second week without receiving a W on your transcript. After week two, a drop shows as a W. 

Source: admin_add_drop_deadline.txt
```

### Until when can I drop a course without receiving a W on my transcript? — run 3

- Best distance: 0.2121 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_pass_fail_option.txt, admin_transcript_requests.txt, admin_withdrawal_deadline.txt

```
You can drop a course through the end of the second week without receiving a W on your transcript. After week two, a drop shows as a W. 

Source: admin_add_drop_deadline.txt
```

### How long does it take to walk from Aldridge Hall to the science quad? — run 1

- Best distance: 0.2698 (passed the gate)
- Sources retrieved: dining_pellew_dining_hall.txt, housing_aldridge_hall.txt, transit_walking.txt

```
It takes 4 minutes to walk from Aldridge Hall to the science quad. 

Source: `transit_walking.txt` (and also mentioned in `housing_aldridge_hall.txt`).
```

### How long does it take to walk from Aldridge Hall to the science quad? — run 2

- Best distance: 0.2698 (passed the gate)
- Sources retrieved: dining_pellew_dining_hall.txt, housing_aldridge_hall.txt, transit_walking.txt

```
It takes 4 minutes to walk from Aldridge Hall to the science quad. 

Source: `transit_walking.txt` (and also mentioned in `housing_aldridge_hall.txt`).
```

### How long does it take to walk from Aldridge Hall to the science quad? — run 3

- Best distance: 0.2698 (passed the gate)
- Sources retrieved: dining_pellew_dining_hall.txt, housing_aldridge_hall.txt, transit_walking.txt

```
It takes 4 minutes to walk from Aldridge Hall to the science quad. 

Source: `transit_walking.txt` (and also mentioned in `housing_aldridge_hall.txt`).
```

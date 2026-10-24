# Data contract
One row per enquiry, describing a snapshot exactly 48 hours after arrival. This demo assumes all timestamps have been normalised to one timezone. The synthetic history covers calendar 2025.

| Column | Type / values | Meaning |
|---|---|---|
| lead_id | unique nonblank string | Pseudonymous enquiry key |
| enquiry_date | ISO date YYYY-MM-DD | Arrival date; production requires full timestamp |
| source | nonblank text | Website, WhatsApp, Referral, Social media; unseen categories supported |
| service | nonblank text | Study, Work permit, Tourist, Skilled migration; fictional service categories |
| response_hours | number 0–48 | Time to first response; use 48 if none by snapshot |
| consultation_booked | integer 0 or 1 | Booked by the snapshot time |
| interactions_48h | integer 0–100 | Recorded interactions before snapshot |
| recency_hours | number 0–48 | Hours since latest customer interaction; 48 if none |
| converted_30d | integer 0 or 1 | Paid-client outcome within 30 days of arrival; history only |

For training only use outcomes after the full observation window. A daily current-state export is not a valid historical 48-hour snapshot unless activity history can reconstruct it. Store first-response timestamp, activity timestamps and payment timestamp going forward; calculate the fields from those events.

## Rules: provisional, not learned
40 points for consultation booked; 30 for ≥3 interactions; 20 for recency ≤12h; 10 for response >12h (recovery opportunity). Maximum 100. High ≥60, Medium 30–59, Standard below 30. Score does not mean conversion percentage. Slow-response points are an operational choice, not an inferred causal relationship. Agree rules with staff and do not use them as staff-performance ratings.

No nationality, gender, age, passport, name, phone or email fields are required. Destination is omitted from this prototype. Only anonymised/pseudonymised agreed fields should be used in a private client pilot. Never commit real data to a repository.

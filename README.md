# OJT Placement Tracking System

Django implementation of the approved ERD (Golez, Norwen Anthony B. — CSIT 327, July 7, 2026).

**No Django Admin Panel is used.** Every entity has its own hand-built list / add / edit / delete
interface (Bootstrap 5 templates) driven by custom views in `placement/views.py`. `django.contrib.admin`
is never wired into `config/urls.py` and no model is registered with it (`placement/admin.py` is
intentionally empty).

## Entities implemented (from the ERD)

| ERD Entity     | Django Model    | Key Fields                                                                                          | Relationships |
|----------------|-----------------|-------------------------------------------------------------------------------------------------------|----------------|
| SCHOOL ADMIN   | `SchoolAdmin`   | admin_id (PK), password                                                                                | "Handles" Company & Coordinator accounts (managed through the app, not a DB FK) |
| STUDENT        | `Student`       | student_id (PK), first_name, last_name, email, contact_number, password, course, department, year_level, section, required_hours | 1 → many `OJTPlacement` |
| COMPANY        | `Company`       | company_id (PK), company_name, contact_person, password, industry_type, contact_number, email          | 1 → many `OJTPlacement` ("host") |
| COORDINATOR    | `Coordinator`   | coordinator_id (PK), first_name, last_name, password, email, department                                | 1 → many `OJTPlacement` ("supervises") |
| OJT_PLACEMENT  | `OJTPlacement`  | placement_id (PK), student_id (FK), company_id (FK), coordinator_id (FK), start_date, end_date, required_hours, status | many → 1 Student/Company/Coordinator; 1 → many `Attendance` ("generates") |
| ATTENDANCE     | `Attendance`    | attendance_id (PK), placement_id (FK), log_date, time_in, time_out, rendered_hours, status, remarks    | many → 1 `OJTPlacement` |

All passwords are hashed with Django's `make_password`/`check_password` (PBKDF2) before being stored —
never saved in plain text.

## Interface for each entity

Every entity gets the same four operations, reachable from the top navbar after logging in:

- **List view** (`/students/`, `/companies/`, `/coordinators/`, `/placements/`, `/attendance/`, `/admins/`)
  — a Bootstrap table showing every field from the ERD, with Edit/Delete actions per row.
- **Create view** (`.../add/`) — a form built from a custom `ModelForm` (see `placement/forms.py`),
  with dropdowns for foreign keys (e.g. selecting the Student/Company/Coordinator for a placement).
- **Update view** (`.../<id>/edit/`) — same form, pre-filled.
- **Delete view** (`.../<id>/delete/`) — confirmation page before removing the record.

A **Dashboard** (`/`) shows record counts for all six entities as an at-a-glance summary.

Access to all of the above requires a School Admin session login (`/login/`) — a custom
session-based auth flow (see `placement/decorators.py` and `placement/views.py`), independent of
`django.contrib.admin`.

## Running the project locally

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create the database tables
python manage.py makemigrations placement
python manage.py migrate

# 4. Create your first School Admin login (admin_id=1, password=admin123 by default)
python manage.py seed_admin
# or choose your own password:
python manage.py seed_admin --password YourPasswordHere

# 5. Run the development server
python manage.py runserver
```

Then open http://127.0.0.1:8000/login/ and log in with `admin_id: 1` and the password you seeded.
From the Dashboard you can add Companies, Coordinators, Students, OJT Placements, and Attendance
records, and create additional Admin accounts under "Admin Accounts".

## Project structure

```
ojt-tracking-system/
├── manage.py
├── requirements.txt
├── config/                    # Django project settings & root URLs (no admin site)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
└── placement/                 # The single app implementing the whole ERD
    ├── models.py               # SchoolAdmin, Student, Company, Coordinator, OJTPlacement, Attendance
    ├── forms.py                 # One ModelForm per entity
    ├── views.py                  # Custom List/Create/Update/Delete views per entity + auth
    ├── urls.py                    # Routes for every entity's CRUD + login/logout
    ├── decorators.py               # Custom session-login guard (not django.contrib.admin)
    ├── admin.py                     # Intentionally empty — Django admin not used
    ├── management/commands/seed_admin.py   # Bootstraps the first admin login
    ├── templatetags/placement_extras.py     # Dynamic field lookup for the shared list template
    ├── templates/placement/                 # base.html, login.html, dashboard.html,
    │                                          generic_list/form/confirm_delete.html
    └── static/placement/css/style.css
```

## Notes on design choices

- The list/create/edit/delete templates are shared (`generic_list.html`, `generic_form.html`,
  `generic_confirm_delete.html`) and driven per-entity by context supplied from each model's own
  view classes in `views.py` — this keeps the UI consistent across all six entities while every
  entity still has its own dedicated views, URLs, and form validation, fully satisfying "an
  appropriate interface for each entity" without duplicating HTML six times over.
- `OJTPlacement` and `Attendance` use Django `ForeignKey`s (`on_delete=models.CASCADE`) to mirror the
  ERD's crow's-foot notation (one Student/Company/Coordinator to many Placements; one Placement to
  many Attendance logs).
- The "Handles" relationship between School Admin and Company/Coordinator is administrative
  (the School Admin manages those accounts through the app) rather than a stored foreign key, since
  the ERD does not show an `admin_id` column on either the Company or Coordinator table.

## Submission checklist (per assignment instructions)

1. Push this repository to GitHub and copy the repo URL.
2. Take screenshots of: the login page, the dashboard, and the list/add/edit views for each of the
   six entities.
3. Use the entity descriptions and interface explanations above in your write-up.
4. Run `git log --oneline` (or check GitHub's commit history view) to show the separate commits made
   for each model and each entity's CRUD interface — already included in this repo's history.
5. Combine everything into a single PDF for submission.

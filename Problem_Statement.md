Problem Statement
1. Title

Esports Tournament Management Platform

2. Domain

Gaming / Esports Technology

3. Who is the user? (2-3 user types, with roles)
Tournament Organizer (Admin): Creates and configures tournaments, approves/rejects team registrations, generates brackets, resolves match disputes, and publishes final results.
Team Captain (Player): Registers a team for open tournaments, adds/manages teammates, views the schedule and bracket, submits match score reports.
Team Member (Player): Joins a team via an invite/code, views their own match schedule and team's tournament progress (read-only for team management actions).
4. What problem are we solving? (3-5 sentences, real-life example)

College gaming clubs and small esports organizers currently run tournaments using a patchwork of WhatsApp groups, Google Forms, and manually maintained Excel sheets. This leads to registration chaos (duplicate or incomplete entries), manual bracket seeding errors, no single source of truth for match timings, and frequent disputes over reported scores since results are just typed into a shared document. For example, a college tech fest running a 32-team Valorant tournament might spend hours manually seeding brackets in Excel, only to have a scheduling clash discovered an hour before a match, or a dispute over a submitted screenshot of a scoreboard with no audit trail. This platform digitizes the entire tournament lifecycle — registration, payment, seeding, scheduling, live results, and leaderboards — into one system, removing manual errors and giving every participant a transparent, single source of truth.

5. Proposed Solution (what the application will do, feature-wise)
Team & Player Management: Captains create teams, invite members via a join code, and manage rosters.
Tournament Creation & Registration: Organizers create tournaments (format, game title, team size, entry fee, slot limit); teams register and pay an entry fee through a sandboxed payment gateway.
Automated Bracket Generation: Single-elimination bracket auto-generated once registration closes, based on seeding rules (random or ranking-based).
Match Scheduling: System auto-assigns match slots avoiding team double-booking; organizers can manually override if needed.
Score Reporting & Dispute Handling: Captains submit match results; organizer reviews and confirms/reverses before the bracket advances.
Live Leaderboard & Standings: Real-time tournament standings and team stats (wins/losses, win %).
Notifications: Email alerts for registration confirmation, match schedule, and results.
(Enhancement, Day 41–60) AI Feature: Match win-probability prediction based on historical team performance, and/or an ELO-style skill rating system used to seed brackets more fairly.
6. Core Entities / Database Tables (list all, minimum 5)
User — id, name, email, password_hash, role (admin/captain/player)
Team — id, name, captain_id (FK → User), created_at
TeamMember — id, team_id (FK → Team), user_id (FK → User) — junction table (Many-to-Many between User and Team)
Tournament — id, name, game_title, format, entry_fee, slot_limit, status, organizer_id (FK → User)
Registration — id, tournament_id (FK), team_id (FK), status (pending/approved/rejected), registered_at
Match — id, tournament_id (FK), team_a_id (FK → Team), team_b_id (FK → Team), scheduled_time, round_number
MatchResult — id, match_id (FK, One-to-One), winner_team_id (FK), score_summary, submitted_by, confirmed_by_admin (bool)
Payment — id, registration_id (FK, One-to-One), amount, payment_status, transaction_ref

Relationships: User↔Team is Many-to-Many via TeamMember; Tournament→Registration and Tournament→Match are One-to-Many; Match→MatchResult and Registration→Payment are One-to-One.

7. User Roles & Permissions (minimum 2 distinct roles)
Admin/Organizer: Full access — create/edit tournaments, approve registrations, generate brackets, confirm/override match results, view all payments.
Team Captain: Register/manage own team, submit match results for own matches, view own registrations and payment status.
Team Member: Read-only access to own team's schedule, bracket position, and results.
8. Success Criteria
A team captain can register a team for an open tournament and receive email confirmation in under 2 minutes.
An organizer can generate a complete bracket for 16+ registered teams with a single action, with zero scheduling conflicts.
Submitted match results are reflected on the live leaderboard within a few seconds of admin confirmation.
Zero double-booked match slots for any team across a live tournament.
9. Out of Scope (clearly list what you will NOT build, to avoid over-commitment)
Live video/stream embedding or broadcasting.
Direct integration with in-game APIs (e.g. Riot API) to auto-pull match stats — results are self-reported and admin-confirmed for MVP.
Real-money betting or wagering features.
In-app real-time chat or voice communication.
Double-elimination / round-robin formats (single-elimination only for MVP; can be a stretch goal).
10. Chosen Track: Python (Django REST Framework)

Recommended over FastAPI for this project because Django's built-in admin panel and auth system will save significant time on the Organizer/Admin dashboard and role-based permissions — both central to this app. FastAPI remains a valid alternative if you prefer a more lightweight, async-first setup.

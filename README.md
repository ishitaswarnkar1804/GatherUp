<div align="center">

# ✦ GatherUp

### Plan together. Decide together. Get things done together.

<p>
  <b>A modern group planning & collaboration platform built for real-world group activities.</b>
</p>

<p>
  Events · Expenses · Polls · Tasks · Food · Chat · Gallery · Notifications
</p>

<br>

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?style=for-the-badge&logo=javascript&logoColor=111111)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=for-the-badge)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

<br>

**🌐 Full Stack · 🔐 Secure · 📱 Responsive · 🧩 Modular · 🚀 Deployment Ready**

</div>

---

## 🌟 What is GatherUp?

**GatherUp** is a full-stack web application designed to make group planning dramatically easier.

Instead of using one app for chatting, another for polls, spreadsheets for expenses, notes for tasks, and random folders for photos, GatherUp brings everything into **one shared group workspace**.

Whether the group is planning:

- 🎉 A college event
- 🏕️ A trip
- 🎂 A birthday
- 🍕 A group dinner
- 🏆 A competition
- 📚 A student project
- 🎮 A meetup

GatherUp gives everyone one place to **plan, coordinate, communicate, and keep track of everything**.

---

# ✨ The Idea

```mermaid
flowchart LR
    U["👤 Group Members"]

    U --> C["💬 Chat"]
    U --> E["📅 Events"]
    U --> X["💰 Expenses"]
    U --> P["🗳️ Polls"]
    U --> T["✅ Tasks"]
    U --> F["🍕 Food Orders"]
    U --> G["📸 Gallery"]

    C --> W["🎯 GatherUp<br/>Shared Workspace"]
    E --> W
    X --> W
    P --> W
    T --> W
    F --> W
    G --> W

    W --> N["🔔 Notifications"]
```

> **One group. One workspace. Everything organized.**

---

# 🚀 Features

<table>
<tr>
<td width="50%">

### 🔐 Authentication

- Secure registration
- Password hashing
- JWT authentication
- Remember Me
- Forgot Password
- Protected routes
- Session management

</td>
<td width="50%">

### 👥 Group Management

- Create groups
- Join groups
- Manage members
- Member roles
- Group workspace
- Group-specific data

</td>
</tr>

<tr>
<td>

### 📅 Event Planning

- Create events
- Event descriptions
- Date & time
- Locations
- Participant management
- Event-specific collaboration

</td>
<td>

### 💰 Expense Management

- Add expenses
- Track who paid
- Split expenses
- Track individual shares
- Mark splits as paid
- Event-linked expenses

</td>
</tr>

<tr>
<td>

### 🗳️ Polls

- Create polls
- Multiple options
- Vote once
- Live vote counts
- User vote tracking
- Persistent results

</td>
<td>

### ✅ Task Management

- Create tasks
- Assign members
- Due dates
- Pending state
- In-progress state
- Completed state

</td>
</tr>

<tr>
<td>

### 🍕 Food Orders

- Add food items
- Quantity tracking
- Price tracking
- Order status
- Group/event coordination

</td>
<td>

### 💬 Group Chat

- Persistent messages
- Group-based conversations
- Real-time communication
- Message notifications

</td>
</tr>

<tr>
<td>

### 📸 Shared Gallery

- Upload images
- Captions
- Group gallery
- Event-linked media

</td>
<td>

### 🔔 Notifications

- Persistent notifications
- Chat notifications
- Activity updates
- Read/unread state

</td>
</tr>
</table>

---

# 🧭 How GatherUp Works

```mermaid
flowchart TD
    A["🚀 Open GatherUp"] --> B{"Authenticated?"}

    B -->|No| C["🔐 Login"]
    B -->|No Account| D["📝 Register"]

    D --> E["✅ Account Created"]
    E --> C

    C --> F{"Valid Credentials?"}

    F -->|No| C
    F -->|Yes| G["🏠 Dashboard"]

    G --> H["👥 Select Group"]

    H --> I["📅 Events"]
    H --> J["💰 Expenses"]
    H --> K["🗳️ Polls"]
    H --> L["✅ Tasks"]
    H --> M["🍕 Food"]
    H --> N["💬 Chat"]
    H --> O["📸 Gallery"]

    I --> P["🔔 Notifications"]
    J --> P
    K --> P
    L --> P
    M --> P
    N --> P
    O --> P
```

---

# 🏗️ System Architecture

GatherUp follows a **client-server architecture** with a JavaScript frontend, FastAPI backend, and MySQL database.

```mermaid
flowchart TB

    subgraph CLIENT["🌐 CLIENT"]
        UI["HTML5 + CSS3 + JavaScript"]
        SW["Service Worker"]
        PWA["PWA Support"]
    end

    subgraph BACKEND["⚡ FASTAPI BACKEND"]
        MAIN["FastAPI Application"]

        AUTH["🔐 Authentication"]
        GROUPS["👥 Groups"]
        EVENTS["📅 Events"]
        EXPENSES["💰 Expenses"]
        POLLS["🗳️ Polls"]
        TASKS["✅ Tasks"]
        FOOD["🍕 Food"]
        GALLERY["📸 Gallery"]
        CHAT["💬 Chat"]
        NOTIFICATIONS["🔔 Notifications"]
    end

    subgraph DATA["🗄️ DATA LAYER"]
        ORM["SQLAlchemy ORM"]
        DB[("MySQL")]
    end

    UI --> MAIN
    SW --> UI
    PWA --> UI

    MAIN --> AUTH
    MAIN --> GROUPS
    MAIN --> EVENTS
    MAIN --> EXPENSES
    MAIN --> POLLS
    MAIN --> TASKS
    MAIN --> FOOD
    MAIN --> GALLERY
    MAIN --> CHAT
    MAIN --> NOTIFICATIONS

    AUTH --> ORM
    GROUPS --> ORM
    EVENTS --> ORM
    EXPENSES --> ORM
    POLLS --> ORM
    TASKS --> ORM
    FOOD --> ORM
    GALLERY --> ORM
    CHAT --> ORM
    NOTIFICATIONS --> ORM

    ORM --> DB
```

---

# 🧩 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| 🎨 Frontend | HTML5 | Page structure |
| 🎨 Styling | CSS3 | Responsive interface |
| ⚡ Frontend Logic | Vanilla JavaScript | API communication & UI |
| 🐍 Backend | Python | Server-side application |
| ⚡ Framework | FastAPI | REST API & application server |
| 🔐 Security | JWT + password hashing | Authentication |
| 🗄️ Database | MySQL | Persistent storage |
| 🔗 ORM | SQLAlchemy | Database interaction |
| 💬 Communication | WebSockets | Group chat |
| 🐳 Deployment | Docker | Containerization |
| ☁️ Hosting Config | Render | Deployment configuration |
| 📦 Version Control | Git + GitHub | Source control |

---

# 🗂️ Project Architecture

```text
GatherUp/
│
├── backend/
│   │
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   │
│   └── routers/
│       ├── auth.py
│       ├── groups.py
│       ├── group_membership.py
│       ├── events.py
│       ├── expenses.py
│       ├── polls.py
│       ├── tasks.py
│       ├── food.py
│       ├── gallery.py
│       ├── chat.py
│       ├── notifications.py
│       └── _helpers.py
│
├── frontend/
│   │
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── group.html
│   ├── style.css
│   ├── manifest.json
│   ├── service-worker.js
│   │
│   └── js/
│       └── app.js
│
├── database/
│
├── Dockerfile
├── render.yaml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

---

# 👥 Group Workspace

The group workspace is the central part of GatherUp.

```mermaid
flowchart LR

    GROUP["👥 GROUP"]

    GROUP --> MEMBERS["👤 Members"]
    GROUP --> EVENTS["📅 Events"]
    GROUP --> EXPENSES["💰 Expenses"]
    GROUP --> POLLS["🗳️ Polls"]
    GROUP --> TASKS["✅ Tasks"]
    GROUP --> FOOD["🍕 Food"]
    GROUP --> CHAT["💬 Chat"]
    GROUP --> GALLERY["📸 Gallery"]
    GROUP --> NOTIFY["🔔 Notifications"]
```

Everything is tied back to a group, keeping collaboration organized and separated between different activities.

---

# 💰 Expense Splitting

Expense management is designed around a simple workflow:

```mermaid
flowchart LR

    A["👤 Member"] --> B["💰 Create Expense"]

    B --> C["₹ Total Amount"]
    B --> D["💳 Paid By"]
    B --> E["👥 Select Members"]

    E --> F["Expense Split"]

    F --> G["Member A"]
    F --> H["Member B"]
    F --> I["Member C"]

    G --> J["💵 Individual Share"]
    H --> J
    I --> J

    J --> K["✅ Payment Status"]
```

### Expense entities

```mermaid
erDiagram

    USERS ||--o{ EXPENSES : pays
    GROUPS ||--o{ EXPENSES : contains
    EVENTS ||--o{ EXPENSES : relates_to

    EXPENSES ||--o{ EXPENSE_SPLITS : contains
    USERS ||--o{ EXPENSE_SPLITS : owes

    USERS {
        int id
        string first_name
        string last_name
        string email
        string password_hash
        string role
    }

    EXPENSES {
        int id
        int group_id
        int event_id
        int paid_by
        string title
        decimal amount
        date expense_date
        string description
    }

    EXPENSE_SPLITS {
        int id
        int expense_id
        int user_id
        decimal amount
        boolean paid
    }
```

---

# 🗳️ Poll System

```mermaid
flowchart TD

    A["📝 Create Poll"] --> B["➕ Add Options"]
    B --> C["📢 Publish"]
    C --> D["👥 Members Vote"]

    D --> E["📊 Store Vote"]

    E --> F["🔢 Calculate Counts"]

    F --> G["🏆 Display Results"]

    G --> H["👤 Show User's Vote"]
```

Each poll, option, and vote is stored in the database so results persist across sessions.

---

# ✅ Task Lifecycle

```mermaid
stateDiagram-v2

    [*] --> Pending

    Pending --> InProgress: Start
    InProgress --> Completed: Finish

    Pending --> Completed: Complete

    Completed --> [*]
```

Tasks support assignment, descriptions, due dates, and status tracking.

---

# 📅 Event Planning

```mermaid
sequenceDiagram

    participant U as 👤 User
    participant UI as 🌐 Frontend
    participant API as ⚡ FastAPI
    participant DB as 🗄️ MySQL

    U->>UI: Create Event
    UI->>API: POST /events
    API->>DB: Store Event
    DB-->>API: Event Created
    API-->>UI: Event Response
    UI-->>U: 🎉 Event Added

    U->>UI: Join Event
    UI->>API: Update Participation
    API->>DB: Store Participant
    DB-->>API: Updated
    API-->>UI: Participation Confirmed
```

---

# 💬 Chat & Notifications

```mermaid
sequenceDiagram

    participant A as 👤 Member A
    participant WS as 🔌 WebSocket
    participant API as ⚡ FastAPI
    participant DB as 🗄️ MySQL
    participant B as 👤 Member B

    A->>WS: Send Message
    WS->>API: Process Message
    API->>DB: Save Message

    API-->>A: Message Sent
    API-->>B: New Message

    API->>DB: Create Notification
    DB-->>B: Notification Available
```

This allows group conversations to remain connected to the rest of the collaboration system.

---

# 🗄️ Database Design

```mermaid
erDiagram

    USERS ||--o{ GROUP_MEMBERS : joins
    GROUPS ||--o{ GROUP_MEMBERS : contains

    GROUPS ||--o{ EVENTS : has
    EVENTS ||--o{ EVENT_PARTICIPANTS : includes
    USERS ||--o{ EVENT_PARTICIPANTS : participates

    GROUPS ||--o{ EXPENSES : contains
    EXPENSES ||--o{ EXPENSE_SPLITS : divided_into

    GROUPS ||--o{ POLLS : contains
    POLLS ||--o{ POLL_OPTIONS : has
    POLL_OPTIONS ||--o{ POLL_VOTES : receives
    USERS ||--o{ POLL_VOTES : casts

    GROUPS ||--o{ TASKS : contains
    USERS ||--o{ TASKS : assigned_to

    GROUPS ||--o{ FOOD_ORDERS : contains
    USERS ||--o{ FOOD_ORDERS : places

    GROUPS ||--o{ GALLERY : contains
    USERS ||--o{ GALLERY : uploads

    USERS ||--o{ NOTIFICATIONS : receives

    GROUPS ||--o{ GROUP_MESSAGES : contains
    USERS ||--o{ GROUP_MESSAGES : sends
```

---

# 🔐 Authentication Architecture

```mermaid
flowchart TD

    START["👤 User"] --> LOGIN["🔐 Login"]

    LOGIN --> CRED["Email + Password"]

    CRED --> VERIFY["🔎 Verify Credentials"]

    VERIFY -->|Invalid| ERROR["❌ Authentication Error"]
    ERROR --> LOGIN

    VERIFY -->|Valid| JWT["🎟️ Generate JWT"]

    JWT --> STORAGE{"Remember Me?"}

    STORAGE -->|Yes| LOCAL["Persistent Browser Storage"]
    STORAGE -->|No| SESSION["Session Storage"]

    LOCAL --> DASH["🏠 Dashboard"]
    SESSION --> DASH
```

GatherUp uses password hashing and JWT-based authentication rather than storing plaintext passwords.

---

# 🔑 Password Recovery

```mermaid
flowchart LR

    A["🔐 Forgot Password"] --> B["📧 Enter Account Email"]
    B --> C["🔎 Find Account"]
    C --> D["🎟️ Generate Reset Token"]
    D --> E["🔗 Reset Password"]
    E --> F["🔒 New Password"]
    F --> G["✅ Account Updated"]
    G --> H["🔐 Login"]
```

The reset mechanism is implemented as an application-level recovery flow so the project can be demonstrated without requiring a third-party email service.

---

# 📱 Responsive Experience

GatherUp is designed around a responsive layout so the same application can be used across:

```text
┌─────────────────────────────────────────┐
│              🖥️ Desktop                 │
│                                         │
│       Dashboard / Group Workspace       │
│                                         │
└─────────────────────────────────────────┘

              ↓ responsive ↓

┌───────────────────────┐
│      📱 Mobile        │
│                       │
│  Dashboard            │
│  Groups               │
│  Events               │
│  Expenses             │
│  Tasks                │
│  Chat                 │
│                       │
└───────────────────────┘
```

---

# 🧪 Validation

The project has been checked across the major application layers.

| Area | Status |
|---|:---:|
| Backend Python compilation | ✅ |
| Frontend JavaScript syntax | ✅ |
| Authentication | ✅ |
| Registration | ✅ |
| Login | ✅ |
| Remember Me | ✅ |
| Password Reset | ✅ |
| Groups | ✅ |
| Events | ✅ |
| Expenses | ✅ |
| Polls | ✅ |
| Tasks | ✅ |
| Food Orders | ✅ |
| Gallery | ✅ |
| Chat | ✅ |
| Notifications | ✅ |
| Static frontend routes | ✅ |
| Health endpoint | ✅ |
| Docker configuration | ✅ |

---

# ⚙️ Local Development

## 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/GatherUp.git
cd GatherUp
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure `.env`

Create a `.env` file locally:

```env
DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@HOST:3306/gatherup
JWT_SECRET=replace-with-a-long-random-secret
PUBLIC_BASE_URL=http://127.0.0.1:8000
```

> ⚠️ Never commit `.env` to GitHub.

## 5. Start the application

```bash
uvicorn backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🐳 Docker

Build the image:

```bash
docker build -t gatherup .
```

Run it:

```bash
docker run -p 8000:8000 --env-file .env gatherup
```

The production Docker configuration intentionally does not use development auto-reload.

---

# ☁️ Deployment

GatherUp includes deployment-oriented configuration:

```text
Dockerfile
render.yaml
requirements.txt
.gitignore
.dockerignore
```

The application exposes a health endpoint:

```http
GET /health
```

Response:

```json
{
  "status": "ok",
  "service": "gatherup"
}
```

### Required production environment

```text
DATABASE_URL
JWT_SECRET
PUBLIC_BASE_URL
```

> GitHub stores the source code. Your hosting platform runs the application and supplies production environment variables.

---

# 🔒 Security

GatherUp follows several basic application-security practices:

- 🔐 Password hashing
- 🎟️ JWT authentication
- ⏳ Expiring authentication tokens
- 🛡️ Protected API endpoints
- 🔑 Environment-based secrets
- 🚫 `.env` excluded from Git
- 🗄️ Database-backed authorization
- 🔒 No plaintext passwords stored

---

# 📊 Feature Overview

```mermaid
mindmap
    root((GATHERUP))
        Authentication
            Registration
            Login
            Remember Me
            Forgot Password
        Groups
            Members
            Roles
            Workspace
        Events
            Date
            Time
            Location
            Participants
        Expenses
            Amount
            Payer
            Splits
            Payment Status
        Polls
            Questions
            Options
            Voting
            Results
        Tasks
            Assignment
            Due Date
            Status
        Food
            Items
            Quantity
            Price
            Status
        Communication
            Chat
            Notifications
        Gallery
            Images
            Captions
```

---

# 🎯 Why GatherUp?

Traditional group planning often looks like:

```text
WhatsApp
   +
Google Sheets
   +
Notes
   +
Poll App
   +
Payment Screenshots
   +
Random Photo Folder
   +
"Who was supposed to do this?"
```

GatherUp turns that into:

```text
                 ┌───────────────────┐
                 │     GATHERUP      │
                 ├───────────────────┤
                 │ 📅 Events         │
                 │ 💰 Expenses       │
                 │ 🗳️ Polls          │
                 │ ✅ Tasks          │
                 │ 🍕 Food           │
                 │ 💬 Chat           │
                 │ 📸 Gallery        │
                 │ 🔔 Notifications  │
                 └───────────────────┘
```

### The goal is simple:

> **Less coordination chaos. More actual collaboration.**

---

# 📈 Future Roadmap

```mermaid
timeline
    title GatherUp Roadmap

    section Core Platform
        Authentication : Complete
        Groups : Complete
        Events : Complete
        Expenses : Complete

    section Collaboration
        Polls : Complete
        Tasks : Complete
        Food Orders : Complete
        Chat : Complete
        Notifications : Complete
        Gallery : Complete

    section Future
        Advanced Analytics : Planned
        Calendar Integration : Planned
        Maps & Location : Planned
        Push Notifications : Planned
        Mobile Application : Planned
        AI Planning Assistant : Planned
```

---

# 🎓 Software Engineering Concepts Demonstrated

GatherUp brings together several software-engineering concepts in one working system:

- Client-server architecture
- REST API development
- Authentication & authorization
- Relational database design
- ORM-based persistence
- Entity relationships
- CRUD operations
- Real-time communication
- Modular backend routing
- Responsive frontend development
- State management
- Deployment configuration
- Containerization
- Version control with Git

---

# 📚 API

FastAPI automatically provides interactive API documentation.

Once the application is running:

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

These provide an interactive view of the backend endpoints.

---

# 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/your-feature
```

Make your changes, then:

```bash
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 📄 License

This project was created as a software engineering project.

If you plan to distribute GatherUp publicly, add the license that matches how you want others to use the project.

---

<div align="center">

## 💜 GatherUp

### One place for every group plan.

**Plan. Collaborate. Celebrate.**

<br>

⭐ **Star the repository if you like GatherUp.**

</div>

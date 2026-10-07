# RRB Technician Grade-I (Signal) — 4-in-1 CBT Mega Mock Hub

An ultra-modern, high-performance Computer-Based Test (CBT) portal simulating the official TCS iON exam pattern for **RRB Technician Grade-I (Signal) CEN 02/2024**.

All four specialized 100-question mock tests are integrated into **one single unified web application**, complete with a real-time countdown timer, interactive question palette, instant evaluation (+1.0 / -0.33 marking), detailed performance diagnostics, and step-by-step solutions with explanations.

---

## 📁 Clean Folder Structure

```
RRB/
├── .gitignore              # Git ignore rules for node_modules, cache, logs
├── README.md               # Complete documentation and deployment guide
├── vercel.json             # Vercel deployment configuration & security headers
├── package.json            # NPM scripts and project metadata
├── index.html              # Main application entry point
├── css/
│   └── style.css           # Modern design system (Vanilla CSS, Dark/Light modes)
├── js/
│   ├── app.js              # CBT test engine, timer, scoring, and UI controller
│   └── data.js             # 400 questions dataset (100 Qs per subject)
├── scripts/
│   └── build_data.py       # Dataset compiler & validator script
└── legacy/                 # Archived standalone single-page mocks
    ├── RRB_Technician_GradeI_BSE_100Q_Mock.html
    ├── RRB_Technician_GradeI_Computers_100Q_Mock.html
    └── RRB_Technician_GradeI_Mathematics_100Q_Mock.html
```

---

## 🏆 Official All-in-One Full Mock Test (Exact CBT Pattern)

Matches the official RRB Technician Gr-I Signal notification break-up:

| Subject / Section | Questions | Marks | Official Weightage |
| :--- | :---: | :---: | :--- |
| **1. General Awareness** | 10 | 10 | Static GK, Current Affairs, Railways GK, Polity, Geography |
| **2. General Intelligence & Reasoning** | 15 | 15 | Syllogisms, Series, Coding-Decoding, Blood Relations, Direction |
| **3. Basics of Computers & Applications** | 20 | 20 | Computer Architecture, OS, Networking, MS Office, Security |
| **4. Mathematics** | 20 | 20 | Algebra, Quadratics, AP, Trigonometry, Coordinate, Statistics |
| **5. Basic Science and Engineering** | 35 | 35 | Physics Fundamentals, DC Circuits, EMI, Electronics, Transducers |
| **TOTAL** | **100 Qs** | **100 Marks** | **90 Minutes Duration (+1.0 / -0.33 Marking)** |

---

## 🎯 Additional Subject-Wise Special Mocks (100 Qs Each)

| Subject / Section | Questions | Duration | Marks (+1 / -0.33) | Syllabus Areas Covered |
| :--- | :---: | :---: | :---: | :--- |
| **1. Basic Science & Engineering** | 100 Qs | 90 Mins | 100 Marks | Physics Fundamentals, DC Circuits, Magnetism, EMI, Electronics & Devices, Digital & Microprocessors, Measurements & Transducers |
| **2. Basics of Computers & Applications** | 100 Qs | 90 Mins | 100 Marks | Architecture, Operating Systems, Networking, Protocols, Storage, Data Representation, MS Office, Cybersecurity |
| **3. Mathematics** | 100 Qs | 90 Mins | 100 Marks | Number System, Algebra, Quadratic Equations, AP, Trigonometry, Coordinate Geometry, Mensuration, Statistics & Probability |
| **4. General Awareness & Reasoning** | 100 Qs | 90 Mins | 100 Marks | Indian Polity, Geography, History, Economy, Railways GK, Science, Syllogisms, Series, Blood Relations, Direction Sense |

---

## 🚀 Running Locally

### Option 1: Direct Browser Launch (Zero Installation)
Simply double-click or open `index.html` in any web browser (Chrome, Edge, Firefox, Safari).

### Option 2: Using Node Dev Server
```bash
# Run local development server
npm run dev
# or
npx serve -l 3000 .
```
Then visit: `http://localhost:3000`

---

## ☁️ How to Deploy to Vercel

This repository is already configured with `vercel.json` for zero-configuration, instant static deployment on Vercel.

### Method A: Deploy via Vercel CLI (Fastest)

1. Open your terminal in the `RRB` project root directory:
   ```bash
   cd d:\projects\RRB
   ```
2. Run the Vercel deployment command:
   ```bash
   npx vercel
   ```
3. Follow the quick terminal prompts:
   - *Set up and deploy?* → **Y**
   - *Which scope?* → Select your Vercel account
   - *Link to existing project?* → **N**
   - *What's your project's name?* → `rrb-technician-cbt-hub` (or your choice)
   - *In which directory is your code located?* → `./`
4. For production deployment:
   ```bash
   npx vercel --prod
   ```
5. You will receive your live URL instantly (e.g., `https://rrb-technician-cbt-hub.vercel.app`)!

---

### Method B: Deploy via GitHub & Vercel Dashboard

1. Initialize git and push to GitHub:
   ```bash
   git init
   git add .
   git commit -m "feat: complete unified 4-in-1 RRB CBT app"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/rrb-technician-cbt.git
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com) and log in.
3. Click **"Add New..."** → **"Project"**.
4. Import your GitHub repository `rrb-technician-cbt`.
5. Keep default settings (Framework Preset: **Other**, Root Directory: `./`).
6. Click **Deploy**. Vercel will build and deploy your app globally in under 30 seconds!

---

## ⚙️ Key Features

- **Real TCS iON CBT Experience**: Realistic question layout, 100-question navigation palette, color status codes (Answered, Not Answered, Marked for Review, Answered & Review, Not Visited).
- **Persistent State**: Progress, answers, and scores are automatically saved in `localStorage`. You won't lose your work if you refresh.
- **Dynamic Scorecard & Diagnostics**: Net Score calculation, accuracy percentage, question review sheet with filter chips (All, Correct, Incorrect, Unattempted).
- **Dark & Light Modes**: Seamless theme switching with high-contrast readability.
- **Audio Sound Effects**: Tactile sound feedback powered by the Web Audio API (with instant mute toggle).
- **Print / PDF Export**: Built-in `@media print` layout to print or save your diagnostic scorecard as a PDF.
- **Keyboard Shortcuts**: Keys `1-4` or `A-D` for choosing options, `Alt+N` for Next, `Alt+P` for Previous, `Alt+M` for Mark for Review.

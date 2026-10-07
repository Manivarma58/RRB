/**
 * RRB Technician Grade-I (Signal) — Unified 4-in-1 CBT Engine
 * Handles State, Timer, Navigation, Scoring, Audio, LocalStorage & Review
 */

// --- Audio Synthesizer (Web Audio API) ---
class SoundController {
  constructor() {
    this.enabled = true;
    this.ctx = null;
  }

  init() {
    if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioCtx();
    }
  }

  playTone(freq, type = 'sine', duration = 0.08, gainVal = 0.1) {
    if (!this.enabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      if (this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {
      // Audio autoplay policy fallback
    }
  }

  click() { this.playTone(600, 'sine', 0.04, 0.05); }
  select() { this.playTone(850, 'triangle', 0.06, 0.08); }
  next() { this.playTone(700, 'sine', 0.05, 0.06); }
  submit() {
    this.playTone(523.25, 'sine', 0.1, 0.1);
    setTimeout(() => this.playTone(659.25, 'sine', 0.1, 0.1), 100);
    setTimeout(() => this.playTone(783.99, 'sine', 0.2, 0.12), 200);
  }
}

const sound = new SoundController();

// --- Main Application Controller ---
class RRBApp {
  constructor() {
    this.activeTestId = 'bse'; // default test
    this.currentView = 'hub'; // Start on Hub overview!
    this.testStates = {};
    this.timerInterval = null;
    this.solFilter = 'all';

    this.init();
  }

  init() {
    this.loadAllTestStates();
    this.setupTheme();
    this.renderTabs();
    this.renderHubCards();
    this.setupEventListeners();
    this.showHubView(); // Show Hub view first so candidate chooses when to start
    this.updateTimerDisplay();
    this.startTimerLoop();
  }

  // --- State Initialization & Persistence ---
  getInitialState(testId) {
    const testData = MOCK_TESTS[testId];
    const qCount = testData.questions.length;
    return {
      testId: testId,
      currentIndex: 0,
      answers: new Array(qCount).fill(null),
      status: new Array(qCount).fill('not-visited'),
      secondsLeft: testData.durationMinutes * 60,
      submitted: false,
      started: false,
      results: null
    };
  }

  loadAllTestStates() {
    Object.keys(MOCK_TESTS).forEach(id => {
      const saved = localStorage.getItem(`rrb_cbt_${id}`);
      if (saved) {
        try {
          this.testStates[id] = JSON.parse(saved);
        } catch (e) {
          this.testStates[id] = this.getInitialState(id);
        }
      } else {
        this.testStates[id] = this.getInitialState(id);
      }
    });
  }

  saveActiveState() {
    if (!this.activeTestId) return;
    localStorage.setItem(
      `rrb_cbt_${this.activeTestId}`,
      JSON.stringify(this.testStates[this.activeTestId])
    );
  }

  getActiveState() {
    return this.testStates[this.activeTestId];
  }

  getActiveData() {
    return MOCK_TESTS[this.activeTestId];
  }

  // --- Start Test Explicitly (Turns Timer On) ---
  startMockTest(testId) {
    if (!MOCK_TESTS[testId]) return;
    sound.submit();
    this.activeTestId = testId;
    const state = this.getActiveState();
    state.started = true;
    if (state.status[state.currentIndex] === 'not-visited') {
      state.status[state.currentIndex] = 'not-answered';
    }
    this.saveActiveState();

    this.showTestView();
    this.renderTabs();
    this.populateSectionDropdown();
    this.renderCurrentQuestion();
    this.updatePaletteAndLegend();
    this.updateTimerDisplay();
  }

  // --- Test Switching ---
  switchTest(testId) {
    if (!MOCK_TESTS[testId]) return;
    this.activeTestId = testId;
    const state = this.getActiveState();
    this.saveActiveState();

    this.showTestView();
    this.renderTabs();
    this.populateSectionDropdown();
    this.renderCurrentQuestion();
    this.updatePaletteAndLegend();
    this.updateTimerDisplay();

    // Update Top Submit/Start Button
    const btnSubmit = document.getElementById('btnSubmitTop');
    if (state.submitted) {
      btnSubmit.innerHTML = '📊 View Scorecard';
      btnSubmit.className = 'btn-submit-top';
      btnSubmit.style.background = 'linear-gradient(135deg, #6366f1, #4f46e5)';
    } else if (!state.started) {
      btnSubmit.innerHTML = '▶️ Start Test';
      btnSubmit.className = 'btn-submit-top';
      btnSubmit.style.background = 'linear-gradient(135deg, #10b981, #059669)';
    } else {
      btnSubmit.innerHTML = 'Submit Test';
      btnSubmit.className = 'btn-submit-top';
      btnSubmit.style.background = '';
    }
  }

  // --- Views Navigation (Hub vs Active Test) ---
  showHubView() {
    this.currentView = 'hub';
    document.getElementById('hubViewContainer').style.display = 'flex';
    document.getElementById('cbtContainer').style.display = 'none';
    document.getElementById('btnViewHub').classList.add('active');
    document.getElementById('btnViewTest').classList.remove('active');
    this.renderHubCards();
    this.updateTimerDisplay();
  }

  showTestView() {
    this.currentView = 'test';
    document.getElementById('hubViewContainer').style.display = 'none';
    document.getElementById('cbtContainer').style.display = 'grid';
    document.getElementById('btnViewHub').classList.remove('active');
    document.getElementById('btnViewTest').classList.add('active');
    this.updateTimerDisplay();
  }

  // --- Header Tabs Rendering ---
  renderTabs() {
    const container = document.getElementById('testTabsList');
    if (!container) return;
    container.innerHTML = '';

    Object.values(MOCK_TESTS).forEach(test => {
      const state = this.testStates[test.id];
      const btn = document.createElement('button');
      btn.className = `test-tab-btn ${test.id === this.activeTestId ? 'active' : ''}`;
      
      let badgeText = '100 Q';
      if (state.submitted && state.results) {
        badgeText = `${state.results.netScore.toFixed(1)}/100`;
      } else if (state.started) {
        const attempted = state.answers.filter(a => a !== null).length;
        badgeText = `${attempted}/100`;
      }

      btn.innerHTML = `
        <span class="tab-icon">${test.icon}</span>
        <span class="tab-title">${test.shortTitle}</span>
        <span class="tab-badge">${badgeText}</span>
      `;

      btn.addEventListener('click', () => {
        sound.click();
        this.switchTest(test.id);
      });

      container.appendChild(btn);
    });
  }

  // --- Hub Cards Rendering ---
  renderHubCards() {
    const grid = document.getElementById('testsCardsGrid');
    if (!grid) return;
    grid.innerHTML = '';

    Object.values(MOCK_TESTS).forEach(test => {
      const state = this.testStates[test.id];
      const attempted = state.answers.filter(a => a !== null).length;
      let statusClass = 'ready';
      let statusText = 'Ready to Start';

      if (state.submitted) {
        statusClass = 'completed';
        statusText = `Completed (${state.results ? state.results.netScore.toFixed(1) : 0} M)`;
      } else if (state.started) {
        statusClass = 'inprogress';
        statusText = `In Progress (${attempted}/100 Qs)`;
      }

      const card = document.createElement('div');
      card.className = 'test-card';
      card.innerHTML = `
        <div class="test-card-header">
          <div class="card-icon-badge">${test.icon}</div>
          <span class="card-status-pill ${statusClass}">${statusText}</span>
        </div>
        <h3>${test.title}</h3>
        <p>${test.description}</p>
        <div class="test-card-meta">
          <div class="meta-col"><span>Questions</span><strong>100 Qs</strong></div>
          <div class="meta-col"><span>Duration</span><strong>${test.durationMinutes} Mins</strong></div>
          <div class="meta-col"><span>Marking</span><strong>+1 / -0.33</strong></div>
        </div>
        <div class="test-card-actions">
          <button class="btn-card-start" onclick="${state.submitted ? `app.showScorecard('${test.id}')` : (state.started ? `app.switchTest('${test.id}')` : `app.startMockTest('${test.id}')`)}">
            ${state.submitted ? '📊 View Scorecard' : (state.started ? `▶️ Resume Test (${Math.floor(state.secondsLeft/60)}m left)` : '▶️ Start Mock Test')}
          </button>
          ${state.submitted ? `<button class="btn-card-score" onclick="app.retakeTestFromHub('${test.id}')" title="Restart this test">🔄 Retake</button>` : ''}
        </div>
      `;
      grid.appendChild(card);
    });
  }

  retakeTestFromHub(testId) {
    if (!confirm(`Are you sure you want to reset and retake ${MOCK_TESTS[testId].title}? All previous answers will be cleared.`)) return;
    this.testStates[testId] = this.getInitialState(testId);
    this.saveActiveState();
    this.startMockTest(testId);
  }

  // --- Section Filter Dropdown ---
  populateSectionDropdown() {
    const select = document.getElementById('sectionFilterSelect');
    if (!select) return;
    select.innerHTML = '<option value="-1">All Topics (1 - 100)</option>';

    const testData = this.getActiveData();
    const topicsMap = new Map();

    testData.questions.forEach((q, idx) => {
      if (!topicsMap.has(q.topic)) {
        topicsMap.set(q.topic, idx);
      }
    });

    topicsMap.forEach((firstIdx, topic) => {
      const opt = document.createElement('option');
      opt.value = firstIdx;
      opt.textContent = `${topic} (from Q${firstIdx + 1})`;
      select.appendChild(opt);
    });
  }

  // --- Question Rendering ---
  renderCurrentQuestion() {
    const state = this.getActiveState();
    const testData = this.getActiveData();
    const qData = testData.questions[state.currentIndex];

    // Meta elements
    document.getElementById('qTopicBadge').textContent = qData.topic || testData.title;
    document.getElementById('qCurrentNum').textContent = state.currentIndex + 1;
    document.getElementById('qTotalNum').textContent = testData.questions.length;
    document.getElementById('questionText').textContent = qData.q;

    // Show or hide Test Start Banner
    const startBanner = document.getElementById('testStartBanner');
    if (!state.started && !state.submitted) {
      if (startBanner) {
        startBanner.style.display = 'flex';
        startBanner.innerHTML = `
          <div class="start-banner-info">
            <h4>Ready to start ${testData.title}?</h4>
            <p>100 Questions · 90 Minutes · The timer will turn ON only when you click Start Test!</p>
          </div>
          <button class="btn-start-banner" onclick="app.startMockTest('${this.activeTestId}')">
            ▶️ Start Mock Test (Turn Timer On)
          </button>
        `;
      }
    } else {
      if (startBanner) startBanner.style.display = 'none';
    }

    // Render options
    const container = document.getElementById('optionsContainer');
    container.innerHTML = '';
    const letters = ['A', 'B', 'C', 'D'];
    const currentAns = state.answers[state.currentIndex];

    qData.options.forEach((optText, optIdx) => {
      const item = document.createElement('div');
      item.className = `option-item ${currentAns === optIdx ? 'selected' : ''}`;
      item.innerHTML = `
        <div class="opt-prefix">${letters[optIdx]}</div>
        <div class="opt-text">${optText}</div>
      `;

      item.addEventListener('click', () => {
        sound.select();
        this.selectOption(optIdx);
      });

      container.appendChild(item);
    });

    // Update Mark for Review Button text
    const revBtn = document.getElementById('btnReview');
    if (state.status[state.currentIndex] === 'marked-review' || state.status[state.currentIndex] === 'answered-review') {
      revBtn.innerHTML = '★ Marked for Review';
      revBtn.style.background = 'var(--warning)';
      revBtn.style.color = '#ffffff';
    } else {
      revBtn.innerHTML = 'Mark for Review';
      revBtn.style.background = '';
      revBtn.style.color = '';
    }
  }

  selectOption(optIdx) {
    const state = this.getActiveState();
    if (!state.started) {
      state.started = true;
      const startBanner = document.getElementById('testStartBanner');
      if (startBanner) startBanner.style.display = 'none';
      this.updateTimerDisplay();
    }
    state.answers[state.currentIndex] = optIdx;
    
    // If it was already marked for review, keep it answered-review
    if (state.status[state.currentIndex] === 'marked-review' || state.status[state.currentIndex] === 'answered-review') {
      state.status[state.currentIndex] = 'answered-review';
    } else {
      state.status[state.currentIndex] = 'answered';
    }

    this.saveActiveState();
    this.renderCurrentQuestion();
    this.updatePaletteAndLegend();
    this.renderTabs();
  }

  // --- Palette & Legend Counters ---
  updatePaletteAndLegend() {
    const state = this.getActiveState();
    const testData = this.getActiveData();
    const grid = document.getElementById('paletteGrid');
    if (!grid) return;
    grid.innerHTML = '';

    let cntAns = 0;
    let cntNotAns = 0;
    let cntRev = 0;
    let cntAnsRev = 0;
    let cntNotVis = 0;

    testData.questions.forEach((_, idx) => {
      const st = state.status[idx];
      const isCurrent = idx === state.currentIndex;

      if (st === 'answered') cntAns++;
      else if (st === 'not-answered') cntNotAns++;
      else if (st === 'marked-review') cntRev++;
      else if (st === 'answered-review') cntAnsRev++;
      else cntNotVis++;

      const btn = document.createElement('button');
      btn.className = `p-btn ${st} ${isCurrent ? 'current' : ''}`;
      btn.textContent = idx + 1;

      btn.addEventListener('click', () => {
        sound.click();
        this.jumpToQuestion(idx);
      });

      grid.appendChild(btn);
    });

    // Update Legend counters
    document.getElementById('cntAns').textContent = cntAns;
    document.getElementById('cntNotAns').textContent = cntNotAns;
    document.getElementById('cntReview').textContent = cntRev;
    document.getElementById('cntAnsReview').textContent = cntAnsRev;
    document.getElementById('cntNotVisited').textContent = cntNotVis;
  }

  // --- Navigation Controls ---
  jumpToQuestion(targetIdx) {
    const state = this.getActiveState();
    if (targetIdx < 0 || targetIdx >= this.getActiveData().questions.length) return;

    // If current was not visited, update to not-answered unless answered
    if (state.status[state.currentIndex] === 'not-visited') {
      state.status[state.currentIndex] = 'not-answered';
    }

    state.currentIndex = targetIdx;
    if (state.status[targetIdx] === 'not-visited') {
      state.status[targetIdx] = 'not-answered';
    }

    this.saveActiveState();
    this.renderCurrentQuestion();
    this.updatePaletteAndLegend();
  }

  prevQuestion() {
    sound.next();
    const state = this.getActiveState();
    if (state.currentIndex > 0) {
      this.jumpToQuestion(state.currentIndex - 1);
    }
  }

  clearResponse() {
    sound.click();
    const state = this.getActiveState();
    state.answers[state.currentIndex] = null;
    if (state.status[state.currentIndex] === 'answered-review') {
      state.status[state.currentIndex] = 'marked-review';
    } else {
      state.status[state.currentIndex] = 'not-answered';
    }
    this.saveActiveState();
    this.renderCurrentQuestion();
    this.updatePaletteAndLegend();
    this.renderTabs();
  }

  toggleMarkForReview() {
    sound.click();
    const state = this.getActiveState();
    const currentAns = state.answers[state.currentIndex];
    const currentStatus = state.status[state.currentIndex];

    if (currentStatus === 'marked-review' || currentStatus === 'answered-review') {
      // Toggle off
      state.status[state.currentIndex] = currentAns !== null ? 'answered' : 'not-answered';
    } else {
      // Toggle on
      state.status[state.currentIndex] = currentAns !== null ? 'answered-review' : 'marked-review';
    }

    this.saveActiveState();
    // Advance to next question after marking for review
    const total = this.getActiveData().questions.length;
    if (state.currentIndex < total - 1) {
      this.jumpToQuestion(state.currentIndex + 1);
    } else {
      this.renderCurrentQuestion();
      this.updatePaletteAndLegend();
    }
  }

  saveAndNext() {
    sound.next();
    const state = this.getActiveState();
    const total = this.getActiveData().questions.length;

    if (state.answers[state.currentIndex] !== null) {
      if (state.status[state.currentIndex] !== 'answered-review') {
        state.status[state.currentIndex] = 'answered';
      }
    } else {
      if (state.status[state.currentIndex] !== 'marked-review') {
        state.status[state.currentIndex] = 'not-answered';
      }
    }

    if (state.currentIndex < total - 1) {
      this.jumpToQuestion(state.currentIndex + 1);
    } else {
      this.saveActiveState();
      this.renderCurrentQuestion();
      this.updatePaletteAndLegend();
      this.openSubmitConfirmModal();
    }
  }

  // --- Timer Loop ---
  startTimerLoop() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    this.timerInterval = setInterval(() => {
      // ONLY decrement timer when candidate is inside test view AND test has been started!
      if (this.currentView !== 'test') return;
      const state = this.getActiveState();
      if (!state || !state.started || state.submitted) return;

      if (state.secondsLeft > 0) {
        state.secondsLeft--;
        this.updateTimerDisplay();
        if (state.secondsLeft % 10 === 0) {
          this.saveActiveState();
        }
      } else {
        // Time expired! Auto submit
        this.autoSubmitDueToTime();
      }
    }, 1000);
  }

  updateTimerDisplay() {
    const state = this.getActiveState();
    const timerElem = document.getElementById('timerVal');
    const timerBox = document.getElementById('timerBox');
    if (!timerElem || !timerBox) return;
    const timerLabel = timerBox.querySelector('.timer-label');

    if (state.submitted) {
      timerElem.textContent = 'COMPLETED';
      if (timerLabel) timerLabel.textContent = 'Status';
      timerBox.classList.remove('warning');
      return;
    }

    if (!state.started) {
      const mins = Math.floor(state.secondsLeft / 60);
      const secs = state.secondsLeft % 60;
      timerElem.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      if (timerLabel) timerLabel.textContent = 'Time Limit (Not Started)';
      timerBox.classList.remove('warning');
      return;
    }

    // When on Hub view, timer is paused
    if (this.currentView === 'hub') {
      const mins = Math.floor(state.secondsLeft / 60);
      const secs = state.secondsLeft % 60;
      timerElem.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      if (timerLabel) timerLabel.textContent = 'Timer Paused (On Hub)';
      timerBox.classList.remove('warning');
      return;
    }

    // Active test in progress
    if (timerLabel) timerLabel.textContent = 'Time Remaining';
    const mins = Math.floor(state.secondsLeft / 60);
    const secs = state.secondsLeft % 60;
    const str = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    timerElem.textContent = str;

    if (state.secondsLeft <= 600) { // under 10 minutes
      timerBox.classList.add('warning');
    } else {
      timerBox.classList.remove('warning');
    }
  }

  autoSubmitDueToTime() {
    alert('Time has expired! Submitting your test automatically.');
    this.processFinalSubmission();
  }

  // --- Submission & Evaluation ---
  openSubmitConfirmModal() {
    const state = this.getActiveState();
    if (state.submitted) {
      this.showScorecard(this.activeTestId);
      return;
    }

    const testData = this.getActiveData();
    let ansCount = 0;
    let notAnsCount = 0;
    let revCount = 0;
    let notVisCount = 0;

    testData.questions.forEach((_, idx) => {
      const st = state.status[idx];
      if (st === 'answered' || st === 'answered-review') ansCount++;
      else if (st === 'not-answered') notAnsCount++;
      else if (st === 'marked-review') revCount++;
      else notVisCount++;
    });

    document.getElementById('modalTotalQ').textContent = testData.questions.length;
    document.getElementById('modalAnsQ').textContent = ansCount;
    document.getElementById('modalNotAnsQ').textContent = notAnsCount + notVisCount;
    document.getElementById('modalReviewQ').textContent = revCount;

    document.getElementById('submitConfirmModal').classList.add('active');
  }

  closeSubmitConfirmModal() {
    document.getElementById('submitConfirmModal').classList.remove('active');
  }

  confirmFinalSubmit() {
    this.closeSubmitConfirmModal();
    this.processFinalSubmission();
  }

  processFinalSubmission() {
    sound.submit();
    const state = this.getActiveState();
    const testData = this.getActiveData();

    let correct = 0;
    let incorrect = 0;
    let unattempted = 0;
    const topicStats = {};

    testData.questions.forEach((q, idx) => {
      const userAns = state.answers[idx];
      const topic = q.topic || 'General';

      if (!topicStats[topic]) {
        topicStats[topic] = { total: 0, attempted: 0, correct: 0, marks: 0 };
      }
      topicStats[topic].total++;

      if (userAns === null) {
        unattempted++;
      } else if (userAns === q.correct) {
        correct++;
        topicStats[topic].attempted++;
        topicStats[topic].correct++;
        topicStats[topic].marks += testData.marksPerCorrect;
      } else {
        incorrect++;
        topicStats[topic].attempted++;
        topicStats[topic].marks -= testData.negativeMarks;
      }
    });

    const netScore = Math.max(0, (correct * testData.marksPerCorrect) - (incorrect * testData.negativeMarks));
    const attemptedTotal = correct + incorrect;
    const accuracy = attemptedTotal > 0 ? (correct / attemptedTotal) * 100 : 0;

    state.results = {
      netScore: parseFloat(netScore.toFixed(2)),
      correctCount: correct,
      incorrectCount: incorrect,
      unattemptedCount: unattempted,
      accuracy: parseFloat(accuracy.toFixed(1)),
      attemptedTotal: attemptedTotal,
      topicStats: topicStats,
      submittedAt: new Date().toISOString()
    };

    state.submitted = true;
    this.saveActiveState();
    this.renderTabs();
    this.updateTimerDisplay();

    // Show Scorecard Modal
    this.showScorecard(this.activeTestId);
  }

  // --- Scorecard & Diagnostics Rendering ---
  showScorecard(testId) {
    const state = this.testStates[testId];
    if (!state || !state.results) return;

    const testData = MOCK_TESTS[testId];
    const res = state.results;

    document.getElementById('scorecardTestTitle').textContent = `${testData.title} — Performance Report`;
    document.getElementById('scoreNet').textContent = res.netScore.toFixed(2);
    document.getElementById('scoreCorrect').textContent = res.correctCount;
    document.getElementById('scoreIncorrect').textContent = res.incorrectCount;
    document.getElementById('scoreAccuracy').textContent = `${res.accuracy.toFixed(1)}%`;
    document.getElementById('scoreUnattempted').textContent = res.unattemptedCount;

    // Render topic breakdown table
    const tableBody = document.getElementById('diagTableBody');
    tableBody.innerHTML = '';

    Object.entries(res.topicStats).forEach(([topic, stats]) => {
      const topicAcc = stats.attempted > 0 ? ((stats.correct / stats.attempted) * 100).toFixed(1) : '0.0';
      const row = document.createElement('tr');
      row.innerHTML = `
        <td style="font-weight:600">${topic}</td>
        <td>${stats.total}</td>
        <td>${stats.attempted}</td>
        <td style="color:var(--success);font-weight:700">${stats.correct}</td>
        <td>${topicAcc}%</td>
        <td style="font-weight:700">${stats.marks.toFixed(2)}</td>
      `;
      tableBody.appendChild(row);
    });

    // Render Solutions
    this.renderSolutionsList(testId);

    document.getElementById('scorecardModal').classList.add('active');
  }

  closeScorecard() {
    document.getElementById('scorecardModal').classList.remove('active');
  }

  setSolutionFilter(filter) {
    this.solFilter = filter;
    document.querySelectorAll('.r-chip').forEach(c => {
      c.classList.toggle('active', c.dataset.filter === filter);
    });
    this.renderSolutionsList(this.activeTestId);
  }

  renderSolutionsList(testId) {
    const testData = MOCK_TESTS[testId];
    const state = this.testStates[testId];
    const container = document.getElementById('solutionsListContainer');
    container.innerHTML = '';
    const letters = ['A', 'B', 'C', 'D'];

    testData.questions.forEach((q, idx) => {
      const userAns = state.answers[idx];
      const isCorrect = userAns === q.correct;
      const isSkipped = userAns === null;

      if (this.solFilter === 'correct' && !isCorrect) return;
      if (this.solFilter === 'wrong' && (isCorrect || isSkipped)) return;
      if (this.solFilter === 'skipped' && !isSkipped) return;

      let cardClass = 'skipped-ans';
      let badgeClass = 'skipped';
      let badgeText = 'Unattempted';

      if (!isSkipped) {
        if (isCorrect) {
          cardClass = 'correct-ans';
          badgeClass = 'correct';
          badgeText = '✓ Correct (+1.0)';
        } else {
          cardClass = 'wrong-ans';
          badgeClass = 'wrong';
          badgeText = '✗ Incorrect (-0.33)';
        }
      }

      const userChoiceText = isSkipped ? 'None Selected' : `${letters[userAns]}: ${q.options[userAns]}`;
      const correctChoiceText = `${letters[q.correct]}: ${q.options[q.correct]}`;

      const card = document.createElement('div');
      card.className = `sol-card ${cardClass}`;
      card.innerHTML = `
        <div class="sol-header">
          <span style="font-weight:700;color:var(--text-muted)">Q${idx + 1} · ${q.topic}</span>
          <span class="sol-badge ${badgeClass}">${badgeText}</span>
        </div>
        <div class="sol-qtext">${q.q}</div>
        <div class="sol-answer-box">
          <div><span style="color:var(--text-muted)">Your Answer:</span> <strong>${userChoiceText}</strong></div>
          <div><span style="color:var(--success)">Correct Answer:</span> <strong style="color:var(--success)">${correctChoiceText}</strong></div>
        </div>
        <div class="sol-exp-box">
          <strong>Explanation:</strong> ${q.exp}
        </div>
      `;
      container.appendChild(card);
    });
  }

  restartActiveTest() {
    if (!confirm('Are you sure you want to restart this test? All answers and scores for this subject will be reset.')) return;
    this.testStates[this.activeTestId] = this.getInitialState(this.activeTestId);
    this.saveActiveState();
    this.closeScorecard();
    this.switchTest(this.activeTestId);
  }

  printScorecard() {
    window.print();
  }

  // --- Keyboard Shortcuts & Event Listeners ---
  setupEventListeners() {
    // Top Bar Actions
    document.getElementById('btnSubmitTop').addEventListener('click', () => {
      const state = this.getActiveState();
      if (state.submitted) {
        this.showScorecard(this.activeTestId);
      } else {
        this.openSubmitConfirmModal();
      }
    });

    document.getElementById('btnSubmitPalette').addEventListener('click', () => {
      this.openSubmitConfirmModal();
    });

    document.getElementById('btnPrev').addEventListener('click', () => this.prevQuestion());
    document.getElementById('btnClear').addEventListener('click', () => this.clearResponse());
    document.getElementById('btnReview').addEventListener('click', () => this.toggleMarkForReview());
    document.getElementById('btnSaveNext').addEventListener('click', () => this.saveAndNext());

    // Section Dropdown
    document.getElementById('sectionFilterSelect').addEventListener('change', (e) => {
      const val = parseInt(e.target.value);
      if (val >= 0) this.jumpToQuestion(val);
    });

    // View Toggles
    document.getElementById('btnViewHub').addEventListener('click', () => this.showHubView());
    document.getElementById('btnViewTest').addEventListener('click', () => this.showTestView());

    // Sound Toggle
    const btnSound = document.getElementById('btnSound');
    btnSound.addEventListener('click', () => {
      sound.enabled = !sound.enabled;
      btnSound.innerHTML = sound.enabled ? '🔊' : '🔇';
      btnSound.title = sound.enabled ? 'Mute Sound' : 'Enable Sound';
    });

    // Fullscreen Toggle
    document.getElementById('btnFullscreen').addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    });

    // Instructions Modal
    document.getElementById('btnInstructions').addEventListener('click', () => {
      document.getElementById('instructionsModal').classList.add('active');
    });

    // Keyboard Shortcuts (1-4 for options, Alt+N for next, Alt+P for prev)
    window.addEventListener('keydown', (e) => {
      // Don't intercept if an input is focused or a modal is active
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

      if (e.key >= '1' && e.key <= '4') {
        const opt = parseInt(e.key) - 1;
        this.selectOption(opt);
      } else if (e.key.toLowerCase() === 'a') {
        this.selectOption(0);
      } else if (e.key.toLowerCase() === 'b') {
        this.selectOption(1);
      } else if (e.key.toLowerCase() === 'c') {
        this.selectOption(2);
      } else if (e.key.toLowerCase() === 'd') {
        this.selectOption(3);
      } else if (e.altKey && e.key.toLowerCase() === 'n') {
        e.preventDefault();
        this.saveAndNext();
      } else if (e.altKey && e.key.toLowerCase() === 'p') {
        e.preventDefault();
        this.prevQuestion();
      } else if (e.altKey && e.key.toLowerCase() === 'm') {
        e.preventDefault();
        this.toggleMarkForReview();
      }
    });
  }

  setupTheme() {
    const btn = document.getElementById('btnTheme');
    const saved = localStorage.getItem('rrb_theme') || 'light';
    if (saved === 'dark') {
      document.body.classList.add('dark-mode');
      btn.innerHTML = '☀️';
    }

    btn.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      const isDark = document.body.classList.contains('dark-mode');
      btn.innerHTML = isDark ? '☀️' : '🌙';
      localStorage.setItem('rrb_theme', isDark ? 'dark' : 'light');
    });
  }
}

// Global App Instance
let app;
window.addEventListener('DOMContentLoaded', () => {
  app = new RRBApp();
});

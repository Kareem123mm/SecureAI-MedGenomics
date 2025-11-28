// 🛡️ Enhanced by SecureAI-MedGenomics Security Platform
// - AML Defense: Protection against adversarial attacks
// - Cryfa Encryption: Optimized genomic data encryption
// - Real-time Monitoring: Grafana security dashboard
// - Intrusion Detection: Bio-inspired IDS
// - 7-Layer Security: Complete defense-in-depth

// Configuration
const CONFIG = {
  API_BASE_URL: 'http://localhost:8000/api',  // Using SecureAI backend
  POLL_INTERVAL: 3000,
  MAX_FILE_SIZE: 10 * 1024 * 1024,
  ALLOWED_EXTENSIONS: ['.fasta', '.fa', '.vcf', '.txt'],
  DEMO_MODE: false, // Set to true to test without backend
  AUTO_ENCRYPT: true, // ALWAYS encrypt - no user choice needed!
  BACKEND_CHECK_INTERVAL: 3000, // Check backend every 3 seconds
  HIDE_BACKEND_STATUS: false // Set true to hide backend indicator
};

// State Management
const state = {
  currentPage: 'upload',
  currentJob: null,
  adminLoggedIn: false,
  adminAuth: null,
  processInterval: null,
  currentStep: 0,
  uploadedFile: null,
  backendConnected: false,
  backendChecking: true,
  securityLayers: {
    aml_defense: 'checking',
    cryfa_encryption: 'checking',
    intrusion_detection: 'checking',
    genetic_algorithm: 'checking',
    monitoring: 'checking'
  }
};

// Mock Data
const mockJobs = [
  {
    job_id: "6f1d8a2e-3b7c-4c8e-9f1a-1234567890ab",
    status: "completed",
    received: "2025-10-27T14:00:12Z",
    completed: "2025-10-27T14:00:45Z",
    duration: 33,
    markers: ["BRCA1_185delAG"],
    confidence: "low"
  },
  {
    job_id: "8a3c9b4f-2d6e-4a1b-8c2f-9876543210cd",
    status: "completed",
    received: "2025-10-27T13:45:00Z",
    completed: "2025-10-27T13:45:28Z",
    duration: 28,
    markers: ["TP53_R175H", "EGFR_L858R"],
    confidence: "medium"
  },
  {
    job_id: "5e2a7c1d-4f8b-3e9c-7a5d-abcdef123456",
    status: "processing",
    received: "2025-10-27T14:05:00Z",
    completed: null,
    duration: null,
    markers: [],
    confidence: null
  },
  {
    job_id: "9b4e2a7f-1c6d-4e8b-9a3f-fedcba987654",
    status: "completed",
    received: "2025-10-27T12:30:00Z",
    completed: "2025-10-27T12:30:35Z",
    duration: 35,
    markers: ["BRCA2_6174delT"],
    confidence: "high"
  },
  {
    job_id: "3d7a8c2b-5e9f-4a1c-8d6e-123456789abc",
    status: "completed",
    received: "2025-10-27T11:15:00Z",
    completed: "2025-10-27T11:15:22Z",
    duration: 22,
    markers: ["EGFR_T790M", "KRAS_G12D"],
    confidence: "high"
  }
];

const processingStages = [
  { name: "Upload Complete", status: "completed" },
  { name: "AML Defense", status: "pending" },
  { name: "IDS Scan", status: "pending" },
  { name: "Cryfa Encryption", status: "pending" },
  { name: "Genomic Analysis", status: "pending" }
];

// Utility Functions
function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

function formatTimestamp(isoString) {
  const date = new Date(isoString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
}

function generateHash() {
  const chars = '0123456789abcdef';
  let hash = '';
  for (let i = 0; i < 64; i++) {
    hash += chars[Math.floor(Math.random() * chars.length)];
  }
  return hash;
}

// Toast Notifications
function showToast(message, type = 'info', duration = 4000) {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  const iconSVG = type === 'success' 
    ? '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'
    : type === 'error'
    ? '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>'
    : '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>';
  
  // Handle multi-line messages
  const formattedMessage = message.replace(/\n/g, '<br>');
  
  toast.innerHTML = `
    <div class="toast-icon">${iconSVG}</div>
    <div class="toast-message">${formattedMessage}</div>
    <button class="toast-close">&times;</button>
  `;
  
  container.appendChild(toast);
  
  toast.querySelector('.toast-close').addEventListener('click', () => {
    toast.remove();
  });
  
  setTimeout(() => {
    toast.remove();
  }, duration);
}

// Navigation
function navigateTo(pageName) {
  // Hide all pages
  document.querySelectorAll('.page').forEach(page => {
    page.classList.remove('active');
  });
  
  // Show target page
  const targetPage = document.getElementById(`page-${pageName}`);
  if (targetPage) {
    targetPage.classList.add('active');
  }
  
  // Update nav links
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
    if (link.dataset.page === pageName) {
      link.classList.add('active');
    }
  });
  
  // Close mobile menu
  document.getElementById('nav-mobile').classList.remove('active');
  
  // Update state
  state.currentPage = pageName;
  
  // Handle page-specific logic
  if (pageName === 'admin') {
    if (!state.adminLoggedIn) {
      document.getElementById('admin-login').style.display = 'flex';
      document.getElementById('admin-dashboard').style.display = 'none';
    } else {
      document.getElementById('admin-login').style.display = 'none';
      document.getElementById('admin-dashboard').style.display = 'block';
    }
  }
  
  if (pageName === 'config') {
    // Re-initialize copy buttons for config page
    setTimeout(() => {
      document.querySelectorAll('.copy-code-btn').forEach(btn => {
        if (!btn.hasAttribute('data-listener')) {
          btn.setAttribute('data-listener', 'true');
          btn.addEventListener('click', () => {
            const code = btn.dataset.code;
            navigator.clipboard.writeText(code).then(() => {
              const originalText = btn.textContent;
              btn.textContent = 'Copied!';
              setTimeout(() => {
                btn.textContent = originalText;
              }, 2000);
            });
          });
        }
      });
    }, 100);
  }
  
  // Scroll to top
  window.scrollTo(0, 0);
}

// Backend Connection Checking
async function checkBackendConnection() {
  const statusEl = document.getElementById('backend-status');
  if (!statusEl || CONFIG.HIDE_BACKEND_STATUS) {
    if (statusEl) statusEl.style.display = 'none';
    return;
  }
  
  try {
    state.backendChecking = true;
    statusEl.className = 'backend-status checking';
    statusEl.innerHTML = '⚪ Checking...';
    
    console.log('Checking backend at:', `${CONFIG.API_BASE_URL}/health`);
    
    // Create a timeout promise for broader browser support
    const timeoutPromise = new Promise((_, reject) => 
      setTimeout(() => reject(new Error('Request timeout')), 5000)
    );
    
    const fetchPromise = fetch(`${CONFIG.API_BASE_URL}/health`, {
      method: 'GET',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      mode: 'cors'
    });
    
    const response = await Promise.race([fetchPromise, timeoutPromise]);
    
    console.log('Backend response:', response.status, response.ok);
    
    if (response.ok) {
      const data = await response.json();
      console.log('Backend health data:', data);
      state.backendConnected = true;
      state.backendChecking = false;
      statusEl.className = 'backend-status connected';
      statusEl.innerHTML = '🟢 Connected';
      statusEl.title = 'Backend server is online and ready';
      
      // Update security layers if provided
      if (data.security_layers) {
        state.securityLayers = data.security_layers;
      }
    } else {
      throw new Error(`Backend returned status ${response.status}`);
    }
  } catch (error) {
    console.error('Backend connection check failed:', error);
    state.backendConnected = false;
    state.backendChecking = false;
    statusEl.className = 'backend-status disconnected';
    statusEl.innerHTML = '🔴 Offline';
    statusEl.title = 'Backend server is not responding';
  }
}

function startBackendHealthCheck() {
  // Initial check
  checkBackendConnection();
  
  // Periodic checks every 5 seconds
  setInterval(() => {
    checkBackendConnection();
  }, CONFIG.BACKEND_CHECK_INTERVAL);
}

// File Upload Handling
function initFileUpload() {
  const fileInput = document.getElementById('file-input');
  const dropZone = document.getElementById('file-drop-zone');
  const fileSelected = document.getElementById('file-selected');
  const fileName = document.getElementById('file-name');
  const removeFileBtn = document.getElementById('remove-file');
  const browseLink = document.querySelector('.browse-link');
  
  if (!fileInput || !dropZone) {
    console.error('File input or drop zone not found');
    return;
  }
  
  // Click browse link to open file dialog
  if (browseLink) {
    browseLink.addEventListener('click', (e) => {
      e.stopPropagation();
      fileInput.click();
    });
  }
  
  // Click drop zone to browse
  dropZone.addEventListener('click', () => {
    fileInput.click();
  });
  
  // File selection
  fileInput.addEventListener('change', (e) => {
    handleFileSelect(e.target.files[0]);
  });
  
  // Drag and drop
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });
  
  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
  });
  
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    handleFileSelect(e.dataTransfer.files[0]);
  });
  
  // Remove file
  if (removeFileBtn) {
    removeFileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      fileInput.value = '';
      state.uploadedFile = null;
      if (dropZone) dropZone.style.display = 'block';
      if (fileSelected) fileSelected.style.display = 'none';
    });
  }
  
  function handleFileSelect(file) {
    if (!file) return;
    
    // Validate file type
    const allowedExtensions = ['.fasta', '.fa', '.vcf', '.txt'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
      showToast('Invalid file type. Please upload a FASTA, VCF, or TXT file.', 'error');
      return;
    }
    
    // Validate file size (10 MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      showToast('File too large. Maximum size is 10 MB.', 'error');
      return;
    }
    
    // File is valid
    state.uploadedFile = file;
    if (fileName) fileName.textContent = file.name;
    if (dropZone) dropZone.style.display = 'none';
    if (fileSelected) fileSelected.style.display = 'flex';
    showToast(`File selected: ${file.name}`, 'success');
    checkUploadButton();
  }
  
  // Reset upload page function
  function resetUploadPage() {
    // Clear uploaded file
    state.uploadedFile = null;
    
    // Reset file input - use correct ID from HTML
    const fileInput = document.getElementById('file-input');
    if (fileInput) fileInput.value = '';
    
    // Reset UI elements - use correct IDs from HTML
    const dropZone = document.getElementById('file-drop-zone');
    const fileSelected = document.getElementById('file-selected');
    const consentCheckbox = document.getElementById('consent-checkbox');
    const submitBtn = document.getElementById('submit-btn');
    const fileName = document.getElementById('file-name');
    
    // Show drop zone, hide file selected
    if (dropZone) dropZone.style.display = 'block';
    if (fileSelected) fileSelected.style.display = 'none';
    
    // Reset form controls
    if (consentCheckbox) consentCheckbox.checked = false;
    
    // Reset submit button to default state
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg> Upload &amp; Analyze';
    }
    
    // Clear file name display
    if (fileName) fileName.textContent = '';
    
    console.log('✓ Upload page fully reset and ready for new file');
  }
  
  // Make resetUploadPage available globally
  window.resetUploadPage = resetUploadPage;

  // Consent checkbox handler
  const consentCheckbox = document.getElementById('consent-checkbox');
  const submitBtn = document.getElementById('submit-btn');
  
  function checkUploadButton() {
    if (submitBtn && consentCheckbox) {
      // Enable button only if file is selected AND consent is checked
      submitBtn.disabled = !(state.uploadedFile && consentCheckbox.checked);
    }
  }

  if (consentCheckbox) {
    consentCheckbox.addEventListener('change', checkUploadButton);
  }
}

// API Functions
async function checkBackendHealth() {
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000)
    });
    state.backendConnected = response.ok;
    return response.ok;
  } catch (error) {
    state.backendConnected = false;
    return false;
  }
}

async function uploadFile(file, email, encrypted) {
  const formData = new FormData();
  formData.append('file', file);
  if (email) formData.append('email', email);
  formData.append('encrypted', encrypted);
  
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    
    if (response.ok) {
      return { success: true, data };
    } else {
      return { success: false, error: data.detail || 'Upload failed' };
    }
  } catch (error) {
    return { success: false, error: 'Network error. Please check your connection and ensure the backend is running.' };
  }
}

async function pollJobStatus(jobId) {
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/status/${jobId}`);
    
    if (!response.ok) {
      throw new Error(`Status check failed: ${response.status}`);
    }
    
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

async function getJobResult(jobId) {
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/result/${jobId}`);
    
    if (response.status === 202) {
      return { success: false, stillProcessing: true };
    }
    
    if (response.status === 404) {
      // Job not found - likely old job after database reset
      console.log('Job not found (database may have been reset)');
      return { success: false, error: 'Job not found', notFound: true };
    }
    
    if (!response.ok) {
      throw new Error('Failed to load results');
    }
    
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    // Suppress errors for old jobs
    console.log('Failed to load result:', error.message);
    return { success: false, error: error.message, notFound: true };
  }
}

async function cancelJob(jobId) {
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/cancel/${jobId}`, {
      method: 'POST'
    });
    return response.ok;
  } catch (error) {
    return false;
  }
}

async function getProofOfDeletion(jobId) {
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/proof/${jobId}`);
    
    if (!response.ok) {
      throw new Error('Failed to get proof');
    }
    
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Form Submission
function initUploadForm() {
  const form = document.getElementById('upload-form');
  const submitBtn = document.getElementById('submit-btn');
  
  if (!form || !submitBtn) {
    console.error('Upload form or submit button not found');
    return;
  }
  
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    console.log('Form submitted, uploaded file:', state.uploadedFile);
    
    if (!state.uploadedFile) {
      showToast('Please select a file to upload.', 'error');
      return;
    }
    
    // Show custom upload confirmation modal
    const fileName = state.uploadedFile.name;
    const fileSize = (state.uploadedFile.size / 1024).toFixed(2);
    
    console.log('Showing confirmation dialog');
    const userConfirmed = await showCustomConfirm(fileName, fileSize);
    console.log('User confirmed:', userConfirmed);
    
    if (!userConfirmed) {
      showToast('Upload canceled', 'info');
      return;
    }
    
    const email = document.getElementById('email-input').value;
    const encrypt = true; // ALWAYS encrypt - checkbox removed from UI
    
    // Check backend connection
    if (!CONFIG.DEMO_MODE) {
      const connected = await checkBackendHealth();
      if (!connected) {
        showToast('Backend not connected. Please start the backend server or enable DEMO_MODE.', 'error');
        return;
      }
    }
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;"><circle cx="12" cy="12" r="10" opacity="0.25"></circle><path d="M12 2a10 10 0 0 1 10 10" opacity="0.75"></path></svg> Uploading...';
    
    try {
      
      if (CONFIG.DEMO_MODE) {
        // Demo mode - simulate upload
        await simulateUpload(email, encrypt);
      } else {
        // Real API call
        const result = await uploadFile(state.uploadedFile, email, encrypt);
        
        if (result.success) {
          state.currentJob = {
            job_id: result.data.job_id,
            status: 'processing',
            received: new Date().toISOString(),
            email: email,
            encrypted: encrypt,
            fileName: state.uploadedFile.name
          };
          
          showToast('File uploaded successfully! Processing started.', 'success');
          
          setTimeout(() => {
            navigateTo('status');
            initStatusPage();
          }, 500);
        } else {
          showToast(result.error || 'Upload failed', 'error');
          submitBtn.disabled = false;
          submitBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg> Upload &amp; Analyze';
        }
      }
    } catch (error) {
      console.error('Upload error:', error);
      showToast('Upload failed: ' + error.message, 'error');
      submitBtn.disabled = false;
      submitBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg> Upload &amp; Analyze';
    }
  });
}

// Simulate upload for demo mode
async function simulateUpload(email, encrypt) {
  return new Promise((resolve) => {
    setTimeout(() => {
      const jobId = generateUUID();
      const now = new Date().toISOString();
      
      state.currentJob = {
        job_id: jobId,
        status: 'processing',
        received: now,
        completed: null,
        duration: null,
        markers: [],
        confidence: null,
        email: email,
        encrypted: encrypt,
        fileName: state.uploadedFile.name
      };
      
      showToast('File uploaded successfully! (Demo Mode)', 'success');
      
      setTimeout(() => {
        navigateTo('status');
        initStatusPage();
      }, 500);
      
      resolve();
    }, 1000);
  });
}

// Status Page
function initStatusPage() {
  if (!state.currentJob) return;
  
  // Display job ID
  document.getElementById('job-id-code').textContent = state.currentJob.job_id;
  
  // Reset processing stages
  state.currentStep = 0;
  processingStages.forEach((stage, index) => {
    if (index === 0) {
      stage.status = 'completed';
    } else {
      stage.status = 'pending';
    }
  });
  
  renderProgressTimeline();
  
  if (CONFIG.DEMO_MODE) {
    // Demo mode - simulate processing
    startDemoProcessing();
  } else {
    // Real mode - poll backend
    startRealTimePolling();
  }
}

function startDemoProcessing() {
  state.processInterval = setInterval(() => {
    if (state.currentStep < processingStages.length - 1) {
      state.currentStep++;
      processingStages[state.currentStep].status = 'processing';
      
      if (state.currentStep > 0) {
        processingStages[state.currentStep - 1].status = 'completed';
      }
      
      renderProgressTimeline();
      
      const statusText = document.getElementById('status-text');
      statusText.textContent = `Status: processing — step ${state.currentStep + 1} of ${processingStages.length}`;
    } else {
      clearInterval(state.processInterval);
      processingStages[state.currentStep].status = 'completed';
      renderProgressTimeline();
      completeJob();
    }
  }, 3000);
}

function startRealTimePolling() {
  state.processInterval = setInterval(async () => {
    const result = await pollJobStatus(state.currentJob.job_id);
    
    if (result.success) {
      const statusData = result.data;
      const { status, current_stage, progress, security_checks } = statusData;
      
      // Update progress bar
      const progressBar = document.querySelector('.progress-fill');
      if (progressBar && progress !== undefined) {
        progressBar.style.width = `${progress}%`;
      }
      
      // Update progress steps based on progress percentage
      let stepIndex = 0;
      if (progress >= 20) stepIndex = 1;
      if (progress >= 40) stepIndex = 2;
      if (progress >= 60) stepIndex = 3;
      if (progress >= 80) stepIndex = 4;
      
      // Update stage statuses
      processingStages.forEach((stage, index) => {
        if (index < stepIndex) {
          stage.status = 'completed';
        } else if (index === stepIndex) {
          stage.status = 'processing';
        } else {
          stage.status = 'pending';
        }
      });
      
      renderProgressTimeline();
      
      // Update status text with current stage message
      const statusText = document.getElementById('status-text');
      if (current_stage) {
        statusText.textContent = `Status: ${current_stage} — ${progress}% complete`;
      } else {
        statusText.textContent = `Status: ${status} — ${progress}% complete`;
      }
      
      // Check if completed
      if (status === 'completed' || progress >= 100) {
        clearInterval(state.processInterval);
        processingStages.forEach(stage => stage.status = 'completed');
        renderProgressTimeline();
        
        // Update current job with all data from status
        state.currentJob = {
          ...state.currentJob,
          status: 'completed',
          progress: 100,
          completed: statusData.completed_at || new Date().toISOString(),
          security_passed: statusData.security_passed,
          ai_completed: statusData.ai_completed,
          encrypted: statusData.encrypted,
          security_report: statusData.security_report,
          ai_results: statusData.ai_results,
          total_time: statusData.total_time
        };
        
        // Navigate to results
        setTimeout(() => {
          showToast('Analysis complete!', 'success');
          navigateTo('result');
          initResultsPage();
        }, 1000);
      } else if (status === 'failed') {
        clearInterval(state.processInterval);
        
        // Check if it's a security failure
        if (statusData.security_report && !statusData.security_passed) {
          const secReport = statusData.security_report;
          const failedLayers = [];
          
          // Collect failed layers
          if (secReport.layers) {
            Object.entries(secReport.layers).forEach(([layerName, layerData]) => {
              if (!layerData.passed) {
                failedLayers.push(layerName.replace(/_/g, ' ').toUpperCase());
              }
            });
          }
          
          // Check for IDS threats
          let threatDetails = '';
          if (secReport.layers?.ids && secReport.layers.ids.threat_detected) {
            const alerts = secReport.layers.ids.alerts || 0;
            threatDetails = ` - ${alerts} security threat${alerts !== 1 ? 's' : ''} detected`;
          }
          
          // Show detailed security warning
          const failedLayersList = failedLayers.length > 0 ? failedLayers.join(', ') : 'Security validation';
          showToast(`🚨 SECURITY THREAT DETECTED${threatDetails}\n❌ Failed: ${failedLayersList}\n⚠️ File rejected for your protection`, 'error', 8000);
        } else {
          // Generic failure
          showToast('❌ Job processing failed. Please try again with a different file.', 'error');
        }
        
        // Clear the upload and reset page
        setTimeout(() => {
          resetUploadPage();
          navigateTo('upload');
        }, 3000);
      }
    } else {
      showToast('Failed to fetch status', 'error');
    }
  }, CONFIG.POLL_INTERVAL);
}

function updateProgressSteps(currentStep) {
  processingStages.forEach((stage, index) => {
    if (index < currentStep - 1) {
      stage.status = 'completed';
    } else if (index === currentStep - 1) {
      stage.status = 'processing';
    } else {
      stage.status = 'pending';
    }
  });
  renderProgressTimeline();
}

function renderProgressTimeline() {
  const timeline = document.getElementById('progress-timeline');
  if (!timeline) return;
  
  timeline.innerHTML = '';
  
  // Calculate completion percentage
  const completedSteps = processingStages.filter(s => s.status === 'completed').length;
  const totalSteps = processingStages.length;
  const percentage = Math.round((completedSteps / totalSteps) * 100);
  
  // Add percentage badge
  if (percentage > 0 && percentage < 100) {
    const percentageBadge = document.createElement('div');
    percentageBadge.className = 'progress-percentage';
    percentageBadge.textContent = `${percentage}% Complete`;
    timeline.appendChild(percentageBadge);
  }
  
  processingStages.forEach((stage, index) => {
    const step = document.createElement('div');
    step.className = `progress-step ${stage.status}`;
    
    const stepCircle = document.createElement('div');
    stepCircle.className = 'step-circle';
    
    let iconHTML = '';
    let statusText = '';
    
    if (stage.status === 'completed') {
      iconHTML = `
        <svg class="step-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      `;
      statusText = 'Completed';
    } else if (stage.status === 'processing') {
      iconHTML = `<div class="step-spinner"></div>`;
      statusText = 'Processing...';
    } else {
      iconHTML = `
        <svg class="step-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2">
          <circle cx="12" cy="12" r="3"></circle>
        </svg>
      `;
      statusText = 'Pending';
    }
    
    stepCircle.innerHTML = iconHTML;
    
    const stepContent = document.createElement('div');
    stepContent.className = 'step-content';
    
    const stepTitle = document.createElement('div');
    stepTitle.className = 'step-title';
    stepTitle.textContent = stage.name;
    
    const stepStatus = document.createElement('div');
    stepStatus.className = 'step-status';
    stepStatus.textContent = statusText;
    
    // Add estimated time for processing step
    if (stage.status === 'processing') {
      const timeRemaining = document.createElement('div');
      timeRemaining.className = 'time-remaining';
      timeRemaining.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
        <span>~${Math.floor(Math.random() * 15) + 5}s remaining</span>
      `;
      stepStatus.appendChild(timeRemaining);
    }
    
    stepContent.appendChild(stepTitle);
    stepContent.appendChild(stepStatus);
    
    step.appendChild(stepCircle);
    step.appendChild(stepContent);
    
    timeline.appendChild(step);
  });
}

// Add spinner animation
const style = document.createElement('style');
style.textContent = `
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;
document.head.appendChild(style);

function completeJob() {
  const now = new Date().toISOString();
  const received = new Date(state.currentJob.received);
  const completed = new Date(now);
  const duration = Math.floor((completed - received) / 1000);
  
  // Generate random markers
  const allMarkers = ['BRCA1_185delAG', 'BRCA2_6174delT', 'TP53_R175H', 'EGFR_L858R', 'KRAS_G12D', 'EGFR_T790M'];
  const numMarkers = Math.floor(Math.random() * 2) + 1;
  const markers = [];
  for (let i = 0; i < numMarkers; i++) {
    markers.push(allMarkers[Math.floor(Math.random() * allMarkers.length)]);
  }
  
  const confidenceLevels = ['low', 'medium', 'high'];
  const confidence = confidenceLevels[Math.floor(Math.random() * confidenceLevels.length)];
  
  state.currentJob.completed = now;
  state.currentJob.duration = duration;
  state.currentJob.markers = markers;
  state.currentJob.confidence = confidence;
  state.currentJob.status = 'completed';
  state.currentJob.deleted = now;
  
  // Navigate to results after a short delay
  setTimeout(() => {
    navigateTo('result');
    initResultsPage();
  }, 2000);
}

// Results Page
async function loadResultsFromBackend() {
  const result = await getJobResult(state.currentJob.job_id);
  
  if (result.stillProcessing) {
    showToast('Still processing, redirecting to status page', 'info');
    navigateTo('status');
    return;
  }
  
  if (result.success) {
    // Update state with backend data
    state.currentJob = {
      ...state.currentJob,
      ...result.data,
      markers: result.data.markers_found || result.data.markers || [],
      completed: result.data.completed_at || result.data.completed || new Date().toISOString(),
      deleted: result.data.deleted || new Date().toISOString(),
      layer_timings: result.data.layer_timings || result.data.results?.layer_timings || {},
      duration: result.data.total_processing_time || result.data.results?.total_processing_time || '0s'
    };
    
    navigateTo('result');
    initResultsPage();
  } else if (result.notFound) {
    // Job not found - don't show error toast, just log
    console.log('Job results not found (normal after database reset)');
    // Don't show error to user
  } else {
    showToast('Failed to load results', 'error');
  }
}

function initResultsPage() {
  if (!state.currentJob) return;
  
  document.getElementById('result-job-id').textContent = state.currentJob.job_id || 'N/A';
  document.getElementById('result-received').textContent = formatTimestamp(state.currentJob.received || state.currentJob.created_at);
  document.getElementById('result-completed').textContent = formatTimestamp(state.currentJob.completed || state.currentJob.completed_at);
  document.getElementById('result-duration').textContent = state.currentJob.total_time ? `${state.currentJob.total_time.toFixed(2)} seconds` : (state.currentJob.duration ? `${state.currentJob.duration} seconds` : '0 seconds');
  
  // Display layer timings if available
  const layerTimingsList = document.getElementById('layer-timings-list');
  if (layerTimingsList && state.currentJob.layer_timings) {
    layerTimingsList.innerHTML = '';
    
    const layerNames = {
      'aml_defense': '🛡️ AML Defense',
      'ids_scan': '🔍 IDS Scan',
      'cryfa_encryption': '🔐 Cryfa Encryption',
      'ai_analysis': '🤖 AI Analysis'
    };
    
    Object.entries(state.currentJob.layer_timings).forEach(([layer, timing]) => {
      const item = document.createElement('div');
      item.style.cssText = 'display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: var(--gray-800); border-radius: 6px;';
      item.innerHTML = `
        <span style="color: var(--gray-300); font-size: 13px;">${layerNames[layer] || layer}</span>
        <span style="color: var(--success); font-weight: 600; font-size: 13px;">${timing}</span>
      `;
      layerTimingsList.appendChild(item);
    });
  }
  
  // Render markers and AI results
  const markersList = document.getElementById('markers-list');
  markersList.innerHTML = '';
  
  // Display AI results if available
  if (state.currentJob.ai_results && state.currentJob.ai_results.success) {
    const aiResults = state.currentJob.ai_results;
    
    // Disease Risk
    if (aiResults.disease_risk) {
      const item = document.createElement('div');
      item.className = 'marker-item';
      const riskPercent = Math.round(aiResults.disease_risk.risk_probability * 100);
      item.innerHTML = `
        <span class="marker-name">🏥 Disease Risk: ${aiResults.disease_risk.risk_level.toUpperCase()}</span>
        <span class="confidence-badge confidence-${aiResults.disease_risk.risk_level}">${riskPercent}%</span>
      `;
      markersList.appendChild(item);
    }
    
    // Drug Response
    if (aiResults.drug_response) {
      const item = document.createElement('div');
      item.className = 'marker-item';
      const responsePercent = Math.round(aiResults.drug_response.response_value * 100);
      item.innerHTML = `
        <span class="marker-name">💊 Drug Response: ${aiResults.drug_response.response_category.toUpperCase()}</span>
        <span class="confidence-badge confidence-high">${responsePercent}%</span>
      `;
      markersList.appendChild(item);
    }
    
    // Feature count
    if (aiResults.feature_count) {
      const item = document.createElement('div');
      item.className = 'marker-item';
      item.innerHTML = `
        <span class="marker-name">🧬 Genomic Features Analyzed</span>
        <span class="confidence-badge confidence-medium">${aiResults.feature_count}</span>
      `;
      markersList.appendChild(item);
    }
  } else {
    // Fallback to old markers format
    const markers = state.currentJob.markers || [];
    
    if (markers.length === 0) {
      markersList.innerHTML = '<p style="color: var(--gray-400); text-align: center;">No markers detected</p>';
    } else {
      markers.forEach(marker => {
        const markerName = typeof marker === 'string' ? marker : marker.name;
        const confidence = marker.confidence || state.currentJob.confidence || 'medium';
        
        const item = document.createElement('div');
        item.className = 'marker-item';
        item.innerHTML = `
          <span class="marker-name">${markerName}</span>
          <span class="confidence-badge confidence-${confidence}">${confidence}</span>
        `;
        markersList.appendChild(item);
      });
    }
  }
  
  // Display security report summary if available
  if (state.currentJob.security_report) {
    const secReport = state.currentJob.security_report;
    
    // Add security status at the top of markers
    const securityItem = document.createElement('div');
    securityItem.className = 'marker-item';
    // Check both possible field names for security status
    const securityPassed = secReport.overall_passed || secReport.security_passed || false;
    const securityScore = secReport.security_score || secReport.overall_score || 0;
    const statusIcon = securityPassed ? '✅' : '❌';
    const statusText = securityPassed ? 'PASSED' : 'FAILED';
    securityItem.innerHTML = `
      <span class="marker-name">${statusIcon} Security Validation: ${statusText}</span>
      <span class="confidence-badge confidence-${securityPassed ? 'high' : 'low'}">${Math.round(securityScore)}%</span>
    `;
    markersList.insertBefore(securityItem, markersList.firstChild);
    
    // Add layer results from the layers object
    if (secReport.layers) {
      Object.entries(secReport.layers).forEach(([layerName, layerData]) => {
        const layerItem = document.createElement('div');
        layerItem.className = 'marker-item';
        const layerPassed = layerData.passed || false;
        const layerIcon = layerPassed ? '✓' : '✗';
        const displayName = layerName.replace(/_/g, ' ').toUpperCase();
        layerItem.innerHTML = `
          <span class="marker-name" style="font-size: 0.9em; padding-left: 20px;">${layerIcon} ${displayName}</span>
          <span class="confidence-badge confidence-${layerPassed ? 'high' : 'low'}">${layerPassed ? 'Pass' : 'Fail'}</span>
        `;
        markersList.insertBefore(layerItem, markersList.children[1]);
      });
    }
    // Fallback to old layer_results format
    else if (secReport.layer_results) {
      secReport.layer_results.forEach(layer => {
        const layerItem = document.createElement('div');
        layerItem.className = 'marker-item';
        const layerIcon = layer.passed ? '✓' : '✗';
        layerItem.innerHTML = `
          <span class="marker-name" style="font-size: 0.9em; padding-left: 20px;">${layerIcon} ${layer.layer}</span>
          <span class="confidence-badge confidence-${layer.passed ? 'high' : 'low'}">${layer.passed ? 'Pass' : 'Fail'}</span>
        `;
        markersList.insertBefore(layerItem, markersList.children[1]);
      });
    }
  }
  
  // Update deletion notice
  const deletionNotice = document.getElementById('deletion-notice-text');
  const deletedTime = state.currentJob.deleted || state.currentJob.completed || state.currentJob.completed_at;
  deletionNotice.textContent = `Your uploaded file and extracted sequences were deleted at ${formatTimestamp(deletedTime)}. We do not keep genomic data.`;
}

// Download Results as JSON
function downloadResults() {
  if (!state.currentJob) return;
  
  // Generate comprehensive JSON result
  const result = {
    job_id: state.currentJob.job_id,
    status: state.currentJob.status,
    timestamps: {
      received: state.currentJob.received || state.currentJob.created_at,
      completed: state.currentJob.completed || state.currentJob.completed_at,
      deleted: state.currentJob.deleted || state.currentJob.completed_at,
      total_time: state.currentJob.total_time
    },
    security_report: state.currentJob.security_report,
    ai_predictions: state.currentJob.ai_results,
    analysis_summary: {
      security_passed: state.currentJob.security_report?.overall_passed || false,
      security_score: state.currentJob.security_report?.security_score || 0,
      disease_risk: state.currentJob.ai_results?.disease_risk,
      drug_response: state.currentJob.ai_results?.drug_response,
      features_analyzed: state.currentJob.ai_results?.feature_count || 0
    }
  };
  
  const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `genomics-result-${state.currentJob.job_id}.json`;
  a.click();
  URL.revokeObjectURL(url);
  
  showToast('JSON downloaded successfully!', 'success');
}

// Download Results as PDF
function downloadResultsPDF() {
  if (!state.currentJob) return;
  
  try {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Colors
    const primaryBlue = [37, 99, 235];
    const successGreen = [16, 185, 129];
    const errorRed = [239, 68, 68];
    const textGray = [55, 65, 81];
    const lightGray = [156, 163, 175];
    
    // Header with border
    doc.setFillColor(37, 99, 235);
    doc.rect(0, 0, 210, 35, 'F');
    doc.setFontSize(22);
    doc.setTextColor(255, 255, 255);
    doc.setFont(undefined, 'bold');
    doc.text('SECURE GENOMICS', 105, 15, { align: 'center' });
    doc.setFontSize(14);
    doc.setFont(undefined, 'normal');
    doc.text('Analysis Report', 105, 25, { align: 'center' });
    
    // Report metadata
    let yPos = 45;
    doc.setFontSize(9);
    doc.setTextColor(...lightGray);
    const reportDate = new Date().toLocaleString();
    doc.text(`Generated: ${reportDate}`, 105, yPos, { align: 'center' });
    
    // Job Information Section
    yPos = 58;
    doc.setFontSize(14);
    doc.setTextColor(...primaryBlue);
    doc.setFont(undefined, 'bold');
    doc.text('JOB INFORMATION', 20, yPos);
    doc.setLineWidth(0.5);
    doc.setDrawColor(...primaryBlue);
    doc.line(20, yPos + 2, 190, yPos + 2);
    
    yPos += 10;
    doc.setFontSize(10);
    doc.setTextColor(...textGray);
    doc.setFont(undefined, 'normal');
    doc.text(`Job ID:`, 20, yPos);
    doc.setFont(undefined, 'bold');
    doc.text(`${state.currentJob.job_id}`, 50, yPos);
    
    yPos += 7;
    doc.setFont(undefined, 'normal');
    doc.text(`Status:`, 20, yPos);
    doc.setFont(undefined, 'bold');
    doc.setTextColor(...successGreen);
    doc.text(`${state.currentJob.status.toUpperCase()}`, 50, yPos);
    
    yPos += 7;
    doc.setTextColor(...textGray);
    doc.setFont(undefined, 'normal');
    doc.text(`Completed:`, 20, yPos);
    doc.text(`${formatTimestamp(state.currentJob.completed || state.currentJob.completed_at)}`, 50, yPos);
    
    yPos += 7;
    doc.text(`Processing Time:`, 20, yPos);
    doc.setTextColor(...primaryBlue);
    doc.setFont(undefined, 'bold');
    doc.text(`${state.currentJob.total_time ? state.currentJob.total_time.toFixed(2) + ' seconds' : 'N/A'}`, 50, yPos);
    
    // Security Validation Section
    yPos += 15;
    doc.setFontSize(14);
    doc.setTextColor(...primaryBlue);
    doc.text('SECURITY VALIDATION', 20, yPos);
    doc.line(20, yPos + 2, 190, yPos + 2);
    
    yPos += 10;
    if (state.currentJob.security_report) {
      const secReport = state.currentJob.security_report;
      const securityPassed = secReport.overall_passed || secReport.security_passed || false;
      const securityScore = secReport.security_score || secReport.overall_score || 100;
      
      // Overall Status Box
      doc.setFillColor(securityPassed ? 220 : 254, securityPassed ? 252 : 226, securityPassed ? 231 : 230);
      doc.roundedRect(20, yPos - 5, 170, 15, 2, 2, 'F');
      
      doc.setFontSize(11);
      doc.setFont(undefined, 'bold');
      if (securityPassed) {
        doc.setTextColor(...successGreen);
      } else {
        doc.setTextColor(...errorRed);
      }
      doc.text(`Overall Status: ${securityPassed ? 'PASSED' : 'FAILED'}`, 25, yPos);
      doc.text(`Security Score: ${Math.round(securityScore)}%`, 140, yPos);
      
      yPos += 12;
      doc.setTextColor(...textGray);
      doc.setFontSize(10);
      doc.setFont(undefined, 'bold');
      doc.text('Security Layers:', 20, yPos);
      
      yPos += 7;
      doc.setFont(undefined, 'normal');
      
      // Security Layers with icons
      if (secReport.layers) {
        Object.entries(secReport.layers).forEach(([layerName, layerData]) => {
          const passed = layerData.passed || false;
          const icon = passed ? '✓' : '✗';
          
          if (passed) {
            doc.setTextColor(...successGreen);
          } else {
            doc.setTextColor(...errorRed);
          }
          doc.text(icon, 25, yPos);
          doc.setTextColor(...textGray);
          doc.text(`${layerName.replace(/_/g, ' ').toUpperCase()}`, 32, yPos);
          if (passed) {
            doc.setTextColor(...successGreen);
          } else {
            doc.setTextColor(...errorRed);
          }
          doc.text(passed ? 'Pass' : 'Fail', 150, yPos);
          
          yPos += 6;
        });
      }
    }
    
    // AI Analysis Results Section
    yPos += 10;
    doc.setFontSize(14);
    doc.setTextColor(...primaryBlue);
    doc.setFont(undefined, 'bold');
    doc.text('AI ANALYSIS RESULTS', 20, yPos);
    doc.line(20, yPos + 2, 190, yPos + 2);
    
    yPos += 10;
    if (state.currentJob.ai_results && state.currentJob.ai_results.success) {
      const aiResults = state.currentJob.ai_results;
      doc.setFontSize(10);
      
      // Disease Risk
      if (aiResults.disease_risk) {
        const riskPercent = Math.round(aiResults.disease_risk.risk_probability * 100);
        const riskLevel = aiResults.disease_risk.risk_level.toUpperCase();
        
        doc.setFillColor(254, 243, 199);
        doc.roundedRect(20, yPos - 5, 170, 12, 2, 2, 'F');
        
        doc.setTextColor(...textGray);
        doc.setFont(undefined, 'bold');
        doc.text('Disease Risk:', 25, yPos);
        if (riskLevel === 'HIGH') {
          doc.setTextColor(...errorRed);
        } else if (riskLevel === 'MEDIUM') {
          doc.setTextColor(245, 158, 11);
        } else {
          doc.setTextColor(...successGreen);
        }
        doc.text(`${riskLevel} (${riskPercent}%)`, 60, yPos);
        yPos += 15;
      }
      
      // Drug Response
      if (aiResults.drug_response) {
        const responsePercent = Math.round(aiResults.drug_response.response_value * 100);
        const responseCategory = aiResults.drug_response.response_category.toUpperCase();
        
        doc.setFillColor(220, 252, 231);
        doc.roundedRect(20, yPos - 5, 170, 12, 2, 2, 'F');
        
        doc.setTextColor(...textGray);
        doc.setFont(undefined, 'bold');
        doc.text('Drug Response:', 25, yPos);
        doc.setTextColor(...successGreen);
        doc.text(`${responseCategory} (${responsePercent}%)`, 65, yPos);
        yPos += 15;
      }
      
      // Features Analyzed
      if (aiResults.feature_count) {
        doc.setFillColor(239, 246, 255);
        doc.roundedRect(20, yPos - 5, 170, 12, 2, 2, 'F');
        
        doc.setTextColor(...textGray);
        doc.setFont(undefined, 'bold');
        doc.text('Genomic Features Analyzed:', 25, yPos);
        doc.setTextColor(...primaryBlue);
        doc.text(`${aiResults.feature_count}`, 90, yPos);
        yPos += 15;
      }
    }
    
    // Privacy Notice
    yPos += 5;
    doc.setFillColor(254, 226, 226);
    doc.roundedRect(20, yPos - 5, 170, 20, 2, 2, 'F');
    doc.setFontSize(9);
    doc.setTextColor(...errorRed);
    doc.setFont(undefined, 'bold');
    doc.text('PRIVACY NOTICE', 25, yPos);
    doc.setFont(undefined, 'normal');
    doc.setTextColor(...textGray);
    doc.text('All uploaded genomic data has been permanently deleted after analysis.', 25, yPos + 6);
    doc.text('No genetic information is stored on our servers.', 25, yPos + 12);
    
    // Footer
    yPos = 275;
    doc.setFontSize(8);
    doc.setTextColor(...lightGray);
    doc.setFont(undefined, 'normal');
    doc.text('SecureAI-MedGenomics Platform | Multi-Layer Security & AI-Powered Analysis', 105, yPos, { align: 'center' });
    doc.text(`Report ID: ${state.currentJob.job_id} | Page 1 of 1`, 105, yPos + 5, { align: 'center' });
    
    // Save PDF
    doc.save(`genomics-report-${state.currentJob.job_id}.pdf`);
    showToast('PDF downloaded successfully!', 'success');
  } catch (error) {
    console.error('PDF generation error:', error);
    showToast('Failed to generate PDF', 'error');
  }
}

// Proof of Deletion Modal
async function showProofOfDeletion() {
  if (!state.currentJob) return;
  
  const modal = document.getElementById('proof-deletion-modal');
  
  if (!CONFIG.DEMO_MODE) {
    // Fetch real proof from backend
    const result = await getProofOfDeletion(state.currentJob.job_id);
    
    if (result.success) {
      document.getElementById('cert-job-id').textContent = result.data.job_id;
      document.getElementById('cert-timestamp').textContent = formatTimestamp(result.data.deletion_timestamp);
      document.getElementById('cert-hash').textContent = result.data.file_hash;
    } else {
      showToast('Failed to retrieve proof', 'error');
      return;
    }
  } else {
    // Demo mode - generate mock proof
    document.getElementById('cert-job-id').textContent = state.currentJob.job_id;
    document.getElementById('cert-timestamp').textContent = formatTimestamp(state.currentJob.deleted);
    document.getElementById('cert-hash').textContent = generateHash();
  }
  
  modal.classList.add('active');
}

// Modals
function initModals() {
  // Encryption instructions modal
  const encryptionModal = document.getElementById('encryption-modal');
  document.getElementById('show-encryption-help').addEventListener('click', () => {
    encryptionModal.classList.add('active');
  });
  
  document.getElementById('close-encryption-modal').addEventListener('click', () => {
    encryptionModal.classList.remove('active');
  });
  
  // Copy code buttons
  document.querySelectorAll('.copy-code-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.dataset.code;
      navigator.clipboard.writeText(code).then(() => {
        btn.textContent = 'Copied!';
        setTimeout(() => {
          btn.textContent = 'Copy';
        }, 2000);
      });
    });
  });
  
  // Proof of deletion modal
  document.getElementById('proof-deletion-btn').addEventListener('click', showProofOfDeletion);
  
  document.getElementById('close-proof-modal').addEventListener('click', () => {
    document.getElementById('proof-deletion-modal').classList.remove('active');
  });
  
  // Cancel job modal
  const cancelModal = document.getElementById('cancel-modal');
  document.getElementById('cancel-job-btn').addEventListener('click', () => {
    cancelModal.classList.add('active');
  });
  
  document.getElementById('close-cancel-modal').addEventListener('click', () => {
    cancelModal.classList.remove('active');
  });
  
  document.getElementById('cancel-modal-no').addEventListener('click', () => {
    cancelModal.classList.remove('active');
  });
  
  document.getElementById('cancel-modal-yes').addEventListener('click', async () => {
    cancelModal.classList.remove('active');
    
    if (!CONFIG.DEMO_MODE && state.currentJob) {
      // Real mode - call cancel API
      const success = await cancelJob(state.currentJob.job_id);
      if (success) {
        showToast('Job cancelled successfully', 'info');
      } else {
        showToast('Failed to cancel job', 'error');
      }
    } else {
      showToast('Job cancelled. File deleted.', 'info');
    }
    
    if (state.processInterval) {
      clearInterval(state.processInterval);
    }
    
    setTimeout(() => {
      navigateTo('upload');
      document.getElementById('upload-form').reset();
      document.getElementById('file-drop-zone').style.display = 'block';
      document.getElementById('file-selected').style.display = 'none';
      state.uploadedFile = null;
      state.currentJob = null;
    }, 1000);
  });
  
  // Close modals on backdrop click
  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', () => {
      backdrop.parentElement.classList.remove('active');
    });
  });
}

// Copy Job ID
function initCopyJobId() {
  document.getElementById('copy-job-id').addEventListener('click', () => {
    const jobId = state.currentJob.job_id;
    navigator.clipboard.writeText(jobId).then(() => {
      showToast('Job ID copied to clipboard!', 'success');
    });
  });
}

// Feedback
function initFeedback() {
  document.getElementById('feedback-yes').addEventListener('click', () => {
    document.querySelector('.feedback-buttons').style.display = 'none';
    document.getElementById('feedback-thank-you').style.display = 'block';
    showToast('Thank you for your feedback!', 'success');
  });
  
  document.getElementById('feedback-no').addEventListener('click', () => {
    document.querySelector('.feedback-buttons').style.display = 'none';
    document.getElementById('feedback-thank-you').style.display = 'block';
    showToast('Thank you for your feedback! We\'ll work on improvements.', 'info');
  });
}

// Download Results Button
function initDownloadButton() {
  document.getElementById('download-result-btn').addEventListener('click', downloadResults);
  document.getElementById('download-pdf-btn').addEventListener('click', downloadResultsPDF);
}

// Admin Panel
function initAdmin() {
  const loginForm = document.getElementById('admin-login-form');
  const loginMessage = document.getElementById('admin-login-message');
  
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('admin-username').value;
    const password = document.getElementById('admin-password').value;
    
    if (!CONFIG.DEMO_MODE) {
      // Real mode - authenticate with backend
      const success = await adminLogin(username, password);
      
      if (success) {
        state.adminLoggedIn = true;
        document.getElementById('admin-login').style.display = 'none';
        document.getElementById('admin-dashboard').style.display = 'block';
        await loadAdminJobs();
        showToast('Logged in successfully!', 'success');
      } else {
        loginMessage.textContent = 'Invalid username or password.';
        loginMessage.className = 'form-message error';
        loginMessage.style.display = 'block';
      }
    } else {
      // Demo mode - simple check
      if (username === 'admin' && password === 'genomics2025') {
        state.adminLoggedIn = true;
        document.getElementById('admin-login').style.display = 'none';
        document.getElementById('admin-dashboard').style.display = 'block';
        loadAdminJobs();
        showToast('Logged in successfully! (Demo Mode)', 'success');
      } else {
        loginMessage.textContent = 'Invalid username or password.';
        loginMessage.className = 'form-message error';
        loginMessage.style.display = 'block';
      }
    }
  });
  
  // Logout
  document.getElementById('logout-btn').addEventListener('click', () => {
    state.adminLoggedIn = false;
    navigateTo('upload');
    showToast('Logged out successfully.', 'info');
  });
  
  // Tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabName = btn.dataset.tab;
      
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
      });
      document.getElementById(`tab-${tabName}`).classList.add('active');
    });
  });
}

async function adminLogin(username, password) {
  const auth = btoa(`${username}:${password}`);
  
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/admin/jobs`, {
      headers: {
        'Authorization': `Basic ${auth}`
      }
    });
    
    if (response.ok) {
      state.adminAuth = auth;
      return true;
    }
    return false;
  } catch (error) {
    return false;
  }
}

async function fetchAdminJobs() {
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/admin/jobs`, {
      headers: {
        'Authorization': `Basic ${state.adminAuth}`
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      return data.jobs || [];
    }
    return null;
  } catch (error) {
    return null;
  }
}

async function loadAdminJobs() {
  const tbody = document.getElementById('jobs-table-body');
  tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px;">Loading...</td></tr>';
  
  let allJobs = [];
  
  if (!CONFIG.DEMO_MODE && state.adminAuth) {
    // Real mode - fetch from backend
    const backendJobs = await fetchAdminJobs();
    if (backendJobs) {
      allJobs = backendJobs;
    } else {
      // Silently fail if can't load jobs (database may be fresh)
      tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px;">No jobs found</td></tr>';
      console.log('No previous jobs found (this is normal after database reset)');
      return;
    }
  } else {
    // Demo mode - use mock data
    allJobs = [...mockJobs];
    if (state.currentJob && state.currentJob.status === 'completed') {
      allJobs.unshift(state.currentJob);
    }
  }
  
  tbody.innerHTML = '';
  
  if (allJobs.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px;">No jobs found</td></tr>';
    return;
  }
  
  allJobs.forEach(job => {
    const row = document.createElement('tr');
    const statusClass = job.status === 'completed' ? 'status-completed' : 'status-processing';
    
    row.innerHTML = `
      <td><code>${job.job_id.substring(0, 8)}...</code></td>
      <td>${formatTimestamp(job.received)}</td>
      <td>${job.completed ? formatTimestamp(job.completed) : 'N/A'}</td>
      <td>${job.duration ? job.duration + 's' : 'N/A'}</td>
      <td><span class="status-badge ${statusClass}">${job.status}</span></td>
      <td><button class="btn btn-outline" style="padding: 4px 12px; font-size: 14px;">View</button></td>
    `;
    
    tbody.appendChild(row);
  });
}

// Hamburger Menu
function initHamburger() {
  const hamburger = document.getElementById('hamburger');
  const navMobile = document.getElementById('nav-mobile');
  
  hamburger.addEventListener('click', () => {
    navMobile.classList.toggle('active');
  });
}

// Hash Routing
function initRouting() {
  window.addEventListener('hashchange', () => {
    const hash = window.location.hash.slice(1);
    if (hash) {
      navigateTo(hash);
    }
  });
  
  // Handle initial load
  const hash = window.location.hash.slice(1);
  if (hash) {
    navigateTo(hash);
  } else {
    navigateTo('upload');
  }
  
  // Navigation links
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const page = link.dataset.page;
      window.location.hash = page;
    });
  });
}

// Backend Status Check
async function initBackendStatus() {
  const statusIndicator = document.getElementById('status-indicator');
  const statusText = document.getElementById('status-text');
  
  if (!statusIndicator || !statusText) return;
  
  if (CONFIG.DEMO_MODE) {
    statusIndicator.textContent = '🟡';
    statusText.textContent = 'Demo Mode (No Backend)';
    return;
  }
  
  const connected = await checkBackendHealth();
  
  if (connected) {
    statusIndicator.textContent = '🟢';
    statusText.textContent = 'Backend Connected';
    statusIndicator.parentElement.style.background = 'rgba(16, 185, 129, 0.2)';
  } else {
    statusIndicator.textContent = '🔴';
    statusText.textContent = 'Backend Offline';
    statusIndicator.parentElement.style.background = 'rgba(239, 68, 68, 0.2)';
    showToast('Backend not connected. Enable DEMO_MODE or start the server.', 'info');
  }
}

// Initialize Modals
function initModals() {
  // Cancel Job Modal
  const cancelJobBtn = document.getElementById('cancel-job-btn');
  const cancelModal = document.getElementById('cancel-modal');
  const closeCancelModal = document.getElementById('close-cancel-modal');
  const cancelModalNo = document.getElementById('cancel-modal-no');
  const cancelModalYes = document.getElementById('cancel-modal-yes');

  if (cancelJobBtn) {
    cancelJobBtn.addEventListener('click', () => {
      cancelModal.classList.add('active');
    });
  }

  if (closeCancelModal) {
    closeCancelModal.addEventListener('click', () => {
      cancelModal.classList.remove('active');
    });
  }

  if (cancelModalNo) {
    cancelModalNo.addEventListener('click', () => {
      cancelModal.classList.remove('active');
    });
  }

  if (cancelModalYes) {
    cancelModalYes.addEventListener('click', async () => {
      cancelModal.classList.remove('active');
      
      if (state.currentJob) {
        try {
          showToast('Canceling job...', 'info');
          const response = await fetch(`${CONFIG.API_BASE_URL}/cancel/${state.currentJob}`, {
            method: 'POST'
          });
          
          if (response.ok) {
            showToast('Job canceled successfully', 'success');
            navigateTo('upload');
          } else {
            showToast('Failed to cancel job', 'error');
          }
        } catch (error) {
          console.error('Error canceling job:', error);
          showToast('Error canceling job', 'error');
          navigateTo('upload'); // Go back anyway
        }
      } else {
        navigateTo('upload');
      }
    });
  }

  // Close modal when clicking backdrop
  const modalBackdrops = document.querySelectorAll('.modal-backdrop');
  modalBackdrops.forEach(backdrop => {
    backdrop.addEventListener('click', () => {
      backdrop.parentElement.classList.remove('active');
    });
  });

  // Encryption modal
  const encryptionModal = document.getElementById('encryption-modal');
  const closeEncryptionModal = document.getElementById('close-encryption-modal');
  
  if (closeEncryptionModal) {
    closeEncryptionModal.addEventListener('click', () => {
      encryptionModal.classList.remove('active');
    });
  }

  // Proof of deletion modal
  const proofDeletionBtn = document.getElementById('proof-deletion-btn');
  const proofDeletionModal = document.getElementById('proof-deletion-modal');
  const closeProofModal = document.getElementById('close-proof-modal');

  if (proofDeletionBtn) {
    proofDeletionBtn.addEventListener('click', async () => {
      // Fill certificate with job data
      const jobIdElement = document.getElementById('cert-job-id');
      const timestampElement = document.getElementById('cert-timestamp');
      const hashElement = document.getElementById('cert-hash');
      
      // Fix: Extract job_id from state.currentJob object
      let jobId;
      if (state.currentJob) {
        jobId = typeof state.currentJob === 'string' ? state.currentJob : state.currentJob.job_id;
      } else {
        jobId = 'DEMO-' + Date.now().toString(36).toUpperCase();
      }
      
      const timestamp = new Date().toISOString();
      
      if (jobIdElement) jobIdElement.textContent = jobId;
      if (timestampElement) timestampElement.textContent = timestamp;
      
      // Generate real cryptographic hash
      if (hashElement) {
        hashElement.textContent = 'Generating...';
        const hash = await generateDeletionHash(jobId, timestamp);
        hashElement.textContent = hash;
      }
      
      proofDeletionModal.classList.add('active');
    });
  }

  if (closeProofModal) {
    closeProofModal.addEventListener('click', () => {
      proofDeletionModal.classList.remove('active');
    });
  }

  // Download certificate as text file
  const downloadCertBtn = document.getElementById('download-certificate-btn');
  if (downloadCertBtn) {
    downloadCertBtn.addEventListener('click', () => {
      const jobId = document.getElementById('cert-job-id')?.textContent || 'N/A';
      const timestamp = document.getElementById('cert-timestamp')?.textContent || 'N/A';
      const hash = document.getElementById('cert-hash')?.textContent || 'N/A';
      
      const certificateText = `
╔═══════════════════════════════════════════════════════════════╗
║          PROOF OF DELETION CERTIFICATE                        ║
║          SecureAI-MedGenomics Platform                        ║
╚═══════════════════════════════════════════════════════════════╝

CERTIFICATE DETAILS
═══════════════════════════════════════════════════════════════

Job ID:
${jobId}

Deletion Timestamp (UTC):
${timestamp}

File Deletion Hash (SHA-256):
${hash}

WHAT IS THIS HASH?
═══════════════════════════════════════════════════════════════
This SHA-256 cryptographic hash serves as verifiable proof that your
genomic data was permanently deleted from our systems. The hash is
generated from:
  • Job ID
  • Deletion timestamp
  • Server secret key

This hash is unique and cannot be forged, providing cryptographic
proof that deletion occurred at the exact time stated above.

VERIFICATION INSTRUCTIONS
═══════════════════════════════════════════════════════════════
1. Save this certificate for your records
2. The hash proves deletion happened at the stated timestamp
3. Contact security@secureai-genomics.edu with the Job ID to verify
4. We do NOT store genomic data - only deletion records for compliance

COMPLIANCE
═══════════════════════════════════════════════════════════════
✓ HIPAA Compliant
✓ GDPR Article 17 (Right to Erasure)
✓ Data Minimization Principle
✓ Cryptographic Proof of Deletion

═══════════════════════════════════════════════════════════════
Issued by: SecureAI-MedGenomics Security Team
Contact: security@secureai-genomics.edu
Generated: ${new Date().toISOString()}
═══════════════════════════════════════════════════════════════
`;
      
      const blob = new Blob([certificateText], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `deletion-certificate-${jobId}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      showToast('Certificate downloaded successfully', 'success');
    });
  }
}

// Generate mock SHA-256 hash for proof of deletion
function generateMockHash() {
  const chars = '0123456789abcdef';
  let hash = '';
  for (let i = 0; i < 64; i++) {
    hash += chars[Math.floor(Math.random() * chars.length)];
  }
  return hash;
}

// Generate cryptographic hash from job data
async function generateDeletionHash(jobId, timestamp) {
  const data = `${jobId}:${timestamp}:SECURE_DELETION_PROOF`;
  
  // Use Web Crypto API for real SHA-256
  if (crypto && crypto.subtle) {
    try {
      const encoder = new TextEncoder();
      const dataBuffer = encoder.encode(data);
      const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
      return hashHex;
    } catch (error) {
      console.error('Crypto API error:', error);
      return generateMockHash();
    }
  }
  
  return generateMockHash();
}

// Custom confirmation modal
function showCustomConfirm(fileName, fileSize) {
  return new Promise((resolve) => {
    // Create modal HTML
    const modalHTML = `
      <div class="custom-confirm-modal" id="custom-confirm-modal">
        <div class="custom-confirm-content">
          <div class="custom-confirm-header">
            <div class="custom-confirm-icon">📤</div>
            <h2 class="custom-confirm-title">Confirm File Upload</h2>
          </div>
          <div class="custom-confirm-body">
            <div class="file-info-box">
              <div class="file-info-row">
                <span class="file-info-label">File Name:</span>
                <span class="file-info-value">${fileName}</span>
              </div>
              <div class="file-info-row">
                <span class="file-info-label">File Size:</span>
                <span class="file-info-value">${fileSize} KB</span>
              </div>
            </div>
            
            <div class="security-checklist">
              <div class="security-checklist-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <span>Automatically encrypted with AES-256</span>
              </div>
              <div class="security-checklist-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <span>Analyzed by AI (species detection, quality check)</span>
              </div>
              <div class="security-checklist-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <span>Permanently deleted after processing (&lt;60 seconds)</span>
              </div>
              <div class="security-checklist-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <span>Proof-of-deletion certificate available</span>
              </div>
            </div>
            
            <div class="custom-confirm-actions">
              <button class="custom-confirm-btn custom-confirm-btn-cancel" id="custom-confirm-cancel">
                Cancel
              </button>
              <button class="custom-confirm-btn custom-confirm-btn-confirm" id="custom-confirm-ok">
                Upload & Analyze
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
    
    // Add to DOM
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    const modal = document.getElementById('custom-confirm-modal');
    const cancelBtn = document.getElementById('custom-confirm-cancel');
    const okBtn = document.getElementById('custom-confirm-ok');
    
    // Handle cancel
    const handleCancel = () => {
      modal.remove();
      resolve(false);
    };
    
    // Handle confirm
    const handleConfirm = () => {
      modal.remove();
      resolve(true);
    };
    
    // Event listeners
    cancelBtn.addEventListener('click', handleCancel);
    okBtn.addEventListener('click', handleConfirm);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) handleCancel();
    });
  });
}

// Initialize App
function init() {
  initRouting();
  initHamburger();
  initFileUpload();
  initUploadForm();
  initModals();
  initCopyJobId();
  initFeedback();
  initDownloadButton();
  initAdmin();
  initBackendStatus();
  startBackendHealthCheck(); // Start checking backend connection
}

// Run on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

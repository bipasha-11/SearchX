import os

css = """
/* ============================================================
   AUTH PAGE (Added dynamically)
   ============================================================ */

.auth-page {
  display: flex;
  min-height: calc(100vh - 64px);
  position: relative;
  overflow: hidden;
  background: var(--cream-light);
  justify-content: center;
  align-items: center;
  padding: 40px;
}

.auth-bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
  opacity: 0.6;
}

.auth-bg-orb-1 {
  top: -100px;
  left: -100px;
  width: 400px;
  height: 400px;
  background: var(--coral-light);
}

.auth-bg-orb-2 {
  bottom: -150px;
  right: -50px;
  width: 500px;
  height: 500px;
  background: var(--sage-light);
}

.auth-bg-orb-3 {
  top: 40%;
  left: 60%;
  width: 300px;
  height: 300px;
  background: var(--cream-dark);
  filter: blur(100px);
}

.auth-container {
  position: relative;
  z-index: 1;
  display: flex;
  width: 100%;
  max-width: 1000px;
  min-height: 600px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.auth-brand-panel {
  flex: 1;
  background: linear-gradient(135deg, var(--navy), var(--navy-dark));
  color: var(--white);
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.auth-brand-logo {
  margin-bottom: 24px;
}

.auth-brand-logo-icon {
  width: 48px;
  height: 48px;
  background: var(--coral);
  color: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 20px;
}

.auth-brand-title {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: 2px;
  margin-bottom: 8px;
}

.auth-brand-title span {
  color: var(--coral);
}

.auth-brand-subtitle {
  font-size: 18px;
  color: var(--sage-light);
  margin-bottom: 24px;
}

.auth-brand-divider {
  width: 40px;
  height: 4px;
  background: var(--coral);
  border-radius: 2px;
  margin-bottom: 24px;
}

.auth-brand-description {
  font-size: 15px;
  line-height: 1.6;
  color: rgba(255,255,255,0.8);
  margin-bottom: 40px;
}

.auth-brand-features {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.auth-brand-feature {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 500;
}

.auth-brand-feature-icon {
  font-size: 20px;
}

.auth-form-panel {
  flex: 1;
  padding: 60px 40px;
  background: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.auth-tabs {
  display: flex;
  position: relative;
  margin-bottom: 40px;
  border-bottom: 2px solid var(--cream-light);
}

.auth-tab {
  flex: 1;
  padding: 12px 0;
  background: none;
  border: none;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-muted);
  cursor: pointer;
  transition: 0.3s;
}

.auth-tab.active {
  color: var(--navy);
}

.auth-tab-indicator {
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 50%;
  height: 2px;
  background: var(--coral);
  transition: transform 0.3s ease;
}

.auth-error {
  background: rgba(224, 122, 95, 0.1);
  color: var(--coral-dark);
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
}

.auth-form-group {
  margin-bottom: 20px;
}

.auth-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--navy);
  margin-bottom: 8px;
}

.auth-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.auth-input-icon {
  position: absolute;
  left: 16px;
  color: var(--text-muted);
  font-size: 16px;
}

.auth-input {
  width: 100%;
  padding: 14px 16px 14px 44px;
  border: 1px solid var(--border);
  border-radius: 12px;
  font-size: 15px;
  transition: 0.3s;
  background: #f9f9fa;
}

.auth-input:focus {
  background: white;
  border-color: var(--coral);
  box-shadow: 0 0 0 3px rgba(224, 122, 95, 0.1);
}

.auth-toggle-password {
  position: absolute;
  right: 16px;
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: var(--text-muted);
}

.auth-show-password {
  margin-bottom: 24px;
}

.auth-checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text-secondary);
}

.auth-form-row {
  display: flex;
  gap: 16px;
}
.auth-form-row > .auth-form-group {
  flex: 1;
}

.auth-submit {
  width: 100%;
  padding: 16px;
  background: var(--coral);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
  margin-bottom: 24px;
}

.auth-submit:hover {
  background: var(--coral-dark);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(224, 122, 95, 0.2);
}

.auth-submit:disabled {
  background: var(--text-muted);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.auth-switch-text {
  text-align: center;
  font-size: 14px;
  color: var(--text-secondary);
}

.auth-switch-link {
  background: none;
  border: none;
  color: var(--coral);
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-left: 4px;
}

.auth-switch-link:hover {
  text-decoration: underline;
}

.auth-submit-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.auth-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@media (max-width: 768px) {
  .auth-container {
    flex-direction: column;
    min-height: auto;
  }
  .auth-brand-panel {
    padding: 40px 30px;
  }
  .auth-form-panel {
    padding: 40px 30px;
  }
  .auth-form-row {
    flex-direction: column;
    gap: 0;
  }
}
"""

with open(r"d:\SEARCHX\frontend\src\index.css", "a") as f:
    f.write(css)

print("CSS appended successfully!")

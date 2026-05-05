import React, { useState } from 'react';
import { Redirect } from 'react-router-dom';
import { useAuth } from '../AuthContext';

function AuthPage() {
    var auth = useAuth();

    // If already logged in, redirect to analytics dashboard
    if (auth.isAuthenticated) {
        return <Redirect to="/analytics" />;
    }

    var tabState = useState('login');
    var activeTab = tabState[0];
    var setActiveTab = tabState[1];

    // Login form
    var loginUsernameState = useState('');
    var loginUsername = loginUsernameState[0];
    var setLoginUsername = loginUsernameState[1];

    var loginPasswordState = useState('');
    var loginPassword = loginPasswordState[0];
    var setLoginPassword = loginPasswordState[1];

    // Register form
    var regUsernameState = useState('');
    var regUsername = regUsernameState[0];
    var setRegUsername = regUsernameState[1];

    var regEmailState = useState('');
    var regEmail = regEmailState[0];
    var setRegEmail = regEmailState[1];

    var regPasswordState = useState('');
    var regPassword = regPasswordState[0];
    var setRegPassword = regPasswordState[1];

    var regConfirmState = useState('');
    var regConfirm = regConfirmState[0];
    var setRegConfirm = regConfirmState[1];

    var regFullNameState = useState('');
    var regFullName = regFullNameState[0];
    var setRegFullName = regFullNameState[1];

    // Shared state
    var loadingState = useState(false);
    var loading = loadingState[0];
    var setLoading = loadingState[1];

    var errorState = useState('');
    var error = errorState[0];
    var setError = errorState[1];

    var showPasswordState = useState(false);
    var showPassword = showPasswordState[0];
    var setShowPassword = showPasswordState[1];

    auth = useAuth();

    var handleLogin = function (e) {
        e.preventDefault();
        setError('');

        if (!loginUsername.trim()) { setError('Username is required'); return; }
        if (!loginPassword) { setError('Password is required'); return; }

        setLoading(true);

        fetch(auth.apiBase + '/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: loginUsername.trim(),
                password: loginPassword
            })
        })
            .then(function (res) {
                return res.json().then(function (data) {
                    return { ok: res.ok, data: data };
                });
            })
            .then(function (result) {
                if (!result.ok) {
                    setError(result.data.error || 'Login failed');
                } else {
                    auth.login(result.data.token, result.data.user);
                }
                setLoading(false);
            })
            .catch(function () {
                setError('Network error. Is the backend running?');
                setLoading(false);
            });
    };

    var isOtpSentState = useState(false);
    var isOtpSent = isOtpSentState[0];
    var setIsOtpSent = isOtpSentState[1];

    var otpState = useState('');
    var otp = otpState[0];
    var setOtp = otpState[1];

    var handleRegister = function (e) {
        e.preventDefault();
        setError('');

        if (!isOtpSent) {
            if (!regFullName.trim()) { setError('Full name is required'); return; }
            if (!regUsername.trim()) { setError('Username is required'); return; }
            if (regUsername.trim().length < 3) { setError('Username must be at least 3 characters'); return; }
            if (!regEmail.trim() || regEmail.indexOf('@') === -1) { setError('Valid email is required'); return; }
            if (!regPassword || regPassword.length < 6) { setError('Password must be at least 6 characters'); return; }
            if (regPassword !== regConfirm) { setError('Passwords do not match'); return; }

            setLoading(true);

            fetch(auth.apiBase + '/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: regUsername.trim(),
                    email: regEmail.trim(),
                    password: regPassword,
                    full_name: regFullName.trim()
                })
            })
                .then(function (res) {
                    return res.json().then(function (data) {
                        return { ok: res.ok, data: data };
                    });
                })
                .then(function (result) {
                    if (!result.ok) {
                        setError(result.data.error || 'Registration failed');
                    } else {
                        setIsOtpSent(true);
                    }
                    setLoading(false);
                })
                .catch(function () {
                    setError('Network error. Is the backend running?');
                    setLoading(false);
                });
        } else {
            if (!otp.trim()) { setError('OTP is required'); return; }
            setLoading(true);

            fetch(auth.apiBase + '/api/auth/register/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: regEmail.trim(),
                    otp: otp.trim()
                })
            })
                .then(function (res) {
                    return res.json().then(function (data) {
                        return { ok: res.ok, data: data };
                    });
                })
                .then(function (result) {
                    if (!result.ok) {
                        setError(result.data.error || 'Verification failed');
                    } else {
                        auth.login(result.data.token, result.data.user);
                    }
                    setLoading(false);
                })
                .catch(function () {
                    setError('Network error. Is the backend running?');
                    setLoading(false);
                });
        }
    };

    var switchTab = function (tab) {
        setActiveTab(tab);
        setIsOtpSent(false);
        setError('');
    };

    return (
        <div className="auth-page" id="auth-page">
            {/* Decorative background elements */}
            <div className="auth-bg-orb auth-bg-orb-1"></div>
            <div className="auth-bg-orb auth-bg-orb-2"></div>
            <div className="auth-bg-orb auth-bg-orb-3"></div>

            <div className="auth-container">
                {/* Left panel - branding */}
                <div className="auth-brand-panel">
                    <div className="auth-brand-content">
                        <div className="auth-brand-logo">
                            <div className="auth-brand-logo-icon">SX</div>
                        </div>
                        <h1 className="auth-brand-title">
                            SEARCH<span>X</span>
                        </h1>
                        <p className="auth-brand-subtitle">
                            Legal Document Intelligence
                        </p>
                        <div className="auth-brand-divider"></div>
                        <p className="auth-brand-description">
                            Your secure portal to search, index, and analyze legal documents.
                            Each user's case files are private and protected.
                        </p>

                        <div className="auth-brand-features">
                            <div className="auth-brand-feature">
                                <span className="auth-brand-feature-icon">🔒</span>
                                <span>Secure & Private</span>
                            </div>
                            <div className="auth-brand-feature">
                                <span className="auth-brand-feature-icon">📄</span>
                                <span>Your Documents, Only Yours</span>
                            </div>
                            <div className="auth-brand-feature">
                                <span className="auth-brand-feature-icon">⚡</span>
                                <span>Oracle 11g Powered</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right panel - form */}
                <div className="auth-form-panel">
                    <div className="auth-form-content">
                        <div className="auth-tabs">
                            <button
                                className={'auth-tab' + (activeTab === 'login' ? ' active' : '')}
                                onClick={function () { switchTab('login'); }}
                                id="tab-login"
                                type="button"
                            >
                                Sign In
                            </button>
                            <button
                                className={'auth-tab' + (activeTab === 'register' ? ' active' : '')}
                                onClick={function () { switchTab('register'); }}
                                id="tab-register"
                                type="button"
                            >
                                Create Account
                            </button>
                            <div
                                className="auth-tab-indicator"
                                style={{ transform: activeTab === 'register' ? 'translateX(100%)' : 'translateX(0)' }}
                            ></div>
                        </div>

                        {error && (
                            <div className="auth-error" id="auth-error">
                                <span className="auth-error-icon">⚠</span>
                                {error}
                            </div>
                        )}

                        {activeTab === 'login' && (
                            <form onSubmit={handleLogin} className="auth-form" id="login-form">
                                <div className="auth-form-group">
                                    <label className="auth-label" htmlFor="login-username">
                                        Username
                                    </label>
                                    <div className="auth-input-wrapper">
                                        <span className="auth-input-icon">👤</span>
                                        <input
                                            type="text"
                                            id="login-username"
                                            className="auth-input"
                                            placeholder="Enter your username"
                                            value={loginUsername}
                                            onChange={function (e) { setLoginUsername(e.target.value); }}
                                            autoFocus
                                            autoComplete="username"
                                        />
                                    </div>
                                </div>

                                <div className="auth-form-group">
                                    <label className="auth-label" htmlFor="login-password">
                                        Password
                                    </label>
                                    <div className="auth-input-wrapper">
                                        <span className="auth-input-icon">🔑</span>
                                        <input
                                            type={showPassword ? 'text' : 'password'}
                                            id="login-password"
                                            className="auth-input"
                                            placeholder="Enter your password"
                                            value={loginPassword}
                                            onChange={function (e) { setLoginPassword(e.target.value); }}
                                            autoComplete="current-password"
                                        />
                                        <button
                                            type="button"
                                            className="auth-toggle-password"
                                            onClick={function () { setShowPassword(!showPassword); }}
                                            tabIndex={-1}
                                        >
                                            {showPassword ? '🙈' : '👁'}
                                        </button>
                                    </div>
                                </div>

                                <button
                                    type="submit"
                                    className="auth-submit"
                                    id="login-submit"
                                    disabled={loading}
                                >
                                    {loading ? (
                                        <span className="auth-submit-loading">
                                            <span className="auth-spinner"></span>
                                            Signing in...
                                        </span>
                                    ) : (
                                        <span>Sign In →</span>
                                    )}
                                </button>

                                <p className="auth-switch-text">
                                    Don't have an account?{' '}
                                    <button
                                        type="button"
                                        className="auth-switch-link"
                                        onClick={function () { switchTab('register'); }}
                                    >
                                        Create one
                                    </button>
                                </p>
                            </form>
                        )}

                        {activeTab === 'register' && (
                            <form onSubmit={handleRegister} className="auth-form" id="register-form">
                                {!isOtpSent && (
                                    <>
                                        <div className="auth-form-group">
                                            <label className="auth-label" htmlFor="reg-fullname">
                                                Full Name
                                            </label>
                                            <div className="auth-input-wrapper">
                                                <span className="auth-input-icon">✏️</span>
                                                <input
                                                    type="text"
                                                    id="reg-fullname"
                                                    className="auth-input"
                                                    placeholder="e.g., Advocate Sharma"
                                                    value={regFullName}
                                                    onChange={function (e) { setRegFullName(e.target.value); }}
                                                    autoFocus
                                                />
                                            </div>
                                        </div>

                                        <div className="auth-form-row">
                                            <div className="auth-form-group">
                                                <label className="auth-label" htmlFor="reg-username">
                                                    Username
                                                </label>
                                                <div className="auth-input-wrapper">
                                                    <span className="auth-input-icon">👤</span>
                                                    <input
                                                        type="text"
                                                        id="reg-username"
                                                        className="auth-input"
                                                        placeholder="Choose a username"
                                                        value={regUsername}
                                                        onChange={function (e) { setRegUsername(e.target.value); }}
                                                        autoComplete="username"
                                                    />
                                                </div>
                                            </div>

                                            <div className="auth-form-group">
                                                <label className="auth-label" htmlFor="reg-email">
                                                    Email
                                                </label>
                                                <div className="auth-input-wrapper">
                                                    <span className="auth-input-icon">📧</span>
                                                    <input
                                                        type="email"
                                                        id="reg-email"
                                                        className="auth-input"
                                                        placeholder="you@example.com"
                                                        value={regEmail}
                                                        onChange={function (e) { setRegEmail(e.target.value); }}
                                                        autoComplete="email"
                                                    />
                                                </div>
                                            </div>
                                        </div>

                                        <div className="auth-form-row">
                                            <div className="auth-form-group">
                                                <label className="auth-label" htmlFor="reg-password">
                                                    Password
                                                </label>
                                                <div className="auth-input-wrapper">
                                                    <span className="auth-input-icon">🔑</span>
                                                    <input
                                                        type={showPassword ? 'text' : 'password'}
                                                        id="reg-password"
                                                        className="auth-input"
                                                        placeholder="Min 6 characters"
                                                        value={regPassword}
                                                        onChange={function (e) { setRegPassword(e.target.value); }}
                                                        autoComplete="new-password"
                                                    />
                                                </div>
                                            </div>

                                            <div className="auth-form-group">
                                                <label className="auth-label" htmlFor="reg-confirm">
                                                    Confirm Password
                                                </label>
                                                <div className="auth-input-wrapper">
                                                    <span className="auth-input-icon">🔑</span>
                                                    <input
                                                        type={showPassword ? 'text' : 'password'}
                                                        id="reg-confirm"
                                                        className="auth-input"
                                                        placeholder="Re-enter password"
                                                        value={regConfirm}
                                                        onChange={function (e) { setRegConfirm(e.target.value); }}
                                                        autoComplete="new-password"
                                                    />
                                                </div>
                                            </div>
                                        </div>

                                        <div className="auth-show-password">
                                            <label className="auth-checkbox-label">
                                                <input
                                                    type="checkbox"
                                                    checked={showPassword}
                                                    onChange={function () { setShowPassword(!showPassword); }}
                                                    className="auth-checkbox"
                                                />
                                                <span className="auth-checkbox-text">Show passwords</span>
                                            </label>
                                        </div>
                                    </>
                                )}

                                {isOtpSent && (
                                    <div className="auth-form-group">
                                        <label className="auth-label" htmlFor="reg-otp">
                                            Verification OTP
                                        </label>
                                        <p style={{fontSize: '12px', color: '#666', marginBottom: '10px'}}>
                                            We've sent a 6-digit code to your email.
                                        </p>
                                        <div className="auth-input-wrapper">
                                            <span className="auth-input-icon">💬</span>
                                            <input
                                                type="text"
                                                id="reg-otp"
                                                className="auth-input"
                                                placeholder="Enter 6-digit code"
                                                value={otp}
                                                maxLength={6}
                                                onChange={function (e) { setOtp(e.target.value); }}
                                                autoFocus
                                            />
                                        </div>
                                    </div>
                                )}

                                <button
                                    type="submit"
                                    className="auth-submit"
                                    id="register-submit"
                                    disabled={loading}
                                >
                                    {loading ? (
                                        <span className="auth-submit-loading">
                                            <span className="auth-spinner"></span>
                                            {isOtpSent ? 'Verifying...' : 'Creating account...'}
                                        </span>
                                    ) : (
                                        <span>{isOtpSent ? 'Verify & Create Account →' : 'Send OTP →'}</span>
                                    )}
                                </button>

                                <p className="auth-switch-text">
                                    Already have an account?{' '}
                                    <button
                                        type="button"
                                        className="auth-switch-link"
                                        onClick={function () { switchTab('login'); }}
                                    >
                                        Sign in
                                    </button>
                                </p>
                            </form>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AuthPage;

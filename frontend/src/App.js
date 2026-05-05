import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link, useLocation, Redirect } from 'react-router-dom';
import { AuthProvider, useAuth } from './AuthContext';
import AuthPage from './pages/AuthPage';
import LandingPage from './pages/LandingPage';
import UploadPage from './pages/UploadPage';
import SearchPage from './pages/SearchPage';
import AnalyticsPage from './pages/AnalyticsPage';
import MyDocumentsPage from './pages/MyDocumentsPage';

function Navbar() {
    var location = useLocation();
    var path = location.pathname;
    var auth = useAuth();

    return (
        <nav className="navbar" id="main-navbar">
            <Link to="/" className="navbar-brand">
                <div className="navbar-logo">SX</div>
                <div className="navbar-title">SEARCH<span>X</span></div>
            </Link>
            <div className="navbar-links">
                <Link to="/" className={'navbar-link' + (path === '/' ? ' active' : '')} id="nav-home">
                    Home
                </Link>
                {auth.user && (
                    <>
                        <Link to="/upload" className={'navbar-link' + (path === '/upload' ? ' active' : '')} id="nav-upload">
                            Upload
                        </Link>
                        <Link to="/search" className={'navbar-link' + (path === '/search' ? ' active' : '')} id="nav-search">
                            Search
                        </Link>
                        <Link to="/documents" className={'navbar-link' + (path === '/documents' ? ' active' : '')} id="nav-docs">
                            Dashboard
                        </Link>
                        <Link to="/analytics" className={'navbar-link' + (path === '/analytics' ? ' active' : '')} id="nav-analytics">
                            Analytics
                        </Link>
                    </>
                )}

                {auth.user ? (
                    <div className="navbar-user">
                        <div className="navbar-user-avatar">
                            {auth.user.full_name ? auth.user.full_name.charAt(0).toUpperCase() : 'U'}
                        </div>
                        <span className="navbar-user-name">
                            {auth.user.full_name}
                        </span>
                        <button onClick={auth.logout} style={{ marginLeft: '15px', padding: '5px 10px', background: 'transparent', border: '1px solid #fff', color: '#fff', borderRadius: '4px', cursor: 'pointer' }}>
                            Logout
                        </button>
                    </div>
                ) : (
                    <Link to="/auth" className="navbar-link" style={{ background: '#e67e22', color: '#fff', padding: '5px 15px', borderRadius: '20px', marginLeft: '10px' }}>
                        Login / Register
                    </Link>
                )}
            </div>
        </nav>
    );
}

function Footer() {
    return (
        <footer className="footer">
            <span>SEARCHX</span> — Search Engine Indexing & Query Analytics System · Oracle 11g · DBMS Project
        </footer>
    );
}

function PrivateRoute({ component: Component, ...rest }) {
    const auth = useAuth();
    return (
        <Route
            {...rest}
            render={props =>
                auth.user ? (
                    <Component {...props} />
                ) : (
                    <Redirect to="/auth" />
                )
            }
        />
    );
}

function AppContent() {
    const auth = useAuth();
    
    if (auth.loading) {
        return <div style={{display: 'flex', height: '100vh', justifyContent: 'center', alignItems: 'center', color: '#fff'}}>Loading...</div>;
    }
    
    return (
        <Router>
            <Navbar />
            <Switch>
                <Route exact path="/" component={LandingPage} />
                <Route path="/auth" component={AuthPage} />
                <PrivateRoute path="/upload" component={UploadPage} />
                <PrivateRoute path="/search" component={SearchPage} />
                <PrivateRoute path="/documents" component={MyDocumentsPage} />
                <PrivateRoute path="/analytics" component={AnalyticsPage} />
                <Redirect to="/" />
            </Switch>
            <Footer />
        </Router>
    );
}

function App() {
    return (
        <AuthProvider>
            <AppContent />
        </AuthProvider>
    );
}

export default App;

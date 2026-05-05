import React, { createContext, useContext, useState, useEffect } from 'react';

var AuthContext = createContext(null);

// Production API Base URL
var API_BASE = 'https://searchx-backend.onrender.com';

function AuthProvider(props) {
    var userState = useState(null);
    var user = userState[0];
    var setUser = userState[1];

    var tokenState = useState(localStorage.getItem('searchx_token'));
    var token = tokenState[0];
    var setToken = tokenState[1];

    var loadingState = useState(true);
    var loading = loadingState[0];
    var setLoading = loadingState[1];

    // Verification on load
    useEffect(function () {
        if (!token) {
            setLoading(false);
            return;
        }
        
        fetch(API_BASE + '/api/auth/me', {
            headers: { 'Authorization': 'Bearer ' + token }
        })
        .then(function(res) {
            if (res.ok) return res.json();
            throw new Error('Token invalid');
        })
        .then(function(data) {
            setUser(data.user);
            setLoading(false);
        })
        .catch(function(err) {
            localStorage.removeItem('searchx_token');
            setToken(null);
            setUser(null);
            setLoading(false);
        });
    }, [token]);

    var login = function (tokenValue, userData) {
        localStorage.setItem('searchx_token', tokenValue);
        setToken(tokenValue);
        setUser(userData);
    };

    var logout = function () {
        localStorage.removeItem('searchx_token');
        setToken(null);
        setUser(null);
    };

    var authFetch = function (url, options) {
        if (!options) options = {};
        if (!options.headers) options.headers = {};

        if (token) {
            options.headers['Authorization'] = 'Bearer ' + token;
        }

        return fetch(API_BASE + url, options).then(function (res) {
            if (res.status === 401) {
                // Token expired — auto-logout
                logout();
                throw new Error('Session expired. Please log in again.');
            }
            return res;
        });
    };

    var value = {
        user: user,
        token: token,
        loading: loading,
        login: login,
        logout: logout,
        authFetch: authFetch,
        apiBase: API_BASE,
        isAuthenticated: !!user
    };

    return React.createElement(AuthContext.Provider, { value: value }, props.children);
}

function useAuth() {
    var context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}

export { AuthProvider, useAuth };
export default AuthContext;

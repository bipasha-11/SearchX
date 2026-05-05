import React, { useState } from 'react';
import { useAuth } from '../AuthContext';

function SearchPage() {
    var auth = useAuth();

    var queryState = useState('');
    var query = queryState[0];
    var setQuery = queryState[1];

    var resultsState = useState(null);
    var results = resultsState[0];
    var setResults = resultsState[1];

    var loadingState = useState(false);
    var loading = loadingState[0];
    var setLoading = loadingState[1];

    var errorState = useState('');
    var error = errorState[0];
    var setError = errorState[1];

    var searchedState = useState(false);
    var searched = searchedState[0];
    var setSearched = searchedState[1];

    var handleSearch = function (e) {
        e.preventDefault();
        var keyword = query.trim();
        if (!keyword) { setError('Enter a search term.'); return; }

        if (keyword.length > 100) { setError('Keyword too long (max 100 characters).'); return; }
        if (!/^[a-zA-Z0-9\s\-_]+$/.test(keyword)) {
            setError('Only letters, numbers, spaces, hyphens, and underscores allowed.');
            return;
        }

        setError('');
        setLoading(true);
        setSearched(true);

        auth.authFetch('/api/search?q=' + encodeURIComponent(keyword))
            .then(function (res) {
                return res.json().then(function (data) {
                    return { ok: res.ok, data: data };
                });
            })
            .then(function (result) {
                if (!result.ok) {
                    setError(result.data.error || 'Search failed');
                    setResults(null);
                } else {
                    setResults(result.data);
                }
                setLoading(false);
            })
            .catch(function (err) {
                setError(err.message || 'Network error. Is the backend running?');
                setResults(null);
                setLoading(false);
            });
    };
    
    var handleView = function (docId) {
        // Use auth.apiBase if available, otherwise fallback to local port 5000
        var baseUrl = auth.apiBase || (window.location.protocol + '//' + window.location.hostname + ':5000');
        window.open(baseUrl + '/api/documents/' + docId + '/view?token=' + encodeURIComponent(auth.token), '_blank');
    };

    var maxScore = 1;
    if (results && results.results && results.results.length > 0) {
        maxScore = Math.max.apply(null, results.results.map(function (r) { return r.relevance_score || 0; }));
    }

    return (
        <div className="page-container" id="search-page">
            <div className="page-header">
                <h1 className="page-title">Search Legal Documents</h1>
                <p className="page-subtitle">
                    Enter a keyword to search across your indexed legal documents.
                    Results are ranked by term frequency (relevance).
                </p>
            </div>

            <div className="search-container">
                <form onSubmit={handleSearch} className="search-box-wrapper">
                    <div className="search-input-row">
                        <input
                            type="text"
                            id="search-input"
                            className="search-input"
                            placeholder="Search for a legal term... e.g. contract, bail, rights"
                            value={query}
                            onChange={function (e) { setQuery(e.target.value); }}
                            maxLength={100}
                            autoFocus
                        />
                        <button type="submit" className="search-btn" id="search-submit" disabled={loading}>
                            {loading ? '⏳' : '🔍'} Search
                        </button>
                    </div>
                </form>

                {error && <div className="error-message" id="search-error">{error}</div>}

                {loading && (
                    <div className="loading-spinner">
                        <div className="spinner"></div>
                    </div>
                )}

                {!loading && searched && results && results.count > 0 && (
                    <div>
                        <div className="search-meta">
                            <div className="search-meta-count">
                                Found <strong>{results.count}</strong> document{results.count !== 1 ? 's' : ''} for "<strong>{results.keyword}</strong>"
                            </div>
                        </div>

                        {results.results.map(function (doc, i) {
                            var barWidth = Math.max((doc.relevance_score / maxScore) * 100, 10);
                            return (
                                <div 
                                    className="result-card" 
                                    key={doc.doc_id + '-' + i} 
                                    id={'result-' + doc.doc_id}
                                    onClick={function() { handleView(doc.doc_id); }}
                                >
                                    <div className="result-title">{doc.title}</div>
                                    <div className="result-meta">
                                        <span className="badge badge-coral">{doc.category}</span>
                                        <span className="badge badge-navy">{doc.jurisdiction}</span>
                                        <span className="badge badge-sage">{doc.type_name}</span>
                                    </div>
                                    <div style={{ fontSize: '13px', color: '#6B6D80' }}>
                                        <span style={{ marginRight: '16px' }}>📄 {doc.file_name}</span>
                                        <span style={{ marginRight: '16px' }}>📏 {doc.content_length ? doc.content_length.toLocaleString() : '0'} chars</span>
                                        <span>🗓 {doc.created_at}</span>
                                    </div>
                                    <div className="result-summary">
                                        <div className="summary-badge">AI EXECUTIVE SUMMARY</div>
                                        {doc.summary || 'Summary processing...'}
                                    </div>

                                    <div className="result-footer">
                                        <div className="result-score">
                                            <span className="score-label">Relevance</span>
                                            <div className="score-bar-bg">
                                                <div
                                                    className="score-bar-fill"
                                                    style={{ width: barWidth + '%' }}
                                                ></div>
                                            </div>
                                            <span className="score-label" style={{ fontWeight: 700, color: '#E07A5F' }}>
                                                {doc.relevance_score}
                                            </span>
                                        </div>
                                        <button className="btn btn-primary btn-sm">
                                            📄 Open Document
                                        </button>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}

                {!loading && searched && results && results.count === 0 && (
                    <div className="empty-state" id="no-results">
                        <div className="empty-state-icon">🔍</div>
                        <h3>No documents found</h3>
                        <p>No indexed documents contain the term "<strong>{results.keyword}</strong>". Try a different keyword.</p>
                    </div>
                )}

                {!searched && (
                    <div className="empty-state" id="search-prompt">
                        <div className="empty-state-icon">⚖️</div>
                        <h3>Search across your legal corpus</h3>
                        <p>Type a keyword above to search across all your indexed legal documents.</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default SearchPage;

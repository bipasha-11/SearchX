import React, { useState, useEffect } from 'react';
import { useAuth } from '../AuthContext';

var BAR_COLORS = ['bar-fill-coral', 'bar-fill-navy', 'bar-fill-sage'];

function AnalyticsPage() {
    var auth = useAuth();
    var analyticsState = useState(null);
    var analytics = analyticsState[0];
    var setAnalytics = analyticsState[1];

    var docsState = useState(null);
    var documents = docsState[0];
    var setDocuments = docsState[1];

    var loadingState = useState(true);
    var loading = loadingState[0];
    var setLoading = loadingState[1];

    var errorState = useState('');
    var error = errorState[0];
    var setError = errorState[1];

    useEffect(function () {
        fetchData();
    }, []);

    function fetchData() {
        setLoading(true);
        setError('');

        Promise.all([
            auth.authFetch('/api/analytics?limit=10'),
            auth.authFetch('/api/documents'),
        ])
            .then(function (responses) {
                var analyticsRes = responses[0];
                var docsRes = responses[1];

                if (!analyticsRes.ok || !docsRes.ok) {
                    setError('Failed to fetch analytics data');
                    setLoading(false);
                    return;
                }

                return Promise.all([analyticsRes.json(), docsRes.json()])
                    .then(function (data) {
                        setAnalytics(data[0]);
                        setDocuments(data[1]);
                        setLoading(false);
                    });
            })
            .catch(function () {
                setError('Network error. Is the backend running?');
                setLoading(false);
            });
    }

    if (loading) {
        return (
            <div className="page-container">
                <div className="loading-spinner"><div className="spinner"></div></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="page-container">
                <div className="error-message" id="analytics-error">{error}</div>
            </div>
        );
    }

    var stats = (analytics && analytics.stats) || {};
    var topTerms = (analytics && analytics.top_terms) || [];
    var docs = (documents && documents.documents) || [];

    var maxCount = topTerms.length > 0
        ? Math.max.apply(null, topTerms.map(function (t) { return t.search_count; }))
        : 1;

    return (
        <div className="page-container" id="analytics-page">
            <div className="page-header">
                <h1 className="page-title">Search Analytics</h1>
                <p className="page-subtitle">
                    Query analytics powered by Oracle QUERY_LOG and DOCUMENT_STATS tables.
                </p>
            </div>

            <div className="analytics-grid" id="stats-grid">
                <div className="stat-card" id="stat-documents">
                    <div className="stat-card-label">Total Documents</div>
                    <div className="stat-card-value">{stats.total_documents || 0}</div>
                </div>
                <div className="stat-card" id="stat-terms">
                    <div className="stat-card-label">Unique Terms</div>
                    <div className="stat-card-value">{stats.total_unique_terms || 0}</div>
                </div>
                <div className="stat-card" id="stat-queries">
                    <div className="stat-card-label">Unique Queries</div>
                    <div className="stat-card-value">{stats.total_unique_queries || 0}</div>
                </div>
                <div className="stat-card" id="stat-searches">
                    <div className="stat-card-label">Total Searches</div>
                    <div className="stat-card-value">{stats.total_searches || 0}</div>
                </div>
            </div>

            <div className="analytics-panels">
                <div className="chart-container" id="top-terms-chart">
                    <h3>Top Searched Terms</h3>
                    {topTerms.length === 0 ? (
                        <div className="empty-state">
                            <p>No search data yet. Try searching for something first!</p>
                        </div>
                    ) : (
                        <div className="bar-chart">
                            {topTerms.map(function (term, idx) {
                                var barWidth = Math.max((term.search_count / maxCount) * 100, 8);
                                return (
                                    <div className="bar-row" key={term.search_term}>
                                        <div className="bar-label">{term.search_term}</div>
                                        <div className="bar-track">
                                            <div
                                                className={'bar-fill ' + BAR_COLORS[idx % BAR_COLORS.length]}
                                                style={{ width: barWidth + '%' }}
                                            >
                                                {term.search_count}
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>

                <div className="chart-container" id="top-terms-table">
                    <h3>Search Log Details</h3>
                    {topTerms.length === 0 ? (
                        <div className="empty-state">
                            <p>No search queries logged yet.</p>
                        </div>
                    ) : (
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Term</th>
                                    <th>Searches</th>
                                    <th>Last Searched</th>
                                </tr>
                            </thead>
                            <tbody>
                                {topTerms.map(function (term, idx) {
                                    return (
                                        <tr key={term.search_term}>
                                            <td>{idx + 1}</td>
                                            <td style={{ fontWeight: 600 }}>{term.search_term}</td>
                                            <td>
                                                <span className="badge badge-coral">{term.search_count}</span>
                                            </td>
                                            <td style={{ fontSize: '13px', color: '#6B6D80' }}>
                                                {term.last_searched || '—'}
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    )}
                </div>
            </div>

            <div className="chart-container" style={{ marginTop: '24px' }} id="documents-table">
                <h3>Indexed Documents</h3>
                {docs.length === 0 ? (
                    <div className="empty-state">
                        <p>No documents indexed yet.</p>
                    </div>
                ) : (
                    <div style={{ overflowX: 'auto' }}>
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Title</th>
                                    <th>Category</th>
                                    <th>Jurisdiction</th>
                                    <th>Type</th>
                                    <th>Terms</th>
                                    <th>Length</th>
                                    <th>Indexed</th>
                                </tr>
                            </thead>
                            <tbody>
                                {docs.map(function (doc) {
                                    return (
                                        <tr key={doc.doc_id}>
                                            <td>{doc.doc_id}</td>
                                            <td style={{ fontWeight: 500, maxWidth: '250px' }}>{doc.title}</td>
                                            <td><span className="badge badge-coral">{doc.category}</span></td>
                                            <td><span className="badge badge-navy">{doc.jurisdiction}</span></td>
                                            <td><span className="badge badge-sage">{doc.type_name}</span></td>
                                            <td>{doc.unique_terms}</td>
                                            <td>{doc.content_length ? doc.content_length.toLocaleString() : '0'}</td>
                                            <td style={{ fontSize: '13px', color: '#6B6D80' }}>{doc.created_at || '—'}</td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}

export default AnalyticsPage;

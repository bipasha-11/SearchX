import React, { useState, useEffect } from 'react';
import { useAuth } from '../AuthContext';

function MyDocumentsPage() {
    var auth = useAuth();
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
        fetchDocuments();
    }, []);

    function fetchDocuments() {
        setLoading(true);
        setError('');
        auth.authFetch('/api/documents')
            .then(function (res) {
                if (!res.ok) throw new Error('Failed to fetch documents');
                return res.json();
            })
            .then(function (data) {
                setDocuments(data.documents);
                setLoading(false);
            })
            .catch(function (err) {
                setError(err.message);
                setLoading(false);
            });
    }

    var handleDelete = function (docId, title) {
        if (!window.confirm('Are you sure you want to delete "' + title + '"? This will remove all indexed terms and cannot be undone.')) {
            return;
        }

        auth.authFetch('/api/documents/' + docId, { method: 'DELETE' })
            .then(function (res) {
                if (!res.ok) return res.json().then(function(d){ throw new Error(d.error || 'Delete failed'); });
                return res.json();
            })
            .then(function () {
                // Refresh list
                fetchDocuments();
            })
            .catch(function (err) {
                alert('Error: ' + err.message);
            });
    };

    var handleView = function (docId) {
        var baseUrl = auth.apiBase || (window.location.protocol + '//' + window.location.hostname + ':5000');
        window.open(baseUrl + '/api/documents/' + docId + '/view?token=' + encodeURIComponent(auth.token), '_blank');
    };

    if (loading) {
        return (
            <div className="page-container">
                <div className="loading-spinner"><div className="spinner"></div></div>
            </div>
        );
    }

    return (
        <div className="page-container" id="my-documents-page">
            <div className="page-header">
                <h1 className="page-title">My Uploaded Documents</h1>
                <p className="page-subtitle">
                    Manage your legal corpus. You can view original files or remove them from the index.
                </p>
            </div>

            {error && <div className="error-message" id="docs-error">{error}</div>}

            <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
                {(!documents || documents.length === 0) ? (
                    <div className="empty-state" style={{ padding: '60px 20px' }}>
                        <div className="empty-state-icon">📄</div>
                        <h3>No documents found</h3>
                        <p>You haven't uploaded any documents yet. Start by indexing your first legal file!</p>
                        <button 
                            className="btn btn-primary" 
                            style={{ marginTop: '20px' }}
                            onClick={function() { window.location.href = '/upload'; }}
                        >
                            Upload Now
                        </button>
                    </div>
                ) : (
                    <div style={{ overflowX: 'auto' }}>
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Document Title</th>
                                    <th>Category</th>
                                    <th>Jurisdiction</th>
                                    <th>Terms</th>
                                    <th>Uploaded</th>
                                    <th style={{ textAlign: 'right' }}>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {documents.map(function (doc) {
                                    return (
                                        <tr key={doc.doc_id}>
                                            <td style={{ color: '#6B6D80', fontSize: '12px' }}>#{doc.doc_id}</td>
                                            <td>
                                                <div style={{ fontWeight: 600, color: 'var(--navy)' }}>{doc.title}</div>
                                                <div style={{ fontSize: '12px', color: '#6B6D80' }}>📄 {doc.file_name}</div>
                                            </td>
                                            <td><span className="badge badge-coral">{doc.category}</span></td>
                                            <td><span className="badge badge-navy">{doc.jurisdiction}</span></td>
                                            <td>
                                                <div style={{ fontWeight: 600 }}>{doc.unique_terms}</div>
                                                <div style={{ fontSize: '11px', color: '#6B6D80' }}>unique terms</div>
                                            </td>
                                            <td style={{ fontSize: '13px', color: '#6B6D80' }}>
                                                {doc.created_at ? doc.created_at.split(' ')[0] : '—'}
                                            </td>
                                            <td style={{ textAlign: 'right' }}>
                                                <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
                                                    <button 
                                                        className="btn btn-secondary btn-sm"
                                                        onClick={function() { handleView(doc.doc_id); }}
                                                    >
                                                        View
                                                    </button>
                                                    <button 
                                                        className="btn btn-outline btn-sm"
                                                        style={{ borderColor: '#e74c3c', color: '#e74c3c' }}
                                                        onClick={function() { handleDelete(doc.doc_id, doc.title); }}
                                                    >
                                                        Delete
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
            
            <div style={{ marginTop: '20px', textAlign: 'right', fontSize: '13px', color: '#6B6D80' }}>
                Total Documents: <strong>{documents ? documents.length : 0}</strong>
            </div>
        </div>
    );
}

export default MyDocumentsPage;

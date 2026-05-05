import React, { useState, useRef } from 'react';
import { useAuth } from '../AuthContext';

var CATEGORIES = ['Contract', 'Case Summary', 'Policy', 'Act', 'Legal Notes'];
var JURISDICTIONS = ['Supreme Court', 'High Court', 'District', 'Corporate', 'Other'];

function UploadPage() {
    var auth = useAuth();
    
    var titleState = useState('');
    var title = titleState[0];
    var setTitle = titleState[1];

    var categoryState = useState('');
    var category = categoryState[0];
    var setCategory = categoryState[1];

    var jurisdictionState = useState('');
    var jurisdiction = jurisdictionState[0];
    var setJurisdiction = jurisdictionState[1];

    var langState = useState('1');
    var languageId = langState[0];
    var setLanguageId = langState[1];

    var fileState = useState(null);
    var file = fileState[0];
    var setFile = fileState[1];

    var textState = useState('');
    var pastedText = textState[0];
    var setPastedText = textState[1];

    var dragState = useState(false);
    var dragOver = dragState[0];
    var setDragOver = dragState[1];

    var loadState = useState(false);
    var loading = loadState[0];
    var setLoading = loadState[1];

    var errState = useState('');
    var error = errState[0];
    var setError = errState[1];

    var successState = useState(null);
    var success = successState[0];
    var setSuccess = successState[1];

    var fileInputRef = useRef(null);

    var handleFileDrop = function (e) {
        e.preventDefault();
        setDragOver(false);
        var droppedFile = e.dataTransfer.files[0];
        if (droppedFile) {
            var ext = droppedFile.name.split('.').pop().toLowerCase();
            if (['pdf', 'docx', 'txt'].indexOf(ext) !== -1) {
                setFile(droppedFile);
                setError('');
            } else {
                setError('Invalid file type. Only PDF, DOCX, and TXT are accepted.');
            }
        }
    };

    var handleFileSelect = function (e) {
        if (e.target.files[0]) {
            setFile(e.target.files[0]);
            setError('');
        }
    };

    var handleSubmit = function (e) {
        e.preventDefault();
        setError('');
        setSuccess(null);

        if (!title.trim()) { setError('Title is required.'); return; }
        if (!category) { setError('Category is required.'); return; }
        if (!jurisdiction) { setError('Jurisdiction is required.'); return; }
        if (!file && !pastedText.trim()) { setError('Upload a file or paste text.'); return; }

        setLoading(true);

        var formData = new FormData();
        formData.append('title', title.trim());
        formData.append('category', category);
        formData.append('jurisdiction', jurisdiction);
        formData.append('language_id', languageId);

        if (file) {
            formData.append('file', file);
        } else {
            formData.append('pasted_text', pastedText.trim());
        }

        auth.authFetch('/api/upload', {
            method: 'POST',
            body: formData,
        })
            .then(function (res) {
                return res.json().then(function (data) {
                    return { ok: res.ok, data: data };
                });
            })
            .then(function (result) {
                if (!result.ok) {
                    setError(result.data.error || 'Upload failed');
                } else {
                    setSuccess(result.data);
                    setTitle('');
                    setCategory('');
                    setJurisdiction('');
                    setFile(null);
                    setPastedText('');
                    if (fileInputRef.current) fileInputRef.current.value = '';
                }
                setLoading(false);
            })
            .catch(function () {
                setError('Network error. Is the backend running?');
                setLoading(false);
            });
    };

    return (
        <div className="page-container" id="upload-page">
            <div className="page-header">
                <h1 className="page-title">Upload Legal Document</h1>
                <p className="page-subtitle">
                    Upload a PDF, DOCX, or TXT file — or paste the document text directly.
                    SEARCHX will tokenize, remove stopwords, and index it via Oracle stored procedures.
                </p>
            </div>

            {error && <div className="error-message" id="upload-error">{error}</div>}

            {success && (
                <div className="upload-success" id="upload-success">
                    <h3>✓ Document Indexed Successfully</h3>
                    <p>
                        <strong>{success.title}</strong> — {success.terms_indexed} terms indexed · {success.content_length} characters · Doc ID: {success.doc_id}
                    </p>
                </div>
            )}

            <form onSubmit={handleSubmit}>
                <div className="upload-layout">
                    <div className="card">
                        <h2 className="card-title" style={{ marginBottom: '20px' }}>Document Details</h2>

                        <div className="form-group">
                            <label className="form-label" htmlFor="doc-title">Document Title</label>
                            <input
                                type="text"
                                id="doc-title"
                                className="form-input"
                                placeholder="e.g., Indian Contract Act 1872"
                                value={title}
                                onChange={function (e) { setTitle(e.target.value); }}
                                maxLength={500}
                            />
                        </div>

                        <div className="form-group">
                            <label className="form-label" htmlFor="doc-category">Category</label>
                            <select
                                id="doc-category"
                                className="form-select"
                                value={category}
                                onChange={function (e) { setCategory(e.target.value); }}
                            >
                                <option value="">Select category...</option>
                                {CATEGORIES.map(function (c) { return <option key={c} value={c}>{c}</option>; })}
                            </select>
                        </div>

                        <div className="form-group">
                            <label className="form-label" htmlFor="doc-jurisdiction">Jurisdiction</label>
                            <select
                                id="doc-jurisdiction"
                                className="form-select"
                                value={jurisdiction}
                                onChange={function (e) { setJurisdiction(e.target.value); }}
                            >
                                <option value="">Select jurisdiction...</option>
                                {JURISDICTIONS.map(function (j) { return <option key={j} value={j}>{j}</option>; })}
                            </select>
                        </div>

                        <div className="form-group">
                            <label className="form-label" htmlFor="doc-language">Language</label>
                            <select
                                id="doc-language"
                                className="form-select"
                                value={languageId}
                                onChange={function (e) { setLanguageId(e.target.value); }}
                            >
                                <option value="1">English</option>
                                <option value="2">Hindi</option>
                                <option value="3">Tamil</option>
                            </select>
                        </div>
                    </div>

                    <div className="card">
                        <h2 className="card-title" style={{ marginBottom: '20px' }}>Document Content</h2>

                        <div
                            className={'upload-zone' + (dragOver ? ' drag-over' : '')}
                            id="upload-dropzone"
                            onDragOver={function (e) { e.preventDefault(); setDragOver(true); }}
                            onDragLeave={function () { setDragOver(false); }}
                            onDrop={handleFileDrop}
                            onClick={function () { if (fileInputRef.current) fileInputRef.current.click(); }}
                        >
                            <div className="upload-zone-icon">📁</div>
                            <div className="upload-zone-text">
                                {file ? '' : 'Drag & drop a file here or click to browse'}
                            </div>
                            <div className="upload-zone-hint">Supported: PDF, DOCX, TXT (max 16 MB)</div>
                            {file && (
                                <div className="upload-file-name">✓ {file.name}</div>
                            )}
                            <input
                                type="file"
                                ref={fileInputRef}
                                style={{ display: 'none' }}
                                accept=".pdf,.docx,.txt"
                                onChange={handleFileSelect}
                            />
                        </div>

                        <div className="or-divider">— or paste text —</div>

                        <div className="form-group">
                            <textarea
                                id="doc-pasted-text"
                                className="form-textarea"
                                placeholder="Paste document text here..."
                                value={pastedText}
                                onChange={function (e) { setPastedText(e.target.value); }}
                                rows={6}
                            />
                        </div>
                    </div>
                </div>

                <div style={{ marginTop: '24px', textAlign: 'center' }}>
                    <button
                        type="submit"
                        className="btn btn-primary"
                        id="upload-submit"
                        disabled={loading}
                    >
                        {loading ? '⏳ Indexing...' : '⬆ Upload & Index Document'}
                    </button>
                </div>
            </form>
        </div>
    );
}

export default UploadPage;
